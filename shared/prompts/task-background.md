# Purpose

Run a single CLI workflow inside a named tmux session so it can keep working in the background while progress is logged to a timestamped report file.

## Variables

### Required

- @USER_PROMPT = $1 — first CLI argument; background task brief forwarded to Codex.

### Optional (derived from @ARGUMENTS)

- @MODEL_NAME = --model — model identifier (default gpt-5.2-codex).
- @REASONING = --reasoning — reasoning effort (default medium; valid minimal|low|medium|high|xhigh).
- @REPORT_FILE = --report-file — destination report file (default ./.enaible/agents/background/background-report-<TIMESTAMP>.md).

### Derived (internal)

- @SESSION_NAME — unique tmux session name for this background task
- @TIMESTAMP — UTC timestamp for file naming and session identification
- @TASK_LABEL — human-friendly label used in session + report names
- @PROCESS_ID — PID of the tmux pane running Codex

## Instructions

- Capture a timestamp before creating directories or files so report names, tmux sessions, and logs stay aligned.
- Create the report directory and header before launching Codex to guarantee every background run has a writable log.
- Always launch the selected CLI inside a dedicated tmux session.
- Record the tmux session name, model, reasoning effort, PID, and report path so operators can monitor or terminate the run later.
- Do not switch models or reasoning effort during preflight; if the selected CLI check fails, exit.
- Use `bash -lc` inside tmux so the CLI runs with the expected shell environment and working directory.

## Workflow

0. CLI preflight
   - Determine the CLI to check based on @MODEL_NAME and run a one-line “hello world” prompt to verify both CLI presence and auth:
     - Codex models (gpt-5._ / gpt-5._-codex / gpt-5._-codex-_):
       `codex exec --model @MODEL_NAME --config model_reasoning_effort="@REASONING" "Hello world"`
   - Claude models (opus, sonnet, haiku):
     `claude --model @MODEL_NAME -p "Hello world"`
   - Gemini models (gemini-2.5-pro, gemini-2.5-flash, gemini-3-pro, gemini-3-flash):
     `gemini --model @MODEL_NAME -p "Hello world"`
   - If the CLI command fails or returns an auth error, report it and exit without launching the background task.

1. Prepare reporting directory
   - Resolve the project root and ensure the reporting directory exists and is writable:
     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     mkdir -p "$PROJECT_ROOT/.enaible/agents/background"
     test -w "$PROJECT_ROOT/.enaible/agents/background"
     ```
   - Abort immediately if the directory cannot be created or is not writable.

2. Parse inputs
   - Require @USER_PROMPT; if missing, prompt the operator and stop.
   - Default @MODEL_NAME to `gpt-5.2-codex` when the selector is absent.
   - Default @REASONING to `medium`. Validate it is one of `minimal`, `low`, `medium`, `high`, `xhigh`.
   - Use the following lists to pick a random adjective + noun for @TASK_LABEL:

     ```
     const ADJECTIVES = [
       'amber',
       'brave',
       'calm',
       'clever',
       'ember',
       'frost',
       'gentle',
       'golden',
       'hidden',
       'iron',
       'juniper',
       'lunar',
       'mellow',
       'navy',
       'olive',
       'quiet',
       'rapid',
       'silver',
       'solid',
       'tender',
       'ultra',
       'vivid',
       'wild',
       'young',
     ];

     const NOUNS = [
       'badger',
       'beacon',
       'canyon',
       'cedar',
       'comet',
       'falcon',
       'forest',
       'harbor',
       'meadow',
       'mountain',
       'nebula',
       'ocean',
       'orchard',
       'pine',
       'raven',
       'river',
       'shadow',
       'signal',
       'summit',
       'thunder',
       'valley',
       'willow',
       'zephyr',
       'mesa',
     ];
     ```

   - Pick one adjective and one noun at random and set `@TASK_LABEL="<adjective>-<noun>"`.

3. Prepare reporting path
   - Compute @TIMESTAMP and @SESSION_NAME, then the default @REPORT_FILE if none was provided; ensure @REPORT_FILE is absolute:
     ```bash
     TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
     SESSION_NAME="bg-${TASK_LABEL}-${TIMESTAMP}"
     REPORT_FILE="@REPORT_FILE"
     if [ -z "$REPORT_FILE" ]; then
       REPORT_FILE="$PROJECT_ROOT/.enaible/agents/background/background-report-${TASK_LABEL}-${TIMESTAMP}.md"
     elif [ "${REPORT_FILE#/}" = "$REPORT_FILE" ]; then
       REPORT_FILE="$PROJECT_ROOT/$REPORT_FILE"
     fi
     ```
   - Create parent directories and initialize the markdown header:
     ```
     # Background Task Report - <human-readable date>
     ## Task: @USER_PROMPT
     ## Session: @SESSION_NAME
     ## Started: <date time>
     ## Monitor
     - tmux attach -t @SESSION_NAME
     - tmux capture-pane -p -S -200 -t @SESSION_NAME
     - tmux kill-session -t @SESSION_NAME
     - tail -f @REPORT_FILE
     ```

4. Launch tmux session
   - Launch the appropriate CLI inside tmux based on @MODEL_NAME:
     ```bash
     case "@MODEL_NAME" in
       gpt-5.*|gpt-5.*-codex|gpt-5.*-codex-*)
        tmux new-session -d -s @SESSION_NAME \
          "bash -lc 'cd \"$PROJECT_ROOT\" && \
            STATUS=0; \
            codex exec --model @MODEL_NAME --config model_reasoning_effort=\"@REASONING\" --full-auto --cd \"$PROJECT_ROOT\" \
              \"@USER_PROMPT\" 2>&1 | tee -a \"$REPORT_FILE\"; \
            STATUS=${PIPESTATUS[0]}; \
            printf \"\\n## Completed: %s (exit %s)\\n\" \"$(date -u)\" \"$STATUS\" >> \"$REPORT_FILE\"; \
            exit \"$STATUS\"'"
        ;;
       claude-*)
         tmux new-session -d -s @SESSION_NAME \
          "bash -lc 'cd \"$PROJECT_ROOT\" && \
            STATUS=0; \
            claude --model @MODEL_NAME -p --permission-mode acceptEdits \
              \"@USER_PROMPT\" 2>&1 | tee -a \"$REPORT_FILE\"; \
            STATUS=${PIPESTATUS[0]}; \
            printf \"\\n## Completed: %s (exit %s)\\n\" \"$(date -u)\" \"$STATUS\" >> \"$REPORT_FILE\"; \
            exit \"$STATUS\"'"
        ;;
       gemini-*)
         tmux new-session -d -s @SESSION_NAME \
          "bash -lc 'cd \"$PROJECT_ROOT\" && \
            STATUS=0; \
            gemini --model @MODEL_NAME -p --approval-mode auto_edit \
              \"@USER_PROMPT\" 2>&1 | tee -a \"$REPORT_FILE\"; \
            STATUS=${PIPESTATUS[0]}; \
            printf \"\\n## Completed: %s (exit %s)\\n\" \"$(date -u)\" \"$STATUS\" >> \"$REPORT_FILE\"; \
            exit \"$STATUS\"'"
        ;;
       *)
         echo "Unknown model selector: @MODEL_NAME" >&2
         exit 1
         ;;
     esac
     ```
   - Capture @PROCESS_ID via `tmux display-message -t @SESSION_NAME:0 -p '#{pane_pid}'` and store it with the session metadata.

5. Confirm launch status (single check)
   - Check once whether the tmux session exists:
     - If listed, report that the background task is running and provide the monitoring commands.
     - If not listed, check @REPORT_FILE for completion output or errors and report the most likely outcome.
   - Do not loop or continually re-check; this is a background task.
   - Use a safe session check that cannot treat the session name as a flag:
     ```bash
     if tmux list-sessions -F '#S' 2>/dev/null | grep -Fx -- "$SESSION_NAME" >/dev/null; then
       echo "Session is running"
     else
       echo "Session not found"
     fi
     ```

6. Configure monitoring
   - Document how operators can manage the session:
     - Attach: `tmux attach -t @SESSION_NAME`
     - Capture output: `tmux capture-pane -p -S -200 -t @SESSION_NAME`
     - Stop when complete: `tmux kill-session -t @SESSION_NAME`
   - Note that progress is continuously appended to @REPORT_FILE for non-interactive monitoring (`tail -f @REPORT_FILE`).

7. Report launch status
   - Summarize model, reasoning effort, tmux session, PID, and report path.
   - Provide explicit monitoring and termination guidance so operators can manage the background task without guessing.

## Output

```md
# RESULT

- Summary: Background task launched (@MODEL_NAME, @REASONING) inside tmux session @SESSION_NAME.

## PROCESS

- tmux session: @SESSION_NAME
- PID: @PROCESS_ID
- Command: tmux new-session -d -s @SESSION_NAME '<CLI command from Step 4 based on @MODEL_NAME>'

## REPORT

- File: @REPORT_FILE
- Monitoring:
  - `tmux attach -t @SESSION_NAME`
  - `tmux capture-pane -p -S -200 -t @SESSION_NAME`
  - `tail -f @REPORT_FILE`
  - `tmux kill-session -t @SESSION_NAME`

## NEXT STEPS

1. Review the report for periodic updates.
2. Terminate the tmux session when work completes (`tmux kill-session -t @SESSION_NAME`).
```

## Examples

```bash
# Default background task
/task-background "Analyze the codebase for performance issues"

# Custom model with explicit report path
/task-background "Refactor the authentication module" --model gpt-5.1-codex-max --reasoning high ./.enaible/agents/background/auth-refactor.md
```
