#!/usr/bin/env bash
# Enaible bootstrap installer (macOS/Linux)

set -euo pipefail

DEFAULT_REPO_URL="https://github.com/adam-versed/ai-assisted-workflows.git"
DEFAULT_CLONE_DIR="${HOME}/.enaible/sources/ai-assisted-workflows"
DEFAULT_SYSTEMS="codex,claude-code"
DEFAULT_SCOPE="user"
DEFAULT_REF="main"
SESSION_DIR="${HOME}/.enaible/install-sessions"

REPO_URL="$DEFAULT_REPO_URL"
CLONE_DIR="$DEFAULT_CLONE_DIR"
SYSTEM_ARG="$DEFAULT_SYSTEMS"
SCOPE="$DEFAULT_SCOPE"
PROJECT_PATH=""
REF="$DEFAULT_REF"
DRY_RUN=false

log() {
    printf '[%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*"
}

die() {
    log "ERROR: $*"
    exit 1
}

ensure_path_entry() {
    case ":${PATH}:" in
        *:"${HOME}/.local/bin":*) ;;
        *) export PATH="${HOME}/.local/bin:${PATH}";;
    esac
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --repo-url)
                REPO_URL="${2:-$REPO_URL}"; shift;
                ;;
            --clone-dir)
                CLONE_DIR="${2:-$CLONE_DIR}"; shift;
                ;;
            --systems)
                SYSTEM_ARG="${2:-$SYSTEM_ARG}"; shift;
                ;;
            --scope)
                SCOPE="${2:-$SCOPE}"; shift;
                ;;
            --project)
                PROJECT_PATH="${2:-}"; shift;
                ;;
            --ref)
                REF="${2:-$REF}"; shift;
                ;;
            --dry-run)
                DRY_RUN=true
                ;;
            --help|-h)
                cat <<'USAGE'
Usage: scripts/install.sh [options]

Options:
  --systems LIST      Comma-separated systems to install (default: codex,claude-code)
  --scope MODE        user|project|both (default: user)
  --project PATH      Project repo path when installing with project or both scopes
  --repo-url URL      Git repo to clone (default: official)
  --clone-dir PATH    Cache directory for the repo clone (default: ~/.enaible/sources/...)
  --ref REF           Git ref/tag/branch to checkout (default: main)
  --dry-run           Print actions without executing
  --help              Show this help
USAGE
                exit 0
                ;;
            *)
                die "Unknown option: $1"
                ;;
        esac
        shift || true
    done
}

run_cmd() {
    if $DRY_RUN; then
        log "DRY-RUN: $*"
    else
        "$@"
    fi
}

run_with_repo_env() {
    if $DRY_RUN; then
        log "DRY-RUN: ENAIBLE_REPO_ROOT=${CLONE_DIR} $*"
    else
        ENAIBLE_REPO_ROOT="$CLONE_DIR" "$@"
    fi
}

parse_systems() {
    IFS=',' read -r -a SYSTEMS <<<"${SYSTEM_ARG// /}"
    local filtered=()
    for system in "${SYSTEMS[@]}"; do
        [[ -n "$system" ]] && filtered+=("$system")
    done
    SYSTEMS=("${filtered[@]}")
    if [[ ${#SYSTEMS[@]} -eq 0 ]]; then
        die "No systems specified"
    fi
}

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"
}

ensure_clone() {
    local dir="$CLONE_DIR"
    mkdir -p "$(dirname "$dir")"
    if [[ -d "$dir/.git" ]]; then
        log "Updating existing clone at $dir"
        run_cmd git -C "$dir" fetch --all --prune
        run_cmd git -C "$dir" checkout "$REF"
        run_cmd git -C "$dir" pull --rebase --autostash origin "$REF"
    else
        log "Cloning $REPO_URL to $dir"
        run_cmd git clone --branch "$REF" "$REPO_URL" "$dir"
    fi
}

install_cli() {
    log "Installing Enaible CLI via uv tool install"
    run_with_repo_env uv tool install --from "$CLONE_DIR/tools/enaible" enaible
}

install_scope() {
    local scope="$1"
    local target="$2"
    if [[ "$scope" == "project" && ! -d "$target" ]]; then
        die "Project scope requested but target '$target' does not exist"
    fi
    for system in "${SYSTEMS[@]}"; do
        log "Installing system '$system' (scope=$scope)"
        local args=(uv run --project "$CLONE_DIR/tools/enaible" enaible install "$system" --mode sync --scope "$scope" --no-install-cli)
        if [[ "$scope" == "project" ]]; then
            args+=(--target "$target")
        fi
        run_with_repo_env "${args[@]}"
    done
}

resolve_project_path() {
    if [[ -n "$PROJECT_PATH" ]]; then
        [[ -d "$PROJECT_PATH" ]] || die "Provided project path '$PROJECT_PATH' does not exist"
        return
    fi
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        PROJECT_PATH="$(git rev-parse --show-toplevel)"
        log "Detected project at $PROJECT_PATH"
    else
        die "Project scope requested but --project not provided and no git repo detected"
    fi
}

write_session_note() {
    mkdir -p "$SESSION_DIR"
    local file="$SESSION_DIR/session-$(date -u +%Y%m%dT%H%M%SZ).md"
    {
        echo "# Enaible bootstrap session"
        echo "- Repo URL: $REPO_URL"
        echo "- Clone dir: $CLONE_DIR"
        echo "- Systems: ${SYSTEMS[*]}"
        echo "- Scope: $SCOPE"
        if [[ -n "$PROJECT_PATH" ]]; then
            echo "- Project: $PROJECT_PATH"
        fi
        echo "- Dry run: $DRY_RUN"
    } >"$file"
    log "Session log saved to $file"
}

main() {
    parse_args "$@"
    parse_systems
    ensure_path_entry
    require_cmd git
    require_cmd python3
    require_cmd uv

    ensure_clone
    install_cli

    case "$SCOPE" in
        user)
            install_scope "user" ""
            ;;
        project)
            resolve_project_path
            install_scope "project" "$PROJECT_PATH"
            ;;
        both)
            resolve_project_path
            install_scope "user" ""
            install_scope "project" "$PROJECT_PATH"
            ;;
        *)
            die "Unknown scope '$SCOPE'"
            ;;
    esac

    write_session_note
    log "Bootstrap complete. Ensure ${HOME}/.local/bin is on your PATH for future shells."
}

main "$@"
