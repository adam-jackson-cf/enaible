# CLI Reference

Use the Enaible docs scraper command to fetch and convert documentation pages.

## Command Template

```bash
uv run --project tools/enaible enaible docs_scrape \
  "$URL" \
  "$OUTPUT_DIR/$FILENAME.md" \
  --title "$TITLE"
```

## Examples

```bash
uv run --project tools/enaible enaible docs_scrape \
  "https://react.dev/reference/react" \
  "./react-reference.md" \
  --title "React Reference"
```

```bash
uv run --project tools/enaible enaible docs_scrape \
  "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization" \
  "./http-authorization-header.md" \
  --title "HTTP Authorization Header"
```

## Batch Run Example

```bash
while read -r url title filename; do
  uv run --project tools/enaible enaible docs_scrape \
    "$url" \
    "./$filename.md" \
    --title "$title"
done < urls.txt
```
