# Purpose

Build `analysis.json` deterministically from a structured analysis input file.

## Variables

### Required

- @INPUT_PATH — structured analysis input JSON (same fields as `analysis.json`, minus `analysisAt` if desired)
- @OUTPUT_PATH — analysis JSON (`@ARTIFACT_ROOT/analysis.json`)

## Workflow

```bash
"$PYTHON_CMD" scripts/research_analyze.py \
  --input-path "@INPUT_PATH" \
  --output-path "@OUTPUT_PATH"
```

The script stamps `analysisAt` if missing and validates the output against the analysis schema.

## Controlled values

- `confidence`: `high`, `medium`, `low`
- `importance`: `key`, `supporting`, `background`
- `priority`: `high`, `medium`, `low`

## Input format

```json
{
  "executiveSummary": "Summary text",
  "findings": [
    {
      "id": "f1",
      "title": "Finding title",
      "statement": "Finding statement",
      "confidence": "high",
      "importance": "key",
      "sourceIds": ["src-001", "src-002", "src-003"]
    }
  ],
  "insights": [
    { "id": "i1", "statement": "Insight", "sourceIds": ["src-001"] }
  ],
  "recommendations": [
    {
      "id": "r1",
      "action": "Recommendation",
      "rationale": "Reasoning",
      "priority": "high",
      "sourceIds": ["src-002", "src-003"]
    }
  ],
  "limitations": ["Limitations text"]
}
```
