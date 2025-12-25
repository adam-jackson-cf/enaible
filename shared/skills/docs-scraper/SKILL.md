---
name: docs-scraper
description: Fetch documentation from URLs and save clean markdown files for offline reference; use when the user wants docs scraped, archived, or analyzed from web sources.
compatibility: Requires network access plus uv and the Enaible CLI available in the workspace.
allowed-tools: Bash Read Write
---

# Docs Scraper

Capture documentation from URLs and save it as readable, well-structured markdown for offline use.

## When to use

- The user asks to scrape, archive, or capture documentation from one or more URLs.
- The user wants documentation converted to markdown for local analysis or sharing.

## Prerequisites

- List of source URLs.
- Write access to the output directory.
- `uv` and the Enaible CLI available in the workspace.

## Resources

| Goal                         | Resource                                                               |
| ---------------------------- | ---------------------------------------------------------------------- |
| End-to-end workflow          | [resources/docs-scrape-workflow.md](resources/docs-scrape-workflow.md) |
| Command reference + examples | [resources/cli-reference.md](resources/cli-reference.md)               |

## Orchestration Overview

### Stage 1: Intake

**Purpose**: Confirm URLs, output directory, and naming expectations.
**Details**: [resources/docs-scrape-workflow.md](resources/docs-scrape-workflow.md)

### Stage 2: Fetch URL content

**Purpose**: Run `enaible docs_scrape` for each URL and validate outputs.
**Details**: [resources/cli-reference.md](resources/cli-reference.md)

### Stage 3: Process + clean

**Purpose**: Reformat content into clean markdown and remove navigation clutter.
**Details**: [resources/cli-reference.md](resources/cli-reference.md)

### Stage 4: Determine filenames

**Purpose**: Derive kebab-case filenames from the URL path or page title.
**Details**: [resources/cli-reference.md](resources/cli-reference.md)

### Stage 5: Save documentation

**Purpose**: Write the cleaned markdown to the output directory.
**Details**: [resources/cli-reference.md](resources/cli-reference.md)

### Stage 6: Verify + report

**Purpose**: Confirm the file exists and summarize what was saved.
**Details**: [resources/cli-reference.md](resources/cli-reference.md)
