---
name: use-parallel-ai
description: Use the Parallel AI API scripts for web search, extraction, enrichment tasks, and entity discovery with verified API access and user-confirmed checkpoints. USE WHEN the user needs Parallel AI-powered search, extraction, or enrichment workflows.
compatibility: Requires Python 3.12+, `PARALLEL_API_KEY` credentials, and network egress to `api.parallel.ai`.
allowed-tools: @BASH @READ @WRITE
---

# Use Parallel AI

Guide for accessing the Parallel AI API via local scripts with deterministic checkpoints.

- The user wants Parallel AI search, extraction, enrichment, or entity-discovery output.
- You have verified API credentials (`PARALLEL_API_KEY`) and network access to `api.parallel.ai`.
- You must capture evidence (inputs, responses, status) for each request and confirm user intent between scripted checkpoints.

## Need to...? Read This

| Goal                       | Reference                                                      |
| -------------------------- | -------------------------------------------------------------- |
| Preflight + API validation | [references/setup-workflow.md](references/setup-workflow.md)   |
| Command reference          | [references/cli-reference.md](references/cli-reference.md)     |
| Troubleshooting            | [references/troubleshooting.md](references/troubleshooting.md) |

## Workflow

Full command sequences, environment expectations, and checkpoint prompts are documented inside the reference files.

### Step 0: Preflight

**Purpose**: Confirm Python command, API key, network access, and script availability before running requests.

- Run the setup workflow checks to verify `PARALLEL_API_KEY`, Python 3.12+ (via `python` or `uv run python`), network egress to `api.parallel.ai`, and that all helper scripts in `scripts/` are accessible/executable.
- Follow the `@ASK_USER_CONFIRMATION` prompts captured in [references/setup-workflow.md](references/setup-workflow.md) for any risky operations.

### Step 1: Execute request

**Purpose**: Run the appropriate script for the user’s request (search, extract, task, findall).

- Use `uv run` or direct Python execution to call the script with the required arguments.
- Capture request JSON, response payloads, and logs under the working directory.
- Command patterns and arguments live in [references/cli-reference.md](references/cli-reference.md).

### Step 2: Validate results

**Purpose**: Summarize outputs, confirm success criteria, and determine follow-up calls.

- Review API status, rate limits, and structured outputs.
- Present results to the user and flag any manual steps using the troubleshooting reference.
- Diagnostics and recovery steps: [references/troubleshooting.md](references/troubleshooting.md).

## Scripts

Command implementations are copied into `scripts/` for reference:

- `scripts/parallel_search.py`
- `scripts/parallel_extract.py`
- `scripts/parallel_task.py`
- `scripts/parallel_findall.py`
- `scripts/parallel_status.py`
