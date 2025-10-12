# Purpose

Shrink and sanitize the Claude configuration history while safeguarding backups and validating the cleaned file.

## Variables

- `CLEAR_ALL_HISTORY` ← boolean flag set when `--clear-all-history` appears in `$ARGUMENTS`.
- `SCRIPT_PATH` ← resolved absolute path to `clean_claude_config.py`.
- `$ARGUMENTS` ← raw argument string for logging.

## Instructions

- ALWAYS create a timestamped backup of `~/.claude.json` before modifying it.
- Enforce every STOP confirmation (pre-clean, post-clean, validation) before advancing.
- Never run without confirming the script path and config file exist.
- Prefer default mode (preserve structure) unless the user explicitly asks for `--clear-all-history`.
- Validate JSON integrity and Claude CLI connectivity after cleaning.

## Workflow

1. Resolve prerequisites
   - Run `ls .claude/scripts/utils/clean_claude_config.py || ls "$HOME/.claude/scripts/utils/clean_claude_config.py"`; if both fail, request an explicit script path and exit if unavailable.
   - Run `ls -la "$HOME/.claude.json"`; exit immediately if the configuration file is missing or unreadable.
2. Back up configuration
   - Run `cp "$HOME/.claude.json" "$HOME/.claude.json.backup.$(date +%Y%m%d-%H%M%S)"`.
   - **STOP:** “Config validated and backed up. Proceed with cleaning? (y/n)”
3. Execute cleaning
   - Default command: `python3 "$SCRIPT_PATH"`.
   - If `CLEAR_ALL_HISTORY=true`: append `--clear-all-history`.
   - Capture stdout/stderr for reporting.
4. Post-clean verification
   - Show file sizes before/after (e.g., `ls -lh` on config and backups).
   - **STOP:** “Cleaning complete. Review results and test Claude functionality? (y/n)”
5. Validate integrity
   - Run:
     - `claude --version`
     - `claude mcp list`
     - `python3 -c "import json; json.load(open('$HOME/.claude.json'))"`
   - Collect outputs and flag failures.
   - **STOP:** “Validation complete. Archive old backups? (y/n)”
6. Optional cleanup
   - On approval, rotate backups (keep most recent three, delete older ones).
   - Summarize archive actions taken.
7. Report results
   - Provide final size comparison, applied mode, validation status, and next steps.

## Output

```md
# RESULT

- Summary: Claude history cleaned (mode: <default|clear-all-history>).

## DETAILS

- Original Size: <size>
- Cleaned Size: <size>
- Backup: <path to newest backup>
- Validation: <pass|fail> (claude --version, claude mcp list, JSON parse)

## FOLLOW-UP

- If validation failed: Restore from backup <path> and retry.
- If validation passed: Confirm Claude behaves as expected.
```

## Examples

```bash
# Remove large conversation history while preserving structure
/clean-history

# Fully clear history content for a fresh start
/clean-history --clear-all-history
```
