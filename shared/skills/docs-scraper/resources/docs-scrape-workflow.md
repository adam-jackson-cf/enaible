# Docs Scrape Workflow

Use this workflow when converting one or more documentation URLs into clean markdown files.

## 1) Intake

- Confirm the list of URLs to scrape.
- Confirm the output directory (default to current directory if not specified).
- Determine filenames using kebab-case derived from the URL path or page title.

## 2) Fetch with the Enaible CLI

For each URL, run the docs scraper command:

```bash
uv run --project tools/enaible enaible docs_scrape \
  --url "$URL" \
  --out "$OUTPUT_DIR/$FILENAME.md" \
  --title "$TITLE"
```

If the command exits non-zero or the content is incomplete, use the system’s web fetch tool (or `curl`) to capture the page and then convert it to markdown manually.

## 3) Clean + Normalize

- Remove navigation menus, footers, and duplicate content.
- Preserve all substantive documentation content.
- Keep code blocks and examples intact.
- Ensure headings use proper `#`/`##`/`###` hierarchy.

## 4) Add Source Attribution

At the top of each output file, include:

```markdown
Source: <URL>
Scraped: <YYYY-MM-DD>
```

Use the local date for the scrape.

## 5) Save + Report

- Write the cleaned content to the chosen output path.
- Provide a short summary of what was saved and the output file locations.
