# Purpose

Launch an autonomous Claude Code (or alternative CLI) session in the background, routing progress updates to a timestamped report file.

## Variables

- `USER_PROMPT` ← $1 required.

### Optional derived from $ARGUMENTS:

- `MODEL_SELECTOR` = `--model` ← (`claude:model`, `codex:codex-medium`, `opencode:provider/model`, `qwen`, `gemini`); default `claude:sonnet`.
- `REPORT_FILE` ← `--report` ← defaults to `./.enaible/agents/background/background-report-<TIMESTAMP>.md`.

## Instructions

- Capture the timestamp before creating files or launching processes to keep naming consistent.
- Initialize the report file (directory + header) prior to starting the background agent.
- Pass the `USER_PROMPT` exactly as supplied; do not modify unless prepending reporting instructions for CLIs lacking `--append-system-prompt`.
- Use `run_in_background=true` with the Bash tool when spawning the process.
- Record process ID, report path, and monitoring guidance in the final summary.

## Workflow

1. **Auth Preflight**

   - Verify credentials without triggering interactive prompts:

     ```bash
     uv run --project tools/enaible enaible auth_check --cli <CLI> --report <REPORT_FILE>
     ```

   - If the command exits non-zero, log the message to the report and stop.

2. **Prepare Reporting Directory**

   - Ensure the background reports directory exists and is writable:

     ```bash
     mkdir -p ./.workspace/agents/background && test -w ./.enaible/agents/background
     ```

   - Abort if the directory cannot be created or written to.

3. **Parse Inputs**

   - Require `USER_PROMPT`; prompt the user and abort when missing.
   - Split `MODEL_SELECTOR` on `:` to derive the CLI (`claude`, `codex`, `opencode`, `qwen`, `gemini`) and model name.

4. **Prepare Reporting Path**

   - Compute `TIMESTAMP`, derive default `REPORT_FILE` when not provided, create parent folders, and initialize the markdown header:

     ```markdown
     # Background Task Report - <human-readable date>

     ## Task: <USER_PROMPT>

     ## Started: <date time>
     ```

5. **Launch Background Process**

   - Assemble the command per CLI and ensure updates are routed to `<REPORT_FILE>`:

     - **Claude**

       ```bash
       claude --model <model> \
         --output-format text \
         --dangerously-skip-permissions \
         --append-system-prompt "Report all progress and results to: <REPORT_FILE>. Use Write tool to append updates." \
         --print "<USER_PROMPT>"
       ```

     - **Codex** (use `cdx-exec`; prepend reporting instructions instead of append-system prompt)

       ```bash
       CDX_MODEL="${MODEL_NAME:-codex-medium}"
       ENHANCED_PROMPT="<USER_PROMPT> IMPORTANT: Report all progress and results to: <REPORT_FILE>. Use the Write tool to append updates."
       cdx-exec --model `CDX_MODEL` `ENHANCED_PROMPT`
       ```

     - **OpenCode** (headless execution with reporting instructions prepended)

       ```bash
       OC_MODEL="${MODEL_NAME:-github-copilot/gpt-5-mini}"
       ENHANCED_PROMPT="<USER_PROMPT> IMPORTANT: Report all progress and results to: <REPORT_FILE>. Use the Write tool to append updates."
       opencode run --model `OC_MODEL` \
         --print-logs \
         --log-level INFO \
         `ENHANCED_PROMPT`
       ```

     - **Qwen / Gemini**
       - Prepend reporting instructions and run with `--yolo` as required by the CLI.

   - Execute the chosen command via the Bash tool with `run_in_background=true`.

6. **Configure Monitoring**

   - Capture the background process ID and job handle.
   - Note how progress will be appended to `<REPORT_FILE>` for downstream monitoring.

7. **Report Launch Status**
   - Summarize the selected CLI/model, background PID, and report path.
   - Provide quick monitoring guidance (e.g., `tail -f <REPORT_FILE>` or inspect process commands).

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
/todo-background "Refactor the authentication module" --model claude:opus --report ./reports/auth-refactor.md

# Launch Qwen with default report
/todo-background "Run security audit and create remediation plan" --model qwen
```
