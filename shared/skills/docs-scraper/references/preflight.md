# Preflight & Environment

Use this checklist before running any docs-scraper commands.

## Export shared variables

```bash
export PYTHON_CMD="${PYTHON_CMD:-python3}"
export RUN_ID="docs-scraper-$(date -u +%Y%m%dT%H%M%SZ)"
export ARTIFACT_ROOT=".enaible/artifacts/docs-scraper/$RUN_ID"
mkdir -p "$ARTIFACT_ROOT/output" "$ARTIFACT_ROOT/logs"
```

- `PYTHON_CMD` must resolve to Python 3.12+.
- `ARTIFACT_ROOT` is the only allowed destination for outputs, logs, and fallback assets.

## Install runtime dependencies (first run per environment)

```bash
uv pip install --python "$PYTHON_CMD" "crawl4ai>=0.7,<0.8" playwright
"$PYTHON_CMD" -m playwright install chromium
```

- Re-run only when the Python environment or system image changes.
- Capture failures (e.g., missing system libraries) in your session notes before proceeding.

## Validate inputs & storage

- Deduplicate the URL list and record any required authentication flow.
- Confirm you can write to `@ARTIFACT_ROOT`; stop if the path is on a read-only volume.
- Decide the filename scheme (kebab-case, includes vendor/product, etc.) up front so every artifact is predictable.
