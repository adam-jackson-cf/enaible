#!/usr/bin/env bash
# Enaible bootstrap installer (macOS/Linux)

set -euo pipefail

DEFAULT_REPO_URL="https://github.com/adam-jackson-cf/enaible"
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

prompt_for_systems() {
    log "Select systems to install (space-separated numbers, e.g., '1 2' for codex and claude-code):"
    echo "  1) codex"
    echo "  2) claude-code"
    echo "  3) copilot"
    echo "  4) cursor"
    echo "  5) gemini"
    echo "  6) antigravity"

    local selected_systems=""
    while [[ -z "$selected_systems" ]]; do
        printf "Enter selection (required): "
        read -r selection

        local systems=()
        for num in $selection; do
            case "$num" in
                1) systems+=("codex") ;;
                2) systems+=("claude-code") ;;
                3) systems+=("copilot") ;;
                4) systems+=("cursor") ;;
                5) systems+=("gemini") ;;
                6) systems+=("antigravity") ;;
                *) log "Invalid selection: $num" ;;
            esac
        done

        if [[ ${#systems[@]} -gt 0 ]]; then
            selected_systems=$(IFS=,; echo "${systems[*]}")
        else
            log "ERROR: You must select at least one system"
        fi
    done

    SYSTEM_ARG="$selected_systems"
    log "Selected systems: $selected_systems"
}

prompt_for_scope() {
    log "Select installation scope:"
    echo "  1) user    - Install to user profile only (~/.config)"
    echo "  2) project - Install to current/specified project only"
    echo "  3) both    - Install to both user and project"

    printf "Enter selection [1]: "
    read -r selection

    case "${selection:-1}" in
        1) SCOPE="user" ;;
        2) SCOPE="project" ;;
        3) SCOPE="both" ;;
        *)
            log "Invalid selection, defaulting to 'user'"
            SCOPE="user"
            ;;
    esac

    log "Selected scope: $SCOPE"
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
  --systems LIST      Comma-separated systems to install (will prompt if not provided)
                      Available: codex,claude-code,copilot,cursor,gemini,antigravity
  --scope MODE        user|project|both (will prompt if not provided, default: user)
  --project PATH      Project repo path when installing with project or both scopes
  --repo-url URL      Git repo to clone (default: https://github.com/adam-jackson-cf/enaible)
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
    local systems_from_flag=false
    local scope_from_flag=false

    for arg in "$@"; do
        [[ "$arg" == "--systems" ]] && systems_from_flag=true
        [[ "$arg" == "--scope" ]] && scope_from_flag=true
    done

    parse_args "$@"

    if ! $systems_from_flag; then
        prompt_for_systems
    fi

    if ! $scope_from_flag; then
        prompt_for_scope
    fi

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
