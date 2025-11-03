# Purpose

Append a timestamped summary of the current chat session to `session-notes.md`, capturing discussions, actions, and outstanding work.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @SESSION_FILE = --session-file — destination file (default ./session-notes.md)
- @DISCUSSION_HINT = --overview — optional sentence appended to Discussion Overview

### Derived (internal)

- (none)

## Instructions

- Gather a complete view of the current session before writing (messages, actions, command outputs).
- Append—never overwrite—`session-notes.md`; maintain chronological order.
- Summaries must be factual, concise, and actionable; highlight key decisions and pending items.
- Use the provided markdown structure exactly; omit sections only when truly empty.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. Collect session context
   - Review recent conversation history, executed commands, file edits, and outcomes.
   - Extract key themes, actions, and blockers.
2. Prepare note entry
   - Capture `TIMESTAMP`.
   - Derive bullet lists for Actions Taken, Files Referenced, Outstanding Tasks, etc.
   - If @DISCUSSION_HINT is supplied, incorporate it into Discussion Overview.
3. Ensure file availability
   - `touch session-notes.md` if the file does not exist.
4. Append entry
   - Use the template below, filling each section with session-specific content.
   - Separate entries with `---`.
5. Confirm write
   - Optionally display the appended section for verification.
6. Report completion
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
/create-session-notes --overview "Focus: API error triage"
```
