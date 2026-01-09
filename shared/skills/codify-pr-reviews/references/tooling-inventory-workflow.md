# Purpose

Inventory deterministic tooling configurations and rule identifiers to enable coverage comparison.

## Variables

- @OUTPUT_PATH — tooling inventory JSON (`@ARTIFACT_ROOT/tooling-inventory.json`)

## Workflow

1. **Run tooling inventory**

   ```bash
   "$PYTHON_CMD" scripts/tooling_inventory.py \
     --repo-root "." \
     --output-path "@OUTPUT_PATH"
   ```

2. **Validate output**
   - Confirm tool entries exist for Semgrep/Ruff/ESLint/Prettier where configs are present.
   - Review parse errors and note them in `@ARTIFACT_ROOT/notes.md`.
