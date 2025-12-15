#!/usr/bin/env bash
set -euo pipefail

show_help() {
  cat <<'USAGE'
Usage: setup-uv-ca.sh [OPTIONS]

Merges the system trust store with a corporate root certificate so uv/openssl-based
commands can trust both DigiCert (used by GitHub/Astral) and your organization.

Options:
  --corp-ca PATH   Explicit path to the corporate CA PEM. Defaults to the first
                   readable file among $CORP_CA_FILE, $SSL_CERT_FILE,
                   $REQUESTS_CA_BUNDLE, and $UV_HTTP_CA_BUNDLE.
  --output PATH    Destination path for the merged bundle. Defaults to
                   $HOME/.config/claude/corp-ca-bundle.pem.
  --print-exports  Print ready-to-source export commands pointing at the bundle.
  --exports-only   Skip the merge and only emit exports for the bundle path.
  -h, --help       Show this help message.
USAGE
}

log() {
  printf '[setup-uv-ca] %s\n' "$*"
}

error() {
  printf '\n[setup-uv-ca] ERROR: %s\n' "$*" >&2
  exit 1
}

abspath() {
  /usr/bin/env python3 - "$1" <<'PY'
import os
import sys
print(os.path.abspath(os.path.expanduser(sys.argv[1])))
PY
}

emit_exports() {
  local bundle_path="$1"
  cat <<EOF
export SSL_CERT_FILE="$bundle_path"
export REQUESTS_CA_BUNDLE="$bundle_path"
export UV_HTTP_CA_BUNDLE="$bundle_path"
export PIP_CERT="$bundle_path"
EOF
}

CORP_CA_FILE="${CORP_CA_FILE:-}"
OUTPUT_BUNDLE=""
PRINT_EXPORTS=0
EXPORTS_ONLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --corp-ca)
      [[ $# -ge 2 ]] || error "--corp-ca requires a path"
      CORP_CA_FILE="$2"
      shift 2
      ;;
    --output)
      [[ $# -ge 2 ]] || error "--output requires a path"
      OUTPUT_BUNDLE="$2"
      shift 2
      ;;
    --print-exports)
      PRINT_EXPORTS=1
      shift
      ;;
    --exports-only)
      EXPORTS_ONLY=1
      PRINT_EXPORTS=1
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      show_help
      error "Unknown argument: $1"
      ;;
  esac
done

if [[ -z "$OUTPUT_BUNDLE" ]]; then
  OUTPUT_BUNDLE="${UV_CA_BUNDLE_PATH:-$HOME/.config/claude/corp-ca-bundle.pem}"
fi
OUTPUT_BUNDLE="$(abspath "$OUTPUT_BUNDLE")"

if [[ "$EXPORTS_ONLY" -eq 1 ]]; then
  [[ -f "$OUTPUT_BUNDLE" ]] || error "Bundle not found at $OUTPUT_BUNDLE. Run without --exports-only first."
  log "Emitting exports for existing bundle: $OUTPUT_BUNDLE"
  emit_exports "$OUTPUT_BUNDLE"
  exit 0
fi

if [[ -z "$CORP_CA_FILE" || ! -f "$CORP_CA_FILE" ]]; then
  for candidate in "${SSL_CERT_FILE:-}" "${REQUESTS_CA_BUNDLE:-}" "${UV_HTTP_CA_BUNDLE:-}"; do
    if [[ -n "$candidate" && -f "$candidate" ]]; then
      CORP_CA_FILE="$candidate"
      break
    fi
  done
fi

[[ -n "$CORP_CA_FILE" ]] || error "Unable to locate a corporate CA file. Pass --corp-ca /path/to/cert.pem"
[[ -f "$CORP_CA_FILE" ]] || error "Corporate CA file not found: $CORP_CA_FILE"
CORP_CA_FILE="$(abspath "$CORP_CA_FILE")"

log "Using corporate CA: $CORP_CA_FILE"

SYSTEM_CA_FILE=$(SSL_CERT_FILE= REQUESTS_CA_BUNDLE= UV_HTTP_CA_BUNDLE= python3 - <<'PY'
import os
import ssl
paths = ssl.get_default_verify_paths()
for attr in ("cafile", "openssl_cafile"):
    candidate = getattr(paths, attr, None)
    if candidate and os.path.exists(candidate):
        print(candidate)
        raise SystemExit(0)
raise SystemExit(1)
PY
) || true

if [[ -z "$SYSTEM_CA_FILE" ]]; then
  if [[ -f /etc/ssl/cert.pem ]]; then
    SYSTEM_CA_FILE=/etc/ssl/cert.pem
  else
    error "System CA bundle not found automatically. Set SYSTEM_CA_FILE=/path before running."
  fi
fi

if [[ "$SYSTEM_CA_FILE" == "$CORP_CA_FILE" ]]; then
  if [[ -f /etc/ssl/cert.pem && /etc/ssl/cert.pem != "$CORP_CA_FILE" ]]; then
    SYSTEM_CA_FILE=/etc/ssl/cert.pem
  else
    error "System CA path resolved to the same file as the corporate CA. Unset SSL_CERT_FILE/REQUESTS_CA_BUNDLE/UV_HTTP_CA_BUNDLE or pass --corp-ca explicitly so both chains can be merged."
  fi
fi

log "Using system CA: $SYSTEM_CA_FILE"

mkdir -p "$(dirname "$OUTPUT_BUNDLE")"
TEMP_BUNDLE="$(mktemp "${OUTPUT_BUNDLE}.XXXXXX")"

cat "$SYSTEM_CA_FILE" > "$TEMP_BUNDLE"
printf '\n' >> "$TEMP_BUNDLE"
cat "$CORP_CA_FILE" >> "$TEMP_BUNDLE"

chmod 0644 "$TEMP_BUNDLE"
mv "$TEMP_BUNDLE" "$OUTPUT_BUNDLE"

log "Merged CA bundle written to $OUTPUT_BUNDLE"

cat <<EOF

Add the following exports to your shell profile (e.g. ~/.zshrc) so uv, curl, and
requests trust both chains:

export SSL_CERT_FILE="$OUTPUT_BUNDLE"
export REQUESTS_CA_BUNDLE="$OUTPUT_BUNDLE"
export UV_HTTP_CA_BUNDLE="$OUTPUT_BUNDLE"
export PIP_CERT="$OUTPUT_BUNDLE"

Then restart your shell or run 'source ~/.zshrc' before rerunning:
uv run --project tools/enaible enaible install copilot --mode fresh --scope user

Optional (applies only to uv):
uv config set http.cabundle "$OUTPUT_BUNDLE"

To update the current shell immediately (without editing your profile):
  source <(./scripts/setup-uv-ca.sh --exports-only --print-exports)
  # include --output /custom/path if you changed the bundle location

EOF

if [[ "$PRINT_EXPORTS" -eq 1 ]]; then
  printf '\n# Export commands for immediate use:\n'
  emit_exports "$OUTPUT_BUNDLE"
fi
