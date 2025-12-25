# Purpose

Transform grouped comments into structured patterns and triage them against existing instruction rules.

## Variables

### Required

- @PREPROCESSED_PATH — grouped comments JSON
- @INSTRUCTION_FILES — mapping of existing instruction files to scan
- @OUTPUT_PATH — output JSON for patterns

### Optional

- @CATEGORIES — list of categories to classify patterns

## Instructions

- Ask the user to confirm the Python command and set `PYTHON_CMD` (must be 3.12+).
- Parse existing instruction files to extract rule titles and examples.
- For each comment group, generate a pattern with severity and category.
- Triage each pattern into: already covered, needs strengthening, or new rule.
- Save rationale and suggested actions in @OUTPUT_PATH.

## Defaults

- Categories and instruction file paths fall back to `config/defaults.json`.

## Deterministic tooling

```bash
"$PYTHON_CMD" scripts/analyze_patterns.py \
  --input-path "@PREPROCESSED_PATH" \
  --output-path "@OUTPUT_PATH"
```

## Workflow

1. **Load grouped comments**
   - Read @PREPROCESSED_PATH.

2. **Parse existing rules**
   - Extract headings, directives, and examples from @INSTRUCTION_FILES.

3. **Generate patterns**
   - Title, description, severity, category, frequency, examples.

4. **Triage**
   - 🟢 Already covered: rule exists + frequency within expected adherence.
   - 🟡 Needs strengthening: rule exists but gaps or high frequency.
   - 🔴 New rule: no existing coverage (or red-flag override).

5. **User approval (Stage 5)**
   - Pause and @ASK_USER_CONFIRMATION for each pattern decision.

6. **Write output**
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
