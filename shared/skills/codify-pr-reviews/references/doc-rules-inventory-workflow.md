# Purpose

Inventory existing system doc rules to compare coverage against extracted patterns.

## Variables

- @INSTRUCTION_FILES — mapping of instruction files to scan (derived from @TARGET_SYSTEM)
- @OUTPUT_PATH — doc rules inventory JSON (`@ARTIFACT_ROOT/doc-rules.json`)

## Workflow

1. **Run doc rules inventory**

   ```bash
   "$PYTHON_CMD" scripts/doc_rules_inventory.py \
     --instruction-files "@INSTRUCTION_FILES" \
     --output-path "@OUTPUT_PATH"
   ```

2. **Validate output**
   - Ensure each rule includes `title`, `hasDirectives`, `hasGood`, `hasBad`, and `sourcePath`.
   - Capture `ruleId` when a `Rule-ID:` line is present.
