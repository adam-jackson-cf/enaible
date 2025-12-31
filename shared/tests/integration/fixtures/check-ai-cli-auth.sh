#!/usr/bin/env bash
set -euo pipefail

# Auth preflight for AI CLIs used by todo-background
# Usage: shared/tests/integration/fixtures/check-ai-cli-auth.sh <claude|codex|qwen|gemini> [--report <path>]
# Note: opencode support was removed

REPORT=""

usage() {
  echo "Usage: $0 <claude|codex|qwen|gemini> [--report <path>]" >&2
}

exists() { command -v "$1" >/dev/null 2>&1; }

append_report() {
  local msg="$1"
  if [[ -n "$REPORT" ]]; then
    { echo "$msg"; } >> "$REPORT" || true
  fi
  echo "$msg"
}

if [[ $# -lt 1 ]]; then usage; exit 2; fi

CLI="$1"; shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --report) REPORT=${2:-}; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

case "$CLI" in
  claude)
    if ! exists claude; then append_report "[AUTH] Claude CLI not found (command 'claude' missing)."; exit 1; fi
    if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then append_report "[AUTH] Claude: OK (ANTHROPIC_API_KEY present)."; exit 0; else append_report "[AUTH] Claude: missing ANTHROPIC_API_KEY. Export it or configure the CLI before continuing."; exit 1; fi
    ;;
  codex)
    if ! exists codex && ! exists cdx-exec; then append_report "[AUTH] Codex CLI not found (commands 'codex'/'cdx-exec' missing)."; exit 1; fi
    if [[ -n "${OPENAI_API_KEY:-}" ]]; then append_report "[AUTH] Codex: OK (OPENAI_API_KEY present)."; exit 0; else append_report "[AUTH] Codex: missing OPENAI_API_KEY. Export it before continuing."; exit 1; fi
    ;;
  qwen)
    if ! exists qwen; then append_report "[AUTH] Qwen CLI not found (command 'qwen' missing)."; exit 1; fi
    if [[ -n "${DASHSCOPE_API_KEY:-}" || -n "${QWEN_API_KEY:-}" ]]; then append_report "[AUTH] Qwen: OK (API key present)."; exit 0; else append_report "[AUTH] Qwen: missing DASHSCOPE_API_KEY (or QWEN_API_KEY). Export it or run the CLI login before continuing."; exit 1; fi
    ;;
  gemini)
    if ! exists gemini; then append_report "[AUTH] Gemini CLI not found (command 'gemini' missing)."; exit 1; fi
    cred_file_default="$HOME/.config/gcloud/application_default_credentials.json"
    if [[ -n "${GOOGLE_API_KEY:-}" || -n "${GEMINI_API_KEY:-}" || -n "${GOOGLE_APPLICATION_CREDENTIALS:-}" && -f "${GOOGLE_APPLICATION_CREDENTIALS}" || -f "$cred_file_default" ]]; then
      append_report "[AUTH] Gemini: OK (API key or Google ADC present)."; exit 0
    else
      append_report "[AUTH] Gemini: missing GOOGLE_API_KEY/GEMINI_API_KEY and no Google ADC found. Set an API key or run 'gcloud auth application-default login'."; exit 1
    fi
    ;;
  *) echo "Unknown CLI: $CLI" >&2; usage; exit 2 ;;
esac
