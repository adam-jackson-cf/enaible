#!/usr/bin/env bash
# Codex CLI installer for AI‑Assisted Workflows
# - Installs Codex prompts/rules into a chosen $CODEX_HOME
# - Copies Python framework to a scripts root for programmatic prompts
# - Merges config.toml (adds trust entries and chrome-devtools MCP)
# - Optionally installs Python dependencies

set -euo pipefail

SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/codex-install.log"

VERBOSE=false
DRY_RUN=false
SKIP_PYTHON=false
INSTALL_MODE=""   # fresh|merge|update|cancel (same semantics as Claude)

CODEX_HOME=""
SCRIPTS_ROOT=""

show_usage() {
  cat << 'EOF'
Codex Installer (AI‑Assisted Workflows)

USAGE:
  ./install.sh [TARGET_PATH] [OPTIONS]

ARGUMENTS:
  TARGET_PATH     Directory where .codex/ will be created (optional)
                  Examples:
                    ~/                 (User global: ~/.codex/)
                    ./myproject        (Project local: ./myproject/.codex/)
                    /path/to/project   (Custom path: /path/to/project/.codex/)
                  Default: interactive menu (defaults to ~/.codex when non‑TTY)

OPTIONS:
  -h, --help        Show this help
  -v, --verbose     Verbose logs
  -n, --dry-run     Show actions without making changes
  --skip-python     Skip Python dependency installation
  --mode <value>    Installation mode for existing installs: fresh|merge|update|cancel

NOTES:
  - This installer always copies ALL Codex prompts and rules.
  - Programmatic prompts that call Python require a scripts root and Python 3.11+.
  - We add trust entries for selected locations in config.toml.
EOF
}

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
vlog() { [[ "$VERBOSE" == true ]] && log "$@" || echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; }
err() { echo "[ERROR] $*" | tee -a "$LOG_FILE" >&2; }

parse_args() {
  TARGET_PATH=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help) show_usage; exit 0 ;;
      -v|--verbose) VERBOSE=true; shift ;;
      -n|--dry-run) DRY_RUN=true; shift ;;
      --skip-python) SKIP_PYTHON=true; shift ;;
      --mode)
        if [[ -n "${2:-}" ]]; then
          case "$2" in fresh|merge|update|cancel) INSTALL_MODE="$2" ;; *) err "Invalid --mode $2"; exit 1;; esac
          shift 2
        else err "--mode requires a value"; exit 1; fi
        ;;
      -*) err "Unknown option: $1"; show_usage; exit 1 ;;
      *) if [[ -z "${TARGET_PATH}" ]]; then TARGET_PATH="$1"; else err "Multiple target paths"; exit 1; fi; shift ;;
    esac
  done
}

resolve_scope_interactive() {
  local default_non_tty="$HOME"

  if [[ -n "${TARGET_PATH}" ]]; then
    # Convert ~ and relative -> absolute
    [[ "$TARGET_PATH" == "~" ]] && TARGET_PATH="$HOME"
    [[ "$TARGET_PATH" == ~* ]] && TARGET_PATH="${TARGET_PATH/#\~/$HOME}"
    TARGET_PATH=$(realpath "$TARGET_PATH" 2>/dev/null || echo "$TARGET_PATH")
    if [[ "$TARGET_PATH" == */.codex ]]; then CODEX_HOME="$TARGET_PATH"; else CODEX_HOME="$TARGET_PATH/.codex"; fi
    return
  fi

  if [[ ! -t 0 ]]; then
    CODEX_HOME="$HOME/.codex"
    vlog "Non‑TTY detected; defaulting CODEX_HOME=$CODEX_HOME"
    return
  fi

  echo ""
  echo "Choose install scope for Codex home (stores prompts/rules/config):"
  echo "  1) User level (~/.codex) [default]"
  echo "  2) Project level (./.codex)"
  echo "  3) Custom path"
  local choice
  read -r -p "Enter choice [1-3]: " choice; choice=${choice:-1}
  case "$choice" in
    1) CODEX_HOME="$HOME/.codex" ;;
    2) CODEX_HOME="$(pwd)/.codex" ;;
    3) read -r -p "Enter absolute path (we will create <path>/.codex if needed): " TARGET_PATH
       [[ "$TARGET_PATH" == "~" ]] && TARGET_PATH="$HOME"
       [[ "$TARGET_PATH" == ~* ]] && TARGET_PATH="${TARGET_PATH/#\~/$HOME}"
       TARGET_PATH=$(realpath "$TARGET_PATH" 2>/dev/null || echo "$TARGET_PATH")
       if [[ "$TARGET_PATH" == */.codex ]]; then CODEX_HOME="$TARGET_PATH"; else CODEX_HOME="$TARGET_PATH/.codex"; fi
       ;;
    *) CODEX_HOME="$HOME/.codex" ;;
  esac
}

choose_scripts_root() {
  if [[ ! -t 0 ]]; then
    # Default scripts beside home
    SCRIPTS_ROOT="$CODEX_HOME/scripts"
    return
  fi
  echo ""
  echo "Where should Python scripts (programmatic prompts) live?"
  echo "  1) Inside Codex home ($CODEX_HOME/scripts) [default]"
  echo "  2) User level (~/.codex/scripts)"
  echo "  3) Custom path"
  local choice; read -r -p "Enter choice [1-3]: " choice; choice=${choice:-1}
  case "$choice" in
    1) SCRIPTS_ROOT="$CODEX_HOME/scripts" ;;
    2) SCRIPTS_ROOT="$HOME/.codex/scripts" ;;
    3) read -r -p "Enter absolute path to scripts root: " SCRIPTS_ROOT
       [[ "$SCRIPTS_ROOT" == "~" ]] && SCRIPTS_ROOT="$HOME"
       [[ "$SCRIPTS_ROOT" == ~* ]] && SCRIPTS_ROOT="${SCRIPTS_ROOT/#\~/$HOME}"
       SCRIPTS_ROOT=$(realpath "$SCRIPTS_ROOT" 2>/dev/null || echo "$SCRIPTS_ROOT")
       ;;
    *) SCRIPTS_ROOT="$CODEX_HOME/scripts" ;;
  esac
}

ensure_dirs() {
  [[ "$DRY_RUN" == true ]] && { log "Would create: $CODEX_HOME"; log "Would create: $SCRIPTS_ROOT"; return; }
  mkdir -p "$CODEX_HOME" "$SCRIPTS_ROOT"
}

backup_existing() {
  if [[ -d "$CODEX_HOME" ]]; then
    if [[ "$DRY_RUN" == true ]]; then
      log "Would backup existing $CODEX_HOME"
    else
      local backup_dir="${CODEX_HOME}.backup.$(date +%Y%m%d_%H%M%S)"
      cp -r "$CODEX_HOME" "$backup_dir"
      log "Backup created: $backup_dir"
      # Determine mode
      local choice
      if [[ -n "$INSTALL_MODE" ]]; then
        case "$INSTALL_MODE" in fresh) choice=1;; merge) choice=2;; update) choice=3;; cancel) choice=4;; esac
        echo "Non‑interactive mode: $INSTALL_MODE"
      elif [[ ! -t 0 ]]; then
        choice=3
        echo "Non‑interactive environment: defaulting to update"
      else
        echo "Found existing $CODEX_HOME"
        echo "  1) Fresh (replace)\n  2) Merge\n  3) Update (prompts/rules/config only)\n  4) Cancel"
        while true; do read -r -p "Enter choice [1-4] (default 3): " choice; choice=${choice:-3}; [[ $choice =~ ^[1-4]$ ]] && break; done
      fi
      case $choice in
        1) rm -rf "$CODEX_HOME"; mkdir -p "$CODEX_HOME" ;;
        2) : ;; # merge path handled by copy logic
        3) : ;;
        4) log "Cancelled by user"; exit 0 ;;
      esac
    fi
  fi
}

copy_prompts_and_rules() {
  local src_prompts="$SCRIPT_DIR/prompts"
  local src_rules="$SCRIPT_DIR/rules"
  [[ -d "$src_prompts" ]] || { err "Missing prompts dir: $src_prompts"; exit 1; }
  [[ -d "$src_rules" ]] || { err "Missing rules dir: $src_rules"; exit 1; }

  if [[ "$DRY_RUN" == true ]]; then
    log "Would copy prompts -> $CODEX_HOME/prompts"
    log "Would copy rules   -> $CODEX_HOME/rules"
    return
  fi

  mkdir -p "$CODEX_HOME/prompts" "$CODEX_HOME/rules"

  # Merge: overwrite built‑ins, preserve unknown files
  rsync -a --delete-excluded --exclude '.*' "$src_prompts/" "$CODEX_HOME/prompts/"
  rsync -a --delete-excluded --exclude '.*' "$src_rules/"   "$CODEX_HOME/rules/"
  log "Copied prompts and rules"
}

copy_python_framework() {
  # Copy only required shared subtrees
  local src_root="$(cd "$SCRIPT_DIR/.." && pwd)/shared"
  local subdirs=(core analyzers setup config utils generators context)
  for d in "${subdirs[@]}"; do
    local src="$src_root/$d"
    [[ -d "$src" ]] || { err "Missing shared subtree: $src"; exit 1; }
  done

  if [[ "$DRY_RUN" == true ]]; then
    log "Would copy Python framework to $SCRIPTS_ROOT/{${subdirs[*]}}"
    return
  fi

  mkdir -p "$SCRIPTS_ROOT"
  for d in "${subdirs[@]}"; do
    rsync -a --delete-excluded --exclude '.*' "$src_root/$d/" "$SCRIPTS_ROOT/$d/"
  done
  log "Copied Python framework to $SCRIPTS_ROOT"
}

# --- Node tools (ESLint + jscpd) setup ---
check_node() {
  if ! command -v node >/dev/null 2>&1; then
    err "Node.js is required for frontend analysis and jscpd. Install from https://nodejs.org"
    exit 1
  fi
  if ! command -v npm >/dev/null 2>&1; then
    err "npm is required for Node tool installation"
    exit 1
  fi
  vlog "Node $(node --version), npm $(npm --version)"
}

install_node_tools() {
  check_node
  local tools_dir="$CODEX_HOME/eslint"
  mkdir -p "$tools_dir"
  cd "$tools_dir"
  if [[ ! -f package.json ]]; then
    cat > package.json << 'EOF'
{
  "name": "codex-node-tools",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "eslint": "^8.0.0",
    "@typescript-eslint/parser": "^5.0.0",
    "@typescript-eslint/eslint-plugin": "^5.0.0",
    "eslint-plugin-react": "^7.32.0",
    "eslint-plugin-import": "^2.27.0",
    "eslint-plugin-vue": "^9.0.0",
    "jscpd": "^3.5.0"
  }
}
EOF
  else
    if ! grep -q '"jscpd"' package.json; then
      tmpfile=$(mktemp)
      awk '{print} /"dependencies"\s*:\s*\{/ && !x {print "    \"jscpd\": \"^3.5.0\","; x=1}' package.json > "$tmpfile" && mv "$tmpfile" package.json
    fi
  fi
  vlog "Installing Node tools (ESLint + jscpd)..."
  npm install --no-fund --no-audit --silent >> "$LOG_FILE" 2>&1 || { err "npm install failed"; exit 1; }
}

PYTHON_BIN=""
select_python() {
  local candidates=(python python3)
  for cand in "${candidates[@]}"; do
    if command -v "$cand" >/dev/null 2>&1; then
      if "$cand" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" 2>/dev/null; then
        PYTHON_BIN="$cand"; break
      fi
    fi
  done
  if [[ -z "$PYTHON_BIN" ]]; then
    err "Python 3.11+ is required but not found as 'python' or 'python3'"; exit 1
  fi
  vlog "Selected interpreter: $PYTHON_BIN ($($PYTHON_BIN -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'))"
}

install_python_deps() {
  if [[ "$SKIP_PYTHON" == true ]]; then log "Skipping Python dependency installation"; return; fi
  select_python

  local req_file="$SCRIPTS_ROOT/setup/requirements.txt"
  [[ -f "$req_file" ]] || { err "Missing requirements file: $req_file"; exit 1; }

  if [[ "$DRY_RUN" == true ]]; then
    log "Would install Python deps from $req_file"
    return
  fi

  log "Installing Python dependencies..."
  PYTHONPATH="$SCRIPTS_ROOT" "$PYTHON_BIN" "$SCRIPTS_ROOT/setup/install_dependencies.py" <<< "y" >> "$LOG_FILE" 2>&1 || {
    err "Dependency installation failed. See $LOG_FILE"; exit 1; }
  log "Python dependencies installed"
}

ensure_config() {
  local cfg="$CODEX_HOME/config.toml"
  if [[ "$DRY_RUN" == true ]]; then
    log "Would ensure config at $cfg and merge trust + mcp"
    return
  fi
  mkdir -p "$CODEX_HOME"
  if [[ ! -f "$cfg" ]]; then
    cp "$SCRIPT_DIR/config.toml" "$cfg"
    log "Created $cfg from template"
  fi

  # Idempotently ensure chrome-devtools MCP block exists
  if ! grep -q "^\[mcp_servers\.chrome-devtools\]" "$cfg" 2>/dev/null; then
    cat >> "$cfg" << 'EOF'

[mcp_servers.chrome-devtools]
command = "npx"
args = ["chrome-devtools-mcp@latest", "--headless", "--isolated"]
EOF
    log "Added mcp_servers.chrome-devtools to config.toml"
  fi

  # Add trust entries for CODEX_HOME and SCRIPTS_ROOT
  add_trust_entry "$cfg" "$CODEX_HOME"
  if [[ "$SCRIPTS_ROOT" != "$CODEX_HOME" && "$SCRIPTS_ROOT" != "$CODEX_HOME"/* ]]; then
    add_trust_entry "$cfg" "$SCRIPTS_ROOT"
  fi
}

add_trust_entry() {
  local cfg="$1"; local path="$2"
  # Normalize: strip trailing slashes
  local abs="${path%/}"
  local tilde="$abs"
  if [[ "$tilde" == "$HOME"* ]]; then
    tilde="~${tilde#$HOME}"
  fi
  # Idempotency: check for either absolute or tilde-mapped section
  if grep -Fq "[projects.\"$abs\"]" "$cfg" 2>/dev/null || \
     grep -Fq "[projects.\"$tilde\"]" "$cfg" 2>/dev/null; then
    vlog "Trust entry already present for $abs (or $tilde)"
    return
  fi
  printf "\n[projects.\"%s\"]\ntrust_level = \"trusted\"\n" "$abs" >> "$cfg"
  log "Added trust for $abs in config.toml"
}

update_agents_md() {
  local target="$CODEX_HOME/AGENTS.md"
  local header="# AI-Assisted Workflows (Codex Global Rules) v$SCRIPT_VERSION - Auto-generated, do not edit"
  local src_agents="$SCRIPT_DIR/rules/global.codex.rules.md"
  [[ -f "$src_agents" ]] || { vlog "Global Codex rules not found; skipping AGENTS.md update"; return 0; }

  if [[ "$DRY_RUN" == true ]]; then
    log "Would append project AGENTS.md section to $target if not present"
    return
  fi

  mkdir -p "$CODEX_HOME"
  touch "$target"
  if grep -qF "$header" "$target" 2>/dev/null; then
    vlog "AGENTS.md section already exists"
    return
  fi
  {
    echo ""; echo "$header"; echo ""; cat "$src_agents"
  } >> "$target"
  log "Updated $target with AI‑Assisted Workflows section"
}

inject_shell_helpers() {
  [[ ! -t 0 ]] && return 0
  echo ""
  echo "Add Codex shell helpers (recommended)?"
  echo "  - cdx                (codex --full-auto)"
  echo "  - cdx-no-sandbox-on-request  (danger-full-access + on-request)"
  echo "  - cdx-no-sandbox-on-failure  (danger-full-access + on-failure)"
  echo "  - cdx-exec           (codex exec ...)"
  read -r -p "Append helpers to your shell profile? [Y/n]: " yn; yn=${yn:-Y}
  case "$yn" in
    Y|y)
      local profile
      if [[ -n "${ZSH_VERSION:-}" ]]; then profile="$HOME/.zshrc";
      elif [[ -n "${BASH_VERSION:-}" ]]; then profile="$HOME/.bashrc";
      else profile="$HOME/.zshrc"; fi
      if [[ "$DRY_RUN" == true ]]; then
        log "Would append helpers to $profile"
      else
        echo "" >> "$profile"
        cat "$SCRIPT_DIR/codex-init-helpers.md" | sed -n '/^```bash$/,/^```$/p' | sed '1d;$d' >> "$profile"
        log "Appended helpers to $profile"
        echo "Run: source $profile (or open a new shell)"
      fi
      ;;
  esac
}

verify_install() {
  [[ "$DRY_RUN" == true ]] && { log "Dry-run: skipping verification"; return; }
  local ok=1
  [[ -d "$CODEX_HOME/prompts" ]] || { err "Missing prompts at $CODEX_HOME/prompts"; ok=0; }
  [[ -d "$CODEX_HOME/rules" ]]   || { err "Missing rules at $CODEX_HOME/rules"; ok=0; }
  select_python || true
  if ! PYTHONPATH="$SCRIPTS_ROOT" ${PYTHON_BIN:-python3} -c "import core.base" >/dev/null 2>&1; then
    err "Python import failed (PYTHONPATH=$SCRIPTS_ROOT). Programmatic prompts may not work."
    ok=0
  fi
  [[ $ok -eq 1 ]] && log "Verification successful" || { err "Verification had errors. See $LOG_FILE"; exit 1; }
}

completion_msg() {
  echo ""
  echo "✅ Codex installation complete"
  echo "  CODEX_HOME:   $CODEX_HOME"
  echo "  SCRIPTS_ROOT: $SCRIPTS_ROOT"
  echo "  Config:       $CODEX_HOME/config.toml (trust entries added)"
  echo ""
  echo "Use helpers (if enabled): cdx | cdx-no-sandbox-on-request | cdx-no-sandbox-on-failure"
  echo "For minimal prompts: keep scripts inside project ./.codex/scripts and run with --sandbox workspace-write."
}

main() {
  echo "Codex Installer v$SCRIPT_VERSION" > "$LOG_FILE"
  parse_args "$@"
  resolve_scope_interactive
  choose_scripts_root
  ensure_dirs
  backup_existing
  copy_prompts_and_rules
  copy_python_framework
  install_python_deps
  install_node_tools
  ensure_config
  update_agents_md
  inject_shell_helpers
  verify_install
  completion_msg
}

main "$@"
