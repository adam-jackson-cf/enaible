# Purpose

Detect the repository technology stack and generate red-flag patterns that must always be surfaced.

## Variables

### Required

- @PROJECT_ROOT — repository root to scan
- @OUTPUT_PATH — path to write the red-flag JSON file

### Optional

- @FORCE_REFRESH — when true, regenerate even if red flags already exist

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Scan dependency and config files to infer backend, frontend, database, and language.
- Generate stack-specific red flags plus a universal security list.
- Cache results at @OUTPUT_PATH and only regenerate when @FORCE_REFRESH is true.
- Return a concise summary (stack + red-flag count) to the main workflow.

## Workflow

1. **Run deterministic stack analysis**
   - Execute the script to detect stack and red flags:
     ```bash
     "$PYTHON_CMD" scripts/stack_analysis.py \
       --project-root "@PROJECT_ROOT" \
       --output-path "@OUTPUT_PATH"
     ```

2. **Review summary**
   - Confirm detected stack and red-flag count.

3. **Write output**
   - Save JSON to @OUTPUT_PATH.
   - If output already exists and @FORCE_REFRESH is false, reuse it.

## Output

```json
{
  "generatedAt": "2025-10-30T14:30:00Z",
  "stack": {
    "backend": "Express.js",
    "frontend": "React",
    "database": "SQLite",
    "language": "TypeScript"
  },
  "redFlags": [
    "SQL injection",
    "hardcoded secret",
    "bcrypt sync",
    "dangerouslySetInnerHTML"
  ]
}
```
