#!/usr/bin/env bash
set -euo pipefail

BRANCH=$(git rev-parse --abbrev-ref HEAD)
REPO_ROOT=$(git rev-parse --show-toplevel)
PROJECT_DIR="$REPO_ROOT"
INSTALL_URL="https://raw.githubusercontent.com/adam-jackson-cf/enaible/${BRANCH}/scripts/install.sh"

log() {
  printf '[reset] %s\n' "$*"
}

cleanup_zshrc() {
  local zshrc="$HOME/.zshrc"
  if [[ -f "$zshrc" ]]; then
    local backup="${zshrc}.tls-backup-$(date -u +%Y%m%dT%H%M%SZ)"
    cp "$zshrc" "$backup"
    log "Backed up ~/.zshrc to ${backup}"
    grep -vE '^(export\s+)?(SSL_CERT_FILE|REQUESTS_CA_BUNDLE|UV_HTTP_CA_BUNDLE|PIP_CERT)=' "$backup" > "$zshrc"
    log "Removed TLS override variables from ~/.zshrc"
  else
    log "~/.zshrc not found; skipping TLS var cleanup"
  fi
}

remove_workspace() {
  if [[ -d "$HOME/.enaible" ]]; then
    rm -rf "$HOME/.enaible"
    log "Removed ~/.enaible"
  else
    log "~/.enaible not present"
  fi
}

uninstall_pip_deps() {
  local pybin
  pybin=$(command -v python3 || true)
  if [[ -z "$pybin" ]]; then
    log "python3 not found; skipping pip uninstall"
    return
  fi
  log "Uninstalling pip dependencies (lizard, semgrep, ruff, detect-secrets)"
  "$pybin" -m pip uninstall -y lizard semgrep ruff detect-secrets >/dev/null 2>&1 || true
}

uninstall_npm_deps() {
  if ! command -v npm >/dev/null 2>&1; then
    log "npm not found; skipping npm uninstall"
    return
  fi
  log "Uninstalling npm globals (jscpd, eslint + plugins)"
  npm uninstall -g jscpd eslint @typescript-eslint/parser eslint-plugin-react eslint-plugin-import eslint-plugin-vue >/dev/null 2>&1 || true
}

install_pip_deps() {
  local pybin
  pybin=$(command -v python3 || true)
  if [[ -z "$pybin" ]]; then
    log "python3 not found; cannot install pip dependencies"
    return
  fi
  log "Installing pip dependencies (lizard, semgrep, ruff, detect-secrets)"
  "$pybin" -m pip install --upgrade lizard semgrep ruff detect-secrets >/dev/null
}

install_npm_deps() {
  if ! command -v npm >/dev/null 2>&1; then
    log "npm not found; cannot install npm dependencies"
    return
  fi
  log "Installing npm globals (jscpd, eslint + plugins)"
  npm install -g jscpd eslint @typescript-eslint/parser eslint-plugin-react eslint-plugin-import eslint-plugin-vue >/dev/null
}

run_installer() {
  if [[ ! -d "$PROJECT_DIR" ]]; then
    log "Project directory $PROJECT_DIR not found" >&2
    exit 1
  fi
  log "Running installer from $INSTALL_URL targeting $PROJECT_DIR"
  curl -fsSL "$INSTALL_URL" | bash -s -- --systems claude-code --scope project --project "$PROJECT_DIR" --ref "$BRANCH"
}

run_install_phase() {
  local label="$1"
  log "$label"
  if run_installer; then
    log "$label succeeded"
    return 0
  else
    local status=$?
    log "$label failed (exit $status)"
    return $status
  fi
}

cleanup_zshrc
remove_workspace
uninstall_pip_deps
uninstall_npm_deps
run_install_phase "Running baseline install without analyzer dependencies to verify skip warnings"
install_pip_deps
install_npm_deps
run_install_phase "Running installer after installing analyzer dependencies"
