# Purpose

Transform grouped comments into structured patterns and triage them against existing instruction rules.

## Variables

### Required

- @PREPROCESSED_PATH — grouped comments JSON
- @TARGET_SYSTEM — target system identifier (`claude-code` or `codex`)
- @INSTRUCTION_FILES — mapping of existing instruction files to scan (derived from @TARGET_SYSTEM)
- @OUTPUT_PATH — output JSON for patterns

### Optional

- @CATEGORIES — list of categories to classify patterns

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Resolve @TARGET_SYSTEM and derive @INSTRUCTION_FILES using `resources/system-targeting.md`.
- Parse existing instruction files to extract rule titles and examples.
- For each comment group, generate a pattern with severity and category.
- Triage each pattern into: already covered, needs strengthening, or new rule.
- Save rationale and suggested actions in @OUTPUT_PATH.

## Defaults

- Categories and instruction file paths fall back to `config/defaults.json`.

## Workflow

1. **Run deterministic pattern analysis**
   - Execute the script to parse rules and classify patterns:
     ```bash
     "$PYTHON_CMD" scripts/analyze_patterns.py \
       --input-path "@PREPROCESSED_PATH" \
       --instruction-files "@INSTRUCTION_FILES" \
       --output-path "@OUTPUT_PATH"
     ```

2. **Review triage**
   - 🟢 Already covered: rule exists + frequency within expected adherence.
   - 🟡 Needs strengthening: rule exists but gaps or high frequency.
   - 🔴 New rule: no existing coverage (or red-flag override).

3. **User approval (Stage 5)**
   - Pause and @ASK_USER_CONFIRMATION for each pattern decision.

4. **Write output**
   - Save patterns + triage metadata to @OUTPUT_PATH.

## Output

```json
{
  "analyzedAt": "2025-10-30T14:35:40Z",
  "summary": {
    "totalPatterns": 12,
    "alreadyCovered": 4,
    "needsStrengthening": 3,
    "newRules": 5
  },
  "patterns": [
    {
      "id": "sql-injection",
      "title": "SQL Injection via String Concatenation",
      "frequency": 8,
      "severity": "critical",
      "category": "security",
      "triage": "needs-strengthening",
      "suggestedAction": "Add examples for LIKE queries, IN clauses",
      "examples": [
        { "pr": 123, "comment": "SQL injection here", "file": "auth.ts:45" }
      ]
    }
  ]
}
```
