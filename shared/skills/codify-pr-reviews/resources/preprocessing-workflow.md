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

- Run exact matching first, then fuzzy (simhash), then semantic checks for edge cases.
- Always keep red-flag matches even if below @MIN_OCCURRENCES.
- Return summary: input count, output groups, filtered count.

## Workflow

1. **Exact match grouping**
   - Group identical comment text.

2. **Fuzzy match grouping**
   - Use simhash or equivalent to group near-duplicates.

3. **Semantic grouping**
   - For ambiguous leftovers, run a lightweight semantic check.

4. **Frequency filter**
   - Keep groups with occurrences >= @MIN_OCCURRENCES.

5. **Red-flag override**
   - Keep any group matching red flags regardless of frequency.

6. **Write output**
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
