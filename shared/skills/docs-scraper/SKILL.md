---
name: docs-scraper
description: Fetch documentation from URLs and save clean markdown files for offline reference. USE WHEN the user asks to scrape, archive, or analyze docs from the web.
compatibility: Requires network access, `uv`, and the Enaible CLI with write access to the desired output directory.
allowed-tools: @BASH @READ @WRITE
---

# Docs Scraper

Capture documentation from URLs and save it as readable, well-structured markdown for offline use.

- The user wants one or more URLs scraped or archived for later reference.
- You need deterministic markdown output for local analysis or sharing.
- You must enrich captures with metadata (sources, timestamps) for auditing.

## Need to...? Read This

| Goal                         | Reference                                                                |
| ---------------------------- | ------------------------------------------------------------------------ |
| End-to-end workflow          | [references/docs-scrape-workflow.md](references/docs-scrape-workflow.md) |
| Command reference + examples | [references/cli-reference.md](references/cli-reference.md)               |

## Workflow

Detailed commands and success criteria live in the reference files. Use this overview to stay aligned with the standard skill structure.

### Step 0: Intake

**Purpose**: Confirm URLs, environment readiness, and storage targets before running scripts.

- Validate provided URLs, deduplicate, and capture any authentication requirements.
- Confirm `uv` + the Enaible CLI are available, you have write access to the destination directory, and the naming pattern is agreed upon.
- Record the destination folder, filename pattern, and any required metadata tags.

### Step 1: Fetch

**Purpose**: Run `enaible docs_scrape` (via `uv run` if needed) for each URL and validate outputs.

- Generate markdown captures plus raw artifacts, storing them under the designated output directory.
- Follow fetch + verification instructions in [references/docs-scrape-workflow.md](references/docs-scrape-workflow.md).

### Step 2: Clean + Save

**Purpose**: Normalize markdown, add source attribution, and save files.

- Apply any post-processing (frontmatter, link rewrites) described in the workflow reference.
- Summarize results for the user and highlight manual follow-ups.
- Consult [references/cli-reference.md](references/cli-reference.md) for command variants and examples.
