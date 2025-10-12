#!/usr/bin/env bash
# AI-Assisted Workflows Codex CLI Uninstall Script
# Removes Codex-specific workflow assets while preserving user customisations

set -euo pipefail

SCRIPT_VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="/tmp/ai-workflows-codex-uninstall.log"

DRY_RUN=false
VERBOSE=false
TARGET_PATH=""
SCRIPTS_ROOT_OVERRIDE=""

CODEX_HOME=""
SCRIPTS_ROOT=""

show_usage() {
  cat <<'EOF'
AI-Assisted Workflows Codex Uninstaller

USAGE:
  ./uninstall.sh [TARGET_PATH] [OPTIONS]

ARGUMENTS:
  TARGET_PATH       Directory containing .codex/ to uninstall from (default: current directory)

OPTIONS:
  -h, --help        Show this help message
  -v, --verbose     Enable verbose output
  -n, --dry-run     Show what would be removed without making changes
  --scripts-root    Override the scripts root used during install (defaults to <CODEX_HOME>/scripts)

DESCRIPTION:
  The uninstaller removes the Codex prompts, rules, Python scripts, and node tooling
  that ship with AI-Assisted Workflows while preserving your .codex directory and
  any user-added content. Python dependency removal is interactive and optional.
EOF
}

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_verbose() {
  if [[ "$VERBOSE" == true ]]; then
    log "$@"
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
  fi
}

log_error() {
  echo "[ERROR] $*" | tee -a "$LOG_FILE" >&2
}

normalize_path() {
  local raw="$1"
  [[ "$raw" == "~" ]] && raw="$HOME"
  if [[ "$raw" == ~* ]]; then
    raw="${raw/#\~/$HOME}"
  fi
  if command -v realpath >/dev/null 2>&1; then
    realpath "$raw" 2>/dev/null || echo "$raw"
  else
    python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$raw" 2>/dev/null || echo "$raw"
  fi
}

parse_arguments() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        show_usage
        exit 0
        ;;
      -v|--verbose)
        VERBOSE=true
        shift
        ;;
      -n|--dry-run)
        DRY_RUN=true
        shift
        ;;
      --scripts-root)
        if [[ -n "${2:-}" ]]; then
          SCRIPTS_ROOT_OVERRIDE="$(normalize_path "$2")"
          shift 2
        else
          log_error "--scripts-root requires a value"
          exit 1
        fi
        ;;
      -* )
        log_error "Unknown option: $1"
        show_usage
        exit 1
        ;;
      *)
        if [[ -z "$TARGET_PATH" ]]; then
          TARGET_PATH="$1"
        else
          log_error "Multiple target paths specified"
          exit 1
        fi
        shift
        ;;
    esac
  done
}

resolve_paths() {
  [[ -z "$TARGET_PATH" ]] && TARGET_PATH="$(pwd)"

  if [[ "$TARGET_PATH" == */.codex ]]; then
    CODEX_HOME="$TARGET_PATH"
  else
    CODEX_HOME="$TARGET_PATH/.codex"
  fi

  if [[ ! -d "$CODEX_HOME" ]]; then
    log_error "No .codex directory found at: $CODEX_HOME"
    exit 1
  fi

  if [[ -n "$SCRIPTS_ROOT_OVERRIDE" ]]; then
    SCRIPTS_ROOT="$SCRIPTS_ROOT_OVERRIDE"
  else
    SCRIPTS_ROOT="$CODEX_HOME/scripts"
  fi

  if [[ ! -d "$SCRIPTS_ROOT" ]]; then
    log_verbose "Scripts root not found at $SCRIPTS_ROOT; script cleanup will be skipped"
    SCRIPTS_ROOT=""
  fi

  log "Codex home: $CODEX_HOME"
  [[ -n "$SCRIPTS_ROOT" ]] && log "Scripts root: $SCRIPTS_ROOT"
}

init_log() {
  echo "" > "$LOG_FILE"
  log "AI-Assisted Workflows Codex Uninstaller v$SCRIPT_VERSION"
}

verify_installation() {
  local matches=0
  if [[ -f "$CODEX_HOME/prompts/plan-solution.md" ]]; then
    ((matches++))
  fi
  if [[ -d "$SCRIPTS_ROOT" ]] && [[ -d "$SCRIPTS_ROOT/core" ]]; then
    ((matches++))
  fi
  if [[ -f "$CODEX_HOME/rules/global.codex.rules.md" ]]; then
    ((matches++))
  fi

  if [[ $matches -eq 0 ]]; then
    log_error "No AI-Assisted Workflows Codex components detected at $CODEX_HOME"
    exit 1
  fi
}

remove_prompt_files() {
  log "Checking for Codex prompt files..."
  if [[ ! -d "$CODEX_HOME/prompts" ]]; then
    log_verbose "No prompts directory found"
    return
  fi

  local prompts=(
    "add-code-precommit-checks.md"
    "analyze-architecture.md"
    "analyze-code-quality.md"
    "analyze-performance.md"
    "analyze-root-cause.md"
    "analyze-security.md"
    "apply-rule-set.md"
    "codify-codex-history.md"
    "create-project.md"
    "create-rule.md"
    "create-session-notes.md"
    "get-primer.md"
    "get-recent-context.md"
    "plan-refactor.md"
    "plan-solution.md"
    "plan-ux-prd.md"
    "setup-dev-monitoring.md"
    "setup-package-monitoring.md"
    "setup-serena-mcp.md"
    "todo-background.md"
    "todo-build-worktree.md"
  )

  local to_remove=()
  for prompt in "${prompts[@]}"; do
    [[ -f "$CODEX_HOME/prompts/$prompt" ]] && to_remove+=("$prompt")
  done

  if [[ ${#to_remove[@]} -eq 0 ]]; then
    log "No Codex prompt files found to remove"
    return
  fi

  echo "" && echo "Found ${#to_remove[@]} prompt files:"
  for file in "${to_remove[@]}"; do
    echo "  - prompts/$file"
  done
  echo ""

  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove ${#to_remove[@]} prompt files"
    return
  fi

  read -p "Remove these prompt files? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    local count=0
    for file in "${to_remove[@]}"; do
      if rm "$CODEX_HOME/prompts/$file" 2>/dev/null; then
        log_verbose "Removed prompt: $file"
        ((count++))
      else
        log_error "Failed to remove prompt: $file"
      fi
    done
    if [[ -d "$CODEX_HOME/prompts" ]] && [[ -z "$(ls -A "$CODEX_HOME/prompts")" ]]; then
      rmdir "$CODEX_HOME/prompts" 2>/dev/null && log_verbose "Removed empty prompts directory"
    fi
    log "Removed $count prompt files"
  else
    log "Skipped removing prompt files"
  fi
}

remove_rule_files() {
  log "Checking for Codex rule files..."
  if [[ ! -d "$CODEX_HOME/rules" ]]; then
    log_verbose "No rules directory found"
    return
  fi

  local rules=(
    "global.codex.rules.md"
    "minimal.intrusion.rules.md"
    "rapid.prototype.rules.md"
    "tdd.rules.md"
  )

  local to_remove=()
  for rule in "${rules[@]}"; do
    [[ -f "$CODEX_HOME/rules/$rule" ]] && to_remove+=("$rule")
  done

  if [[ ${#to_remove[@]} -eq 0 ]]; then
    log "No Codex rule files found to remove"
    return
  fi

  echo "" && echo "Found ${#to_remove[@]} rule files:"
  for file in "${to_remove[@]}"; do
    echo "  - rules/$file"
  done
  echo ""

  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove ${#to_remove[@]} rule files"
    return
  fi

  read -p "Remove these rule files? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    local count=0
    for file in "${to_remove[@]}"; do
      if rm "$CODEX_HOME/rules/$file" 2>/dev/null; then
        log_verbose "Removed rule: $file"
        ((count++))
      else
        log_error "Failed to remove rule: $file"
      fi
    done
    if [[ -d "$CODEX_HOME/rules" ]] && [[ -z "$(ls -A "$CODEX_HOME/rules")" ]]; then
      rmdir "$CODEX_HOME/rules" 2>/dev/null && log_verbose "Removed empty rules directory"
    fi
    log "Removed $count rule files"
  else
    log "Skipped removing rule files"
  fi
}

remove_script_directories() {
  if [[ -z "$SCRIPTS_ROOT" ]]; then
    return
  fi

  log "Checking for Codex Python framework scripts..."

  local subdirs=(analyzers config context core generators setup utils web_scraper)
  local to_remove=()
  for dir in "${subdirs[@]}"; do
    if [[ -d "$SCRIPTS_ROOT/$dir" ]]; then
      to_remove+=("$dir")
    fi
  done

  if [[ ${#to_remove[@]} -eq 0 ]]; then
    log "No managed scripts found in $SCRIPTS_ROOT"
    return
  fi

  echo "" && echo "Found ${#to_remove[@]} managed script directories under $SCRIPTS_ROOT:"
  for dir in "${to_remove[@]}"; do
    echo "  - $dir"
  done
  echo ""

  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove script directories from $SCRIPTS_ROOT"
    return
  fi

  read -p "Remove these script directories? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    local count=0
    for dir in "${to_remove[@]}"; do
      if rm -rf "$SCRIPTS_ROOT/$dir" 2>/dev/null; then
        log_verbose "Removed scripts: $dir"
        ((count++))
      else
        log_error "Failed to remove scripts: $dir"
      fi
    done
    find "$SCRIPTS_ROOT" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    if [[ -d "$SCRIPTS_ROOT" ]] && [[ -z "$(find "$SCRIPTS_ROOT" -type f -print -quit 2>/dev/null)" ]]; then
      rmdir "$SCRIPTS_ROOT" 2>/dev/null && log_verbose "Removed empty scripts root"
    fi
    log "Removed $count script directories"
  else
    log "Skipped removing script directories"
  fi
}

remove_eslint_bundle() {
  if [[ ! -d "$CODEX_HOME/eslint" ]]; then
    return
  fi
  log "Checking for local ESLint workspace..."
  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove $CODEX_HOME/eslint"
    return
  fi
  read -p "Remove Codex ESLint workspace? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$CODEX_HOME/eslint" 2>/dev/null && log "Removed ESLint workspace"
  else
    log "Skipped removing ESLint workspace"
  fi
}

remove_agents_section() {
  local agents_md="$CODEX_HOME/AGENTS.md"
  local marker="# AI-Assisted Workflows (Codex Global Rules)"

  if [[ ! -f "$agents_md" ]] || ! grep -q "$marker" "$agents_md"; then
    log_verbose "No Codex rules section found in AGENTS.md"
    return
  fi

  echo "" && echo "Found AI-Assisted Workflows Codex section in AGENTS.md"
  echo ""

  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove Codex section from AGENTS.md"
    return
  fi

  read -p "Remove the AI-Assisted Workflows section from AGENTS.md? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    local backup="$agents_md.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$agents_md" "$backup"
    log_verbose "Created backup: $(basename "$backup")"

    AGENTS_MD="$agents_md" SECTION_MARKER="$marker" python3 - <<'PY'
import os
from pathlib import Path

path = Path(os.environ["AGENTS_MD"])
marker = os.environ["SECTION_MARKER"]
text = path.read_text(encoding="utf-8")
idx = text.find(marker)
if idx == -1:
    raise SystemExit(0)
trimmed = text[:idx].rstrip()
if trimmed:
    trimmed += '\n'
path.write_text(trimmed, encoding="utf-8")
PY

    log "Removed Codex rules section from AGENTS.md"
    echo "Backup saved as: $(basename "$backup")"
  else
    log "Skipped removing AGENTS.md section"
  fi
}

remove_python_packages() {
  if [[ -z "$SCRIPTS_ROOT" ]]; then
    return
  fi

  local requirement_files=()
  [[ -f "$SCRIPTS_ROOT/setup/requirements.txt" ]] && requirement_files+=("$SCRIPTS_ROOT/setup/requirements.txt")
  [[ -f "$SCRIPTS_ROOT/setup/ci/requirements.txt" ]] && requirement_files+=("$SCRIPTS_ROOT/setup/ci/requirements.txt")

  if [[ ${#requirement_files[@]} -eq 0 ]]; then
    log_verbose "No requirements files found under scripts root"
    return
  fi

  local packages=()
  for req in "${requirement_files[@]}"; do
    while IFS= read -r line; do
      [[ -z "$line" || "$line" =~ ^[[:space:]]*# ]] && continue
      local pkg="${line%%[>=<]*}"
      pkg="${pkg// /}"
      [[ -n "$pkg" ]] && packages+=("$pkg")
    done < "$req"
  done

  if [[ ${#packages[@]} -eq 0 ]]; then
    return
  fi

  local unique=()
  declare -A seen=()
  for pkg in "${packages[@]}"; do
    if [[ -z "${seen[$pkg]:-}" ]]; then
      unique+=("$pkg")
      seen[$pkg]=1
    fi
  done
  packages=("${unique[@]}")

  local installed=()
  for pkg in "${packages[@]}"; do
    if python3 -m pip show "$pkg" &>/dev/null; then
      installed+=("$pkg")
    fi
  done

  if [[ ${#installed[@]} -eq 0 ]]; then
    log "No Codex-specific Python packages detected"
    return
  fi

  echo "" && echo "Codex Python packages that can be removed:"
  for pkg in "${installed[@]}"; do
    echo "  - $pkg"
  done
  echo ""

  if [[ "$DRY_RUN" == true ]]; then
    log "Would prompt to remove ${#installed[@]} Python packages"
    return
  fi

  local removed=0
  for pkg in "${installed[@]}"; do
    read -p "Remove Python package '$pkg'? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      if python3 -m pip uninstall -y "$pkg" &>/dev/null; then
        log_verbose "Removed Python package: $pkg"
        ((removed++))
      else
        log_error "Failed to remove Python package: $pkg"
      fi
    else
      log_verbose "Skipped Python package: $pkg"
    fi
  done

  if [[ $removed -gt 0 ]]; then
    log "Removed $removed Python packages"
  else
    log "No Python packages were removed"
  fi
}

remove_misc_files() {
  log "Cleaning up auxiliary Codex files..."
  local extras=("installation-log.txt")
  local to_remove=()
  for item in "${extras[@]}"; do
    if [[ -e "$CODEX_HOME/$item" ]]; then
      to_remove+=("$item")
    fi
  done

  if [[ ${#to_remove[@]} -eq 0 ]]; then
    log_verbose "No auxiliary Codex files to remove"
    return
  fi

  if [[ "$DRY_RUN" == true ]]; then
    log "Would remove auxiliary files: ${to_remove[*]}"
    return
  fi

  read -p "Remove auxiliary Codex files (${to_remove[*]})? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    for item in "${to_remove[@]}"; do
      rm -rf "$CODEX_HOME/$item" 2>/dev/null && log_verbose "Removed $item"
    done
    log "Removed auxiliary Codex files"
  else
    log "Skipped removing auxiliary files"
  fi
}

show_summary() {
  echo ""
  echo "🧹 Codex uninstall completed"
  echo "  Codex home: $CODEX_HOME"
  [[ -n "$SCRIPTS_ROOT" ]] && echo "  Scripts root: $SCRIPTS_ROOT"
  echo ""
  echo "Components processed:"
  echo "  ✓ Prompt files"
  echo "  ✓ Rule files"
  echo "  ✓ Python framework scripts"
  echo "  ✓ ESLint workspace"
  echo "  ✓ AGENTS.md Codex section"
  echo "  ✓ Auxiliary files"
  echo "  ✓ Python packages (interactive)"
  echo ""
  echo "Detailed log: $LOG_FILE"
}

main() {
  init_log
  parse_arguments "$@"
  resolve_paths
  verify_installation

  if [[ "$DRY_RUN" == true ]]; then
    echo "🔍 DRY RUN MODE - no changes will be made"
  fi

  echo ""
  echo "🧹 Codex Workflow Uninstaller"
  echo "============================"
  echo "This will remove AI-Assisted Workflows assets from: $CODEX_HOME"
  [[ -n "$SCRIPTS_ROOT" ]] && echo "Scripts root: $SCRIPTS_ROOT"
  echo ""

  if [[ "$DRY_RUN" != true ]]; then
    read -p "Continue with uninstall? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      log "Uninstall cancelled by user"
      echo "Cancelled."
      exit 0
    fi
  fi

  remove_prompt_files
  remove_rule_files
  remove_script_directories
  remove_eslint_bundle
  remove_agents_section
  remove_misc_files
  remove_python_packages

  if [[ "$DRY_RUN" != true ]]; then
    show_summary
  else
    echo "Dry run completed - no changes were made"
  fi
}

main "$@"
