# Purpose

Apply approved rule drafts to instruction files with a final user confirmation checkpoint.

## Variables

### Required

- @APPROVED_RULES_PATH — approved rules JSON
- @INSTRUCTION_FILES — mapping of instruction files to update

## Instructions

- Load approved rules and map them to target instruction files.
- Pause and @ASK_USER_CONFIRMATION before modifying files.
- Apply edits and record a summary.

## Workflow

1. **Load approved rules**
   - Read @APPROVED_RULES_PATH.

2. **Final confirmation**
   - Pause and @ASK_USER_CONFIRMATION before editing instruction files.

3. **Apply edits**
   - Update target files and record a summary of changes.

## Output

- Updated instruction files
- Summary file of applied changes
