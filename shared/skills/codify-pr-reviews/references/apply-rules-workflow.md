# Purpose

Apply approved rule drafts to instruction files with a final user confirmation checkpoint.

## Variables

### Required

- @APPROVED_RULES_PATH — approved rules JSON (`@ARTIFACT_ROOT/patterns.json` or per-rule approvals under `@ARTIFACT_ROOT/drafts/`)
- @TARGET_SYSTEM — target system identifier (`claude-code`, `codex`, `copilot`, `cursor`, or `gemini`)
- @INSTRUCTION_FILES — mapping of instruction files to update (derived from @TARGET_SYSTEM)

## Instructions

- Load approved rules and map them to target instruction files.
- Resolve @TARGET_SYSTEM and derive @INSTRUCTION_FILES using `references/system-targeting.md`.
- Pause and @ASK_USER_CONFIRMATION before modifying files.
- Apply edits and record a summary.
- Persist the change log at `@ARTIFACT_ROOT/apply-summary.json` (or `.md`) alongside any supporting diffs.

## Workflow

1. **Load approved rules**
   - Read @APPROVED_RULES_PATH.

2. **Final confirmation**
   - Pause and @ASK_USER_CONFIRMATION before editing instruction files.

3. **Apply edits**
   - Update target files and record a summary of changes under `@ARTIFACT_ROOT/apply-summary.json` (or `.md`) plus any diff logs required for audit.

## Output

- Updated instruction files
- Summary file at `.enaible/artifacts/codify-pr-reviews/<timestamp>/apply-summary.*`
