# Purpose

Compare extracted patterns against tooling inventory and system doc rules to suggest enforcement paths.

## Variables

- @PATTERNS_PATH — extracted patterns (`@ARTIFACT_ROOT/patterns.json`)
- @TOOLING_INVENTORY_PATH — tooling inventory (`@ARTIFACT_ROOT/tooling-inventory.json`)
- @DOC_RULES_PATH — doc rules inventory (`@ARTIFACT_ROOT/doc-rules.json`)
- @OUTPUT_PATH — coverage comparison (`@ARTIFACT_ROOT/coverage.json`)

## Workflow

1. **Run coverage comparison**

   ```bash
   "$PYTHON_CMD" scripts/coverage_compare.py \
     --patterns-path "@PATTERNS_PATH" \
     --tooling-inventory-path "@TOOLING_INVENTORY_PATH" \
     --doc-rules-path "@DOC_RULES_PATH" \
     --output-path "@OUTPUT_PATH"
   ```

2. **Validate output**
   - Confirm each pattern has `docCoverage`, `toolingCoverage`, and `enforcementSuggestion`.
   - Use this file during enforcement review; do not draft rules before it exists.
