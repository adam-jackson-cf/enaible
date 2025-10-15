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
EFFECTIVE_MODE="fresh"

CODEX_HOME=""
SCRIPTS_ROOT=""
SCRIPTS_ROOT_OVERRIDE=""

TOTAL_PHASES=11
CURRENT_PHASE=0

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
  --mode <value>    Installation mode when an existing install is found:
                      fresh  – Reinstall core assets (preserves auth.json, log/, sessions/)
                      merge  – Overlay Codex files without removing unknown files
                      update – Overlay core assets and refresh bundled templates (e.g. ExecPlan)
                      cancel – Abort without making changes

NOTES:
  - This installer always copies ALL Codex prompts and rules.
  - Programmatic prompts that call Python require a scripts root and Python 3.11+.
  - We add trust entries for selected locations in config.toml.
EOF
}

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
vlog() { [[ "$VERBOSE" == true ]] && log "$@" || echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; }
err() { echo "[ERROR] $*" | tee -a "$LOG_FILE" >&2; }

show_header() {
  echo ""
  echo "┌─────────────────────────────────────┐"
  echo "│        Codex CLI Installer          │"
  echo "│        Version $SCRIPT_VERSION          │"
  echo "└─────────────────────────────────────┘"
}

next_phase() {
  CURRENT_PHASE=$((CURRENT_PHASE + 1))
  echo ""
  echo "[$CURRENT_PHASE/$TOTAL_PHASES] $1"
  echo "----------------------------------------"
}

normalize_path() {
  local raw="$1"
  [[ "$raw" == "~" ]] && raw="$HOME"
  if [[ "$raw" == ~* ]]; then
    raw="${raw/#\~/$HOME}"
  fi
  realpath "$raw" 2>/dev/null || echo "$raw"
}

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
      --scripts-root)
        if [[ -n "${2:-}" ]]; then
          SCRIPTS_ROOT_OVERRIDE="$2"
          shift 2
        else err "--scripts-root requires a value"; exit 1; fi
        ;;
      -*) err "Unknown option: $1"; show_usage; exit 1 ;;
      *) if [[ -z "${TARGET_PATH}" ]]; then TARGET_PATH="$1"; else err "Multiple target paths"; exit 1; fi; shift ;;
    esac
  done
}

resolve_scope_interactive() {
  if [[ -n "${TARGET_PATH}" ]]; then
    local normalized_target
    normalized_target=$(normalize_path "${TARGET_PATH}")
    if [[ "$normalized_target" == */.codex ]]; then
      CODEX_HOME="$normalized_target"
    else
      CODEX_HOME="$normalized_target/.codex"
    fi
  elif [[ ! -t 0 ]]; then
    CODEX_HOME="$HOME/.codex"
    vlog "Non-TTY detected; defaulting CODEX_HOME=$CODEX_HOME"
  else
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
      3)
        read -r -p "Enter absolute path (we will create <path>/.codex if needed): " TARGET_PATH
        local normalized_custom
        normalized_custom=$(normalize_path "${TARGET_PATH}")
        if [[ "$normalized_custom" == */.codex ]]; then
          CODEX_HOME="$normalized_custom"
        else
          CODEX_HOME="$normalized_custom/.codex"
        fi
        ;;
      *) CODEX_HOME="$HOME/.codex" ;;
    esac
  fi

  if [[ -z "$CODEX_HOME" ]]; then
    CODEX_HOME="$HOME/.codex"
  fi

  if [[ -n "$SCRIPTS_ROOT_OVERRIDE" ]]; then
    SCRIPTS_ROOT=$(normalize_path "$SCRIPTS_ROOT_OVERRIDE")
  else
    SCRIPTS_ROOT="$CODEX_HOME/scripts"
  fi

  vlog "Resolved CODEX_HOME=$CODEX_HOME"
  vlog "Resolved SCRIPTS_ROOT=$SCRIPTS_ROOT"
}


ensure_dirs() {
  [[ "$DRY_RUN" == true ]] && { log "Would create: $CODEX_HOME"; log "Would create: $SCRIPTS_ROOT"; return; }
  mkdir -p "$CODEX_HOME" "$SCRIPTS_ROOT"
}

preserve_fresh_artifacts() {
  local preserve_items=("auth.json" "log" "sessions")
  local temp_dir
  temp_dir=$(mktemp -d "${TMPDIR:-/tmp}/codex-preserve.XXXXXX")
  local preserved=()

  for item in "${preserve_items[@]}"; do
    local src="$CODEX_HOME/$item"
    if [[ -f "$src" ]]; then
      mkdir -p "$(dirname "$temp_dir/$item")"
      cp -p "$src" "$temp_dir/$item"
      preserved+=("$item")
    elif [[ -d "$src" ]]; then
      mkdir -p "$temp_dir/$item"
      rsync -a "$src/" "$temp_dir/$item/"
      preserved+=("$item/")
    fi
  done

  rm -rf "$CODEX_HOME"
  mkdir -p "$CODEX_HOME"

  for item in "${preserve_items[@]}"; do
    local staged="$temp_dir/$item"
    local dest="$CODEX_HOME/$item"
    if [[ -f "$staged" ]]; then
      mkdir -p "$(dirname "$dest")"
      cp -p "$staged" "$dest"
    elif [[ -d "$staged" ]]; then
      mkdir -p "$dest"
      rsync -a "$staged/" "$dest/"
    fi
  done

  rm -rf "$temp_dir"

  if [[ ${#preserved[@]} -gt 0 ]]; then
    log "Preserved ${preserved[*]} during fresh install"
  else
    log "Fresh install: no auth.json/log/sessions to preserve"
  fi
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
        cat <<'EOF'
  1) Fresh – reinstall core Codex assets (auth.json, log/, sessions/ are kept)
  2) Merge – add/update Codex files but leave any other files untouched
  3) Update – refresh core Codex assets and bundled templates (ExecPlan, global rules)
  4) Cancel
EOF
        while true; do read -r -p "Enter choice [1-4] (default 3): " choice; choice=${choice:-3}; [[ $choice =~ ^[1-4]$ ]] && break; done
      fi
      case $choice in
        1)
          EFFECTIVE_MODE="fresh"
          if [[ "$DRY_RUN" == true ]]; then
            log "Would perform fresh install while retaining auth.json, log/, and sessions/ (if present)"
          else
            preserve_fresh_artifacts
          fi
          ;;
        2)
          EFFECTIVE_MODE="merge"
          ;;
        3)
          EFFECTIVE_MODE="update"
          ;;
        4)
          log "Cancelled by user"; exit 0 ;;
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
  # The repo layout has `shared/` at the repository root, sibling to `systems/`.
  # This script lives in `systems/codex/`, so we must go two levels up.
  local src_root="$(cd "$SCRIPT_DIR/../.." && pwd)/shared"
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
  if [[ "$DRY_RUN" == true ]]; then
    log "Would install Node tools into $tools_dir"
    return
  fi
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
  log "Installing Node tools (ESLint + jscpd)..."
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
  local start_marker="<!-- CODEx_GLOBAL_RULES_START -->"
  local end_marker="<!-- CODEx_GLOBAL_RULES_END -->"
  [[ -f "$src_agents" ]] || { vlog "Global Codex rules not found; skipping AGENTS.md update"; return 0; }

  if [[ "$DRY_RUN" == true ]]; then
    log "Would ensure Codex global rules section is updated without duplicates in $target"
    return
  fi

  mkdir -p "$CODEX_HOME"
  touch "$target"

  TARGET="$target" SRC_AGENTS="$src_agents" HEADER="$header" START_MARKER="$start_marker" END_MARKER="$end_marker" python <<'PY'
import os
import re
from pathlib import Path

target_path = Path(os.environ["TARGET"])
header = os.environ["HEADER"].strip()
start_marker = os.environ["START_MARKER"]
end_marker = os.environ["END_MARKER"]
src_rules = Path(os.environ["SRC_AGENTS"]).read_text(encoding="utf-8").strip()

if target_path.exists():
    existing = target_path.read_text(encoding="utf-8")
else:
    existing = ""

line_ending = "\r\n" if "\r\n" in existing else "\n"
existing_norm = existing.replace("\r\n", "\n")

block_body = f"{header}\n\n{src_rules.strip()}\n"
block = f"{start_marker}\n{block_body}{end_marker}"

def parse_sections(text: str):
    pattern = re.compile(r'^(#{1,6})\s+(.+?)\s*$', re.MULTILINE)
    matches = list(pattern.finditer(text))
    sections = []
    for idx, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        start = match.start()
        end = len(text)
        for next_idx in range(idx + 1, len(matches)):
            next_level = len(matches[next_idx].group(1))
            if next_level <= level:
                end = matches[next_idx].start()
                break
        sections.append((level, title, start, end))
    return sections

updated = None

if start_marker in existing_norm and end_marker in existing_norm:
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    updated = pattern.sub(block, existing_norm)
else:
    sections = parse_sections(existing_norm)
    source_sections = parse_sections(block_body)
    source_keys = {(lvl, title) for (lvl, title, _, _) in source_sections}
    first_start = None
    last_end = None
    for level, title, start, end in sections:
        if (level, title) in source_keys:
            if first_start is None:
                first_start = start
            last_end = end
    if first_start is not None and last_end is not None:
        before = existing_norm[:first_start].rstrip("\n")
        after = existing_norm[last_end:].lstrip("\n")
        parts = []
        if before:
            parts.append(before)
        parts.append(block)
        if after:
            parts.append(after)
        updated = "\n\n".join(parts).strip() + "\n"
    else:
        cleaned = existing_norm.rstrip()
        if cleaned:
            updated = f"{cleaned}\n\n{block}\n"
        else:
            updated = f"{block}\n"

if updated is None:
    updated = f"{block}\n"

final = updated.replace("\n", line_ending)
target_path.write_text(final, encoding="utf-8")
PY

  log "Updated $target with AI‑Assisted Workflows section"

  # Also place the ExecPlan template alongside AGENTS.md
  local src_execplan="$SCRIPT_DIR/execplan.md"
  local dst_execplan="$CODEX_HOME/execplan.md"
  if [[ -f "$src_execplan" ]]; then
    if [[ "$DRY_RUN" == true ]]; then
      if [[ "$EFFECTIVE_MODE" == "update" ]]; then
        log "Would overwrite ExecPlan template at $dst_execplan (update mode)"
      else
        log "Would copy ExecPlan template to $dst_execplan"
      fi
    else
      mkdir -p "$CODEX_HOME"
      if [[ "$EFFECTIVE_MODE" == "update" ]]; then
        cp "$src_execplan" "$dst_execplan"
        log "Replaced ExecPlan template at $dst_execplan (update mode)"
      else
        if [[ -f "$dst_execplan" ]] && cmp -s "$src_execplan" "$dst_execplan"; then
          vlog "ExecPlan template already up to date at $dst_execplan"
        else
          cp "$src_execplan" "$dst_execplan"
          log "Copied ExecPlan template to $dst_execplan"
        fi
      fi
    fi
  else
    vlog "No execplan.md found in script directory; skipping template copy"
  fi
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
  show_header
  CURRENT_PHASE=0

  next_phase "Resolve installation paths"
  resolve_scope_interactive

  next_phase "Prepare target directories"
  ensure_dirs

  next_phase "Backup existing installation (if present)"
  backup_existing

  next_phase "Copy Codex prompts and rules"
  copy_prompts_and_rules

  next_phase "Copy Python framework"
  copy_python_framework

  next_phase "Install Python dependencies"
  install_python_deps

  next_phase "Install Node-based tooling"
  install_node_tools

  next_phase "Configure codex config.toml"
  ensure_config

  next_phase "Update AGENTS.md"
  update_agents_md

  next_phase "Offer shell helpers"
  inject_shell_helpers

  next_phase "Verify installation"
  verify_install

  completion_msg
}

main "$@"
