# Purpose

Append a timestamped summary of the current chat session to `session-notes.md`, capturing discussions, actions, and outstanding work.

## Variables

- `SESSION_FILE` ← `./session-notes.md` (create if missing).
- `TIMESTAMP` ← ISO-formatted timestamp (`date -u +"%Y-%m-%dT%H:%M:%SZ"`).
- `$ARGUMENTS` ← optional context string to insert under Discussion Overview.

## Instructions

- Gather a complete view of the current session before writing (messages, actions, command outputs).
- Append—never overwrite—`session-notes.md`; maintain chronological order.
- Summaries must be factual, concise, and actionable; highlight key decisions and pending items.
- Use the provided markdown structure exactly; omit sections only when truly empty.

## Workflow

1. Prepare workspace
   - Run `mkdir -p . && test -w .`; exit immediately if the working directory is not writable because session notes must be persisted.
2. Collect session context
   - Review recent conversation history, executed commands, file edits, and outcomes.
   - Extract key themes, actions, and blockers.
3. Prepare note entry
   - Capture `TIMESTAMP`.
   - Derive bullet lists for Actions Taken, Files Referenced, Outstanding Tasks, etc.
   - If `$ARGUMENTS` supplied, incorporate into Discussion Overview.
4. Ensure file availability
   - `touch session-notes.md` if the file does not exist.
5. Append entry
   - Use the template below, filling each section with session-specific content.
   - Separate entries with `---`.
6. Confirm write
   - Optionally display the appended section for verification.
7. Report completion
   - Provide file path and summary of captured highlights.

## Output

```md
# RESULT

- Summary: Session notes appended for <TIMESTAMP>.
- File: session-notes.md
- Sections Updated: [Overview, Actions, Files, Outstanding, Decisions, Next Steps, Context]
```

## Examples

```bash
# Record current session summary
/create-session-notes

# Add contextual hint for discussion overview
/create-session-notes "Focus: API error triage"
```
