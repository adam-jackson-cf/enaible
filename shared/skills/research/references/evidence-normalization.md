# Purpose

Normalize evidence by standardizing publisher names and deduplicating sources.

## Variables

### Required

- @EVIDENCE_PATH — evidence JSON (`@ARTIFACT_ROOT/evidence.json`)

### Optional

- @PUBLISHER_MAP_PATH — publisher normalization map (`assets/publisher-map.json`)

## Workflow

```bash
"$PYTHON_CMD" scripts/research_normalize.py \
  --evidence-path "@EVIDENCE_PATH" \
  --publisher-map-path "@PUBLISHER_MAP_PATH"
```

The script updates `evidence.json` in place, adds canonical URLs, and records deduplicated sources under `normalization`.

## Notes

- Re-run normalization after adding new sources (logging clears prior normalization metadata).
- Canonical URLs are produced by stripping tracking parameters and fragments.
