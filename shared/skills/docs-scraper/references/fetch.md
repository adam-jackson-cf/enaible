# Fetch & Capture

Run the skill-local script once per URL. All command snippets assume the environment variables from Preflight are set.

## Command template

```bash
"$PYTHON_CMD" scripts/run_docs_scraper.py \
  "$URL" \
  "$ARTIFACT_ROOT/output/$FILENAME.md" \
  --title "$TITLE" \
  --log-level INFO \
  > "$ARTIFACT_ROOT/logs/$FILENAME.log" 2>&1
```

- `--title` is optional; omit it to use the detected page title.
- Use `--log-level DEBUG` if Crawl4AI becomes unstable; include the log file in your final report.

## Validation

For each run:

- Ensure the script exits 0. If not, capture stderr from the `.log` file and decide whether to retry (after refreshing Playwright) or fall back to manual capture.
- Confirm the resulting markdown contains the header, `Source:` line, `Scraped:` timestamp, and non-empty body.
- If content looks truncated, capture raw HTML using the system fetch tool, store it under `@ARTIFACT_ROOT/output/`, and note the fallback when reporting.

## Batch mode (optional)

```bash
while read -r url title filename; do
  "$PYTHON_CMD" scripts/run_docs_scraper.py \
    "$url" \
    "$ARTIFACT_ROOT/output/$filename.md" \
    --title "$title" \
    --log-level INFO \
    > "$ARTIFACT_ROOT/logs/$filename.log" 2>&1
done < urls.txt
```

Use CSV or TSV inputs only when the destination naming scheme is finalized; mixing ad-hoc filenames makes auditing difficult.
