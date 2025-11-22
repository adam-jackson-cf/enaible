#!/usr/bin/env bash
set -euo pipefail

# Test matrix runner for /todo-background background launch patterns across CLIs.
# Valid modes: claude, codex, qwen, gemini, all
# Note: opencode support was removed

# Resolve repo root from fixtures directory: shared/tests/integration/fixtures -> repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/../../../.. && pwd)"
REPORT_DIR="$REPO_ROOT/.workspace/agents/background"
mkdir -p "$REPORT_DIR"

exists() { command -v "$1" >/dev/null 2>&1; }

print_header() {
  echo ""
  echo "────────────────────────────────────────────────────────"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Testing mode: $1"
  echo "────────────────────────────────────────────────────────"
}

run_mode() {
  local mode="$1"
  print_header "$mode"

  local ts ack report pid enhanced user_prompt
  ts=$(date +"%A_%H_%M_%S")
  report="$REPORT_DIR/background-report-${ts}.md"
  ack="ACK-${mode}-${ts}"

  # Initialize report header
  {
    echo "# Background Task Report - $(date)"
    echo "## Task: Test $mode background run"
    echo "## Started: $(date)"
    echo
  } > "$report"

  # Auth preflight for the selected CLI mode
  local fixture_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  local auth_script="$fixture_dir/check-ai-cli-auth.sh"
  if [[ -x "$auth_script" ]]; then
    if ! "$auth_script" "$mode" --report "$report"; then
      echo "AUTH CHECK FAILED for $mode — skipping launch. See report: $report"
      tail -n 10 "$report" || true
      return 0
    fi
  fi

  user_prompt="First, append a single line '${ack}' to the report file immediately, then stop."

  case "$mode" in
    claude)
      if ! exists claude; then echo "SKIP: claude CLI not found"; return 0; fi
      set +e
      claude --model sonnet \
        --output-format text \
        --dangerously-skip-permissions \
        --append-system-prompt "Report all progress and results to: $report. Use Write tool to append updates." \
        --print "$user_prompt" &
      pid=$!
      set -e
      ;;
    codex)
      if exists cdx-exec; then
        enhanced="$user_prompt IMPORTANT: Report all progress and results to: $report using the Write tool to append updates."
        set +e
        cdx-exec --model 'codex-medium' "$enhanced" &
        pid=$!
        set -e
      elif exists codex; then
        enhanced="$user_prompt IMPORTANT: Report all progress and results to: $report using the Write tool to append updates."
        set +e
        codex exec --model 'codex-medium' --sandbox workspace-write --config 'sandbox_workspace_write.network_access=true' "$enhanced" &
        pid=$!
        set -e
      else
        echo "SKIP: codex CLI not found"; return 0
      fi
      ;;
    qwen)
      if ! exists qwen; then echo "SKIP: qwen CLI not found"; return 0; fi
      enhanced="$user_prompt IMPORTANT: Report all progress and results to: $report using the Write tool to append updates."
      set +e
      qwen --yolo --prompt "$enhanced" &
      pid=$!
      set -e
      ;;
    gemini)
      if ! exists gemini; then echo "SKIP: gemini CLI not found"; return 0; fi
      enhanced="$user_prompt IMPORTANT: Report all progress and results to: $report using the Write tool to append updates."
      set +e
      gemini --yolo --prompt "$enhanced" &
      pid=$!
      set -e
      ;;
    *)
      echo "Unknown mode: $mode"; return 2 ;;
  esac

  echo "Launched $mode with PID $pid"
  echo "Report file: $report"

  # Wait briefly for agent to write
  sleep 25

  # Assertions
  if [[ -f "$report" ]]; then
    echo "Report exists: $report"
  else
    echo "ERROR: Report file not created: $report"
  fi

  if command -v rg >/dev/null 2>&1 && rg -q --fixed-strings "$ack" "$report"; then
    echo "SUCCESS: Found ACK line: $ack"
  else
    echo "WARN: ACK line not detected yet: $ack"
  fi

  # Cleanup background process if still running
  if ps -p "$pid" >/dev/null 2>&1; then
    kill "$pid" >/dev/null 2>&1 || true
    sleep 1
    if ps -p "$pid" >/dev/null 2>&1; then
      echo "INFO: Forcibly terminating PID $pid"
      kill -9 "$pid" >/dev/null 2>&1 || true
    fi
  fi

  # Preview tail of report
  echo "--- tail of report ---"
  tail -n 20 "$report" || true
  echo "-----------------------"
}

main() {
  local modes=("$@")
  if [[ ${#modes[@]} -eq 0 || "${modes[0]}" == "all" ]]; then
    modes=(claude codex qwen gemini)
  fi
  for m in "${modes[@]}"; do
    run_mode "$m"
  done
}

main "$@"
