# Purpose

Extract normalized comment patterns from preprocessed groups without making enforcement decisions.

## Variables

- @PREPROCESSED_PATH — grouped comments JSON (`@ARTIFACT_ROOT/preprocessed.json`)
- @OUTPUT_PATH — patterns output (`@ARTIFACT_ROOT/patterns.json`)

## Workflow

1. **Run pattern extraction**

   ```bash
   "$PYTHON_CMD" scripts/extract_patterns.py \
     --preprocessed-path "@PREPROCESSED_PATH" \
     --output-path "@OUTPUT_PATH"
   ```

2. **Validate output**
   - Ensure each pattern has `id`, `title`, `description`, `category`, and `frequency`.
   - Confirm no enforcement decisions are embedded here (those happen later).
