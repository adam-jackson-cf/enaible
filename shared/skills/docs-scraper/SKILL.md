---
name: docs-scraper
description: Fetch documentation from URLs and save clean markdown files for offline reference. USE WHEN the user asks to scrape, archive, or analyze docs from the web.
compatibility: Requires uv≥0.4, Python 3.12+ (export `PYTHON_CMD`), and Crawl4AI + Playwright dependencies installed in the active environment.
allowed-tools: @BASH @READ @WRITE
---

# Docs Scraper

Capture documentation from URLs and save it as readable, well-structured markdown for offline use.

- The user wants one or more URLs scraped or archived for later reference.
- You need deterministic markdown output for local analysis or sharing.
- You must enrich captures with metadata (sources, timestamps) for auditing.

## Need to...? Read This

| Goal                     | Reference                                                        |
| ------------------------ | ---------------------------------------------------------------- |
| Preflight & environment  | [references/preflight.md](references/preflight.md)               |
| Fetch & capture          | [references/fetch.md](references/fetch.md)                       |
| Clean, attribute, report | [references/clean-and-report.md](references/clean-and-report.md) |

## Workflow

Detailed instructions, artifact conventions, and success criteria live in the reference files. Use this overview to stay aligned with the standard skill structure.

### Step 0: Preflight + establish run directories

**Purpose**: Confirm environment readiness and guarantee deterministic storage before scraping.

- Follow the [Preflight reference](references/preflight.md) to export `PYTHON_CMD`, `RUN_ID`, and `ARTIFACT_ROOT`, install Crawl4AI + Playwright as needed, and lock in filenames plus storage locations.
- Keep every output/log under `@ARTIFACT_ROOT`; no other destination paths are allowed.

### Step 1: Fetch

**Purpose**: Run the skill-local script for each URL and validate outputs.

- Use the command template + batch loop in the [Fetch reference](references/fetch.md) so every capture has deterministic filenames, log paths, and validation criteria.

### Step 2: Clean + Save

**Purpose**: Normalize markdown, add source attribution, and save final files.

- Use [Clean, attribute, report](references/clean-and-report.md) to handle content pruning, metadata verification, and run summaries so all evidence stays inside `@ARTIFACT_ROOT`.
