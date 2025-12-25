---
name: use-parallel-ai
description: Use the Parallel AI API scripts for web search, extraction, enrichment tasks, and entity discovery with verified API access and user-confirmed checkpoints.
compatibility: Requires Python 3.12+ and PARALLEL_API_KEY with access to api.parallel.ai.
allowed-tools: Bash Read Write
---

# Use Parallel AI

Guide for accessing the Parallel AI API via local scripts. Use when the user requests web search, content extraction, enrichment tasks, or entity discovery.

## Prerequisites

- Python 3.12+
- `PARALLEL_API_KEY` set in environment
- Network access to api.parallel.ai

## Resources

| Goal                       | Resource                                                     |
| -------------------------- | ------------------------------------------------------------ |
| Preflight + API validation | [resources/setup-workflow.md](resources/setup-workflow.md)   |
| Command reference          | [resources/cli-reference.md](resources/cli-reference.md)     |
| Troubleshooting            | [resources/troubleshooting.md](resources/troubleshooting.md) |

## Orchestration Overview

### Stage 1: Preflight

**Purpose**: Confirm Python command and API access before running scripts.
**Details**: [resources/setup-workflow.md](resources/setup-workflow.md)

### Stage 2: Execute request

**Purpose**: Run the matching script for the user’s request (search, extract, task, findall).
**Details**: [resources/cli-reference.md](resources/cli-reference.md)

### Stage 3: Validate results

**Purpose**: Summarize outputs and confirm if follow-up runs are needed.
**Details**: [resources/troubleshooting.md](resources/troubleshooting.md)

## Scripts

Command implementations are copied into `scripts/` for reference:

- `scripts/parallel_search.py`
- `scripts/parallel_extract.py`
- `scripts/parallel_task.py`
- `scripts/parallel_findall.py`
- `scripts/parallel_status.py`
