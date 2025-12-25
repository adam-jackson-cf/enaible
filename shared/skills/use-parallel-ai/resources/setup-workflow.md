# Purpose

Install and configure the Parallel AI CLI for web intelligence operations.

## Instructions

- Verify Python 3.12+ and uv are available before proceeding.
- Never edit shell config files directly.
- Install the CLI from `tools/parallel` using uv.
- Validate the CLI with `parallel --help`.
- Pause and @ASK_USER_CONFIRMATION at the checkpoints.

## Workflow

1. **Check prerequisites**
   - Verify uv is available: `command -v uv`
   - Check Python version: `python3 --version` (must be 3.12+)

2. **Check API key**
   - Look for `PARALLEL_API_KEY` in environment: `echo $PARALLEL_API_KEY`
   - If not set, pause and @ASK_USER_CONFIRMATION before proceeding.

3. **Install package**
   - Navigate to tools/parallel: `cd tools/parallel`
   - Run uv sync: `uv sync`

4. **Verify installation**
   - Test CLI: `uv run --directory tools/parallel parallel --help`
   - Pause and @ASK_USER_CONFIRMATION before continuing.

5. **Document commands**
   - Update system instructions (CLAUDE.md/AGENTS.md) with the command reference.

6. **Test connectivity (optional)**
   - Pause and @ASK_USER_CONFIRMATION before running a test search.
   - `uv run --directory tools/parallel parallel search "test query" --max-results 1`

## Deterministic references

Command implementations are mirrored in `scripts/` for traceability:

- `scripts/parallel_search.py`
- `scripts/parallel_extract.py`
- `scripts/parallel_task.py`
- `scripts/parallel_findall.py`
- `scripts/parallel_status.py`
