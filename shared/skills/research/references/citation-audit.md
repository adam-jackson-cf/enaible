# Purpose

Validate that findings, insights, and recommendations cite enough logged sources with traceable IDs.

## Variables

### Required

- @ANALYSIS_PATH — analysis JSON (`@ARTIFACT_ROOT/analysis.json`)
- @EVIDENCE_PATH — evidence JSON (`@ARTIFACT_ROOT/evidence.json`)
- @OUTPUT_PATH — citation report (`@ARTIFACT_ROOT/citation-report.json`)

## Workflow

1. **Run citation validation**

   ```bash
   "$PYTHON_CMD" scripts/research_citations.py \
     --analysis-path "@ANALYSIS_PATH" \
     --evidence-path "@EVIDENCE_PATH" \
     --output-path "@OUTPUT_PATH"
   ```

Optional overrides:

- `--min-sources-insight` and `--min-sources-recommendation` to raise/lower thresholds for those sections.

2. **Fix violations**
   - Add missing sources or adjust findings until the report passes.

## Analysis JSON format

```json
{
  "analysisAt": "2026-01-09T00:00:00Z",
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
    {
      "id": "i1",
      "statement": "Cross-domain insight",
      "sourceIds": ["src-001", "src-004"]
    }
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
