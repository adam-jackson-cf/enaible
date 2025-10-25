# Purpose

Launch an autonomous Claude Code (or alternative CLI) session in the background, routing progress updates to a timestamped report file.

## Variables

### Required

- @USER_PROMPT = $1 — background task brief forwarded to the selected CLI

### Optional (derived from $ARGUMENTS)

- @MODEL_SELECTOR = --model — CLI/model selector (e.g., claude:model, codex:codex-medium); default claude:sonnet
- @REPORT_FILE = --report-file — destination report file (default ./.workspace/agents/background/background-report-<TIMESTAMP>.md)

### Derived (internal)

- (none)

## Instructions

- Capture the timestamp before creating files or launching processes to keep naming consistent.
- Initialize the report file (directory + header) prior to starting the background agent.
- Pass the `USER_PROMPT` exactly as supplied; do not modify unless prepending reporting instructions for CLIs lacking `--append-system-prompt`.
- Use `run_in_background=true` with the Bash tool when spawning the process.
- Record process ID, report path, and monitoring guidance in the final summary.

## Workflow

0. Auth preflight
   - Run `uv run --project tools/enaible enaible auth_check --cli <CLI> --report <REPORT_FILE>` using the parsed CLI from @MODEL_SELECTOR.
   - If the command exits non‑zero, write the message to the report and stop; do not prompt for login interactively inside the background task.
1. Prepare reporting directory
   - Run `mkdir -p ./.workspace/agents/background && test -w ./.workspace/agents/background`; exit immediately if the directory cannot be created or written because progress logs rely on it.
2. Parse inputs
   - Require `USER_PROMPT`; if missing, prompt the user and stop.
   - Split `MODEL_SELECTOR` on `:` to derive `CLI` (`claude`, `codex`, `opencode`, `qwen`, `gemini`) and model name.
3. Prepare reporting path
   - Compute `TIMESTAMP` and default `REPORT_FILE` path if not provided.
   - Create parent directories and initialize markdown header:
     ```
     # Background Task Report - <human-readable date>
     ## Task: <USER_PROMPT>
     ## Started: <date time>
     ```
4. Launch background process
   - Build command per CLI:
     - Claude:
       ```
       claude --model <model> \
         --output-format text \
         --dangerously-skip-permissions \
         --append-system-prompt "Report all progress and results to: <REPORT_FILE>. Use Write tool to append updates." \
         --print "<USER_PROMPT>"
       ```
     - Codex:
     - Use the `cdx-exec` helper. Default the model to `codex-medium` (override via `MODEL_SELECTOR`, e.g., `codex:codex-large`).
       For Codex, prepend reporting instructions to the prompt (no append-system-prompt flag):
       ```
       CDX_MODEL="${MODEL_NAME:-codex-medium}"
       ENHANCED_PROMPT="<USER_PROMPT> IMPORTANT: Report all progress and results to: <REPORT_FILE>. Use the Write tool to append updates."
       cdx-exec --model "$CDX_MODEL" "$ENHANCED_PROMPT"
       ```
     - OpenCode:
     - Use `opencode run` for headless execution. Default the model to `github-copilot/gpt-5-mini` (override via `MODEL_SELECTOR`, e.g., `opencode:github-copilot/gpt-5-codex`).
       OpenCode does not support append-system-prompt, so prepend reporting instructions to the prompt:
       ```
       OC_MODEL="${MODEL_NAME:-github-copilot/gpt-5-mini}"
       ENHANCED_PROMPT="<USER_PROMPT> IMPORTANT: Report all progress and results to: <REPORT_FILE>. Use the Write tool to append updates."
       opencode run --model "$OC_MODEL" \
         --print-logs \
         --log-level INFO \
         "$ENHANCED_PROMPT"
       ```
     - Qwen / Gemini: prepend reporting instructions to prompt and use `--yolo`.
   - Execute via Bash tool with `run_in_background=true`.
5. Configure monitoring
   - Capture process ID and background job handle.
   - Note how progress will be appended to `REPORT_FILE`.
6. Report launch status
   - Summarize CLI selected, model, background PID, and report path.
   - Provide instructions for checking progress (tail the report, inspect process).

## Output

```md
# RESULT

- Summary: Background task launched with <CLI> (<model>).

## PROCESS

- PID: <pid>
- Command: <full CLI invocation>

## REPORT

- File: <REPORT_FILE>
- Monitoring: `tail -f <REPORT_FILE>`

## NEXT STEPS

1. Review report for periodic updates.
2. Terminate background process when work is complete (`kill <pid>` if needed).
```

## Examples

```bash
# Default Claude Sonnet background task
/todo-background "Analyze the codebase for performance issues"

# Run with Claude Opus and custom report location
/todo-background "Refactor the authentication module" claude:opus ./reports/auth-refactor.md

# Launch Qwen with default report
/todo-background "Run security audit and create remediation plan" qwen
```
