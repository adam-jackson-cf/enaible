---
name: use-parallel-ai
description: Install and use the Parallel AI CLI for web intelligence tasks (search, extract, task, findall) with verified setup and user-confirmed checkpoints.
compatibility: Requires Python 3.12+, uv, and PARALLEL_API_KEY with access to api.parallel.ai.
allowed-tools: Bash Read Write
---

# Use Parallel AI

Guide for installing and operating the Parallel AI CLI. Use when the user requests web search, content extraction, enrichment tasks, or entity discovery.

## Prerequisites

- `uv` installed
- Python 3.12+
- `PARALLEL_API_KEY` set in environment

## Resources

| Goal                       | Resource                                                     |
| -------------------------- | ------------------------------------------------------------ |
| Install and verify the CLI | [resources/setup-workflow.md](resources/setup-workflow.md)   |
| Command reference          | [resources/cli-reference.md](resources/cli-reference.md)     |
| Troubleshooting            | [resources/troubleshooting.md](resources/troubleshooting.md) |

## Scripts

Command implementations are copied into `scripts/` for reference:

- `scripts/parallel_search.py`
- `scripts/parallel_extract.py`
- `scripts/parallel_task.py`
- `scripts/parallel_findall.py`
- `scripts/parallel_status.py`
