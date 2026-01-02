# Purpose

Preflight checks for using Parallel AI's API via the local scripts (search, extract, task, findall).

## Instructions

- Confirm the Python command with the user; do not assume `python3`.
- Do not install anything for this skill; it uses the external Parallel AI API.
- Never edit shell config files directly.
- Ensure `PARALLEL_API_KEY` is set before making API calls.
- Pause and @ASK_USER_CONFIRMATION at the checkpoints.

## Workflow

1. **Set Python command**
   - Ask the user which Python command to use (e.g., `python` or a full path).
   - Verify version: `<python-cmd> --version` (must be 3.12+).
   - Export the working command: `export PYTHON_CMD=<python-cmd>`.
   - Pause and @ASK_USER_CONFIRMATION before moving on.

2. **Check API key**
   - Look for `PARALLEL_API_KEY` in environment: `echo $PARALLEL_API_KEY`.
   - If not set, pause and @ASK_USER_CONFIRMATION before proceeding.

3. **Test connectivity (optional)**
   - Pause and @ASK_USER_CONFIRMATION before running a test search.
   - `"$PYTHON_CMD" scripts/parallel_search.py "test query" --max-results 1`

4. **Document commands**
   - Update system instructions (CLAUDE.md/AGENTS.md) with the command reference.

## Deterministic references

Command implementations are mirrored in `scripts/` for traceability:

- `scripts/parallel_search.py`
- `scripts/parallel_extract.py`
- `scripts/parallel_task.py`
- `scripts/parallel_findall.py`
- `scripts/parallel_status.py`
