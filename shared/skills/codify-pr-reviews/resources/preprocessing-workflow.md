# Purpose

Deduplicate and group PR comments with a hybrid exact + fuzzy + semantic approach.

## Variables

### Required

- @INPUT_PATH — fetched comments JSON
- @RED_FLAGS_PATH — red flags JSON from stack analysis
- @OUTPUT_PATH — output JSON for grouped comments

### Optional

- @MIN_OCCURRENCES — minimum frequency to keep a group (default 3)
- @SEMANTIC_THRESHOLD — similarity threshold for semantic grouping (default 0.85)

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Run exact matching first, then fuzzy (simhash), then semantic checks for edge cases.
- Always keep red-flag matches even if below @MIN_OCCURRENCES.
- Return summary: input count, output groups, filtered count.

## Defaults

- Optional parameters fall back to `config/defaults.json` when omitted.

## Workflow

1. **Run deterministic preprocessing**
   - Execute the script to dedupe and group comments:
     ```bash
     "$PYTHON_CMD" scripts/preprocess_comments.py \
       --input-path "@INPUT_PATH" \
       --red-flags-path "@RED_FLAGS_PATH" \
       --min-occurrences "@MIN_OCCURRENCES" \
       --semantic-threshold "@SEMANTIC_THRESHOLD" \
       --output-path "@OUTPUT_PATH"
     ```

2. **Review summary**
   - Confirm input count, output groups, and red-flag retention.

3. **Write output**
   - Save grouped comments to @OUTPUT_PATH.

## Output

```json
{
  "processedAt": "2025-10-30T14:32:15Z",
  "inputComments": 450,
  "outputGroups": 20,
  "filteredOut": 330,
  "commentGroups": [
    {
      "id": "sql-injection",
      "representative": "SQL injection vulnerability",
      "occurrences": 8,
      "isRedFlag": true,
      "examples": [
        { "pr": 123, "comment": "SQL injection here", "author": "reviewer1" }
      ]
    }
  ]
}
```
