# Purpose

Review coverage findings and approve enforcement decisions for tooling and/or system docs.

## Variables

- @COVERAGE_PATH — coverage comparison (`@ARTIFACT_ROOT/coverage.json`)
- @APPROVED_PATH — approved enforcement output (`@ARTIFACT_ROOT/approved-enforcement.json`)
- @DOC_PATTERNS_PATH — doc-only patterns (`@ARTIFACT_ROOT/doc-patterns.json`)
- @TOOLING_CHANGES_PATH — tooling change plan (`@ARTIFACT_ROOT/tooling-changes.md`, plus `.json`)

## Workflow

1. **Review coverage findings**
   - Walk each pattern in `coverage.json` with the user.
   - Confirm whether the pattern represents a quality issue, and where enforcement should live (`tooling`, `docs`, `both`, or `skip`).
   - Capture the decision for each pattern, including:
     - `enforcementPath`
     - `action` (`create`, `strengthen`, `skip`)
     - `rationale`
     - `toolingAction` when `tooling` or `both` is selected.

2. **Write approval artifact**
   - Save decisions in `@APPROVED_PATH` using this structure:

   ```json
   {
     "approvedAt": "2026-01-09T16:00:00Z",
     "patterns": [
       {
         "id": "sql-injection",
         "title": "Avoid string-based SQL queries",
         "description": "Use parameterized queries instead of string concatenation.",
         "category": "security",
         "frequency": 8,
         "decision": {
           "enforcementPath": "tooling",
           "action": "strengthen",
           "toolingAction": "Add Semgrep rule for raw SQL string concatenation",
           "rationale": "Semgrep is configured but no matching rule exists."
         }
       }
     ]
   }
   ```

3. **Prepare enforcement outputs**
   - Generate doc patterns and tooling change plan:

   ```bash
   "$PYTHON_CMD" scripts/prepare_enforcement_outputs.py \
     --approved-path "@APPROVED_PATH" \
     --coverage-path "@COVERAGE_PATH" \
     --doc-patterns-path "@DOC_PATTERNS_PATH" \
     --tooling-changes-path "@TOOLING_CHANGES_PATH"
   ```

```

4. **Proceed to drafting**
 - Use `doc-patterns.json` for rule drafting.
 - Use `tooling-changes.md` and `tooling-changes.json` to guide deterministic enforcement updates.
```
