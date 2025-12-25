# Purpose

Run mandatory user approvals for pattern decisions and rule wording before modifying instruction files.

## Variables

### Required

- @PATTERNS_PATH — patterns JSON from analysis stage
- @DRAFTS_DIR — directory containing generated rule drafts
- @APPROVED_PATTERNS_PATH — output JSON for approved patterns
- @APPROVED_RULES_PATH — output JSON for approved rules

## Instructions

- Use explicit user confirmations at each checkpoint.
- Process one pattern or rule at a time; do not batch approvals.
- Record the decision and rationale in the output JSON files.
- If user requests edits, capture feedback verbatim.

## Workflow

1. **Pattern review (Stage 5)**
   - Load @PATTERNS_PATH.
   - For each pattern, ask the user to choose: skip, strengthen, or create.
   - Write decisions to @APPROVED_PATTERNS_PATH.

2. **Rule wording review (Stage 7)**
   - Load drafts from @DRAFTS_DIR.
   - Present each rule and ask for approval, edit, retarget, or reject.
   - Write decisions to @APPROVED_RULES_PATH.

3. **Final confirmation (Stage 8)**
   - Before editing instruction files, request explicit approval.
   - If approved, proceed with rule application.

## Output

```json
{
  "metadata": {
    "runId": "2025-10-30_143022",
    "approvedPatterns": 8,
    "approvedRules": 6
  },
  "approvedPatterns": [
    {
      "patternId": "sql-injection",
      "action": "strengthen",
      "userFeedback": "Add LIKE and IN clause examples"
    }
  ]
}
```
