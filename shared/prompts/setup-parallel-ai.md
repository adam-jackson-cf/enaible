# Purpose

Validate Parallel AI API access and document the local scripts for search, extraction, research tasks, and entity discovery.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)

### Derived (internal)

- @SCOPE = <user|project> — installation scope from user choice
- @SYSTEMS = <filename> — system instructions file (CLAUDE.md or AGENTS.md depending on target)
- @SYSTEMS_PATH = <path> — full path to systems file based on scope
- @PYTHON_CMD = <python command> — validated Python command (python, python3, or full path)

## Instructions

- ALWAYS verify Python 3.12+ and confirm the Python command (`python`, `python3`, or full path) before proceeding.
- Set @PYTHON_CMD to the validated Python command for all script invocations.
- NEVER modify shell configuration files (.zshrc, .bashrc, etc.) directly.
- DO NOT install anything; Parallel AI is accessed via the external API.
- Verify `PARALLEL_API_KEY` before attempting any API request.
- Document commands in @SYSTEMS.md for reference (project or user level).
- Respect STOP confirmations unless @AUTO is provided.

## Workflow

1. Check prerequisites
   - Confirm Python command with the user: `python --version` or `python3 --version` (must be 3.12+)
   - Set @PYTHON_CMD to the validated command.
   - If Python is missing or outdated, exit with instructions to install Python 3.12+.
2. Check API key
   - Look for `PARALLEL_API_KEY` in environment: `echo $PARALLEL_API_KEY`
   - If not set, **STOP (skip when @AUTO):** "PARALLEL_API_KEY not set. Get your key from platform.parallel.ai and add to shell config. Continue anyway? (y/n)"
   - If user declines, exit with instructions to add API key.
3. Verify scripts availability
   - Confirm the Parallel AI scripts are available in the installed skill directory.
   - If missing, instruct the user to run the appropriate `enaible install` flow for their system.
4. Validate connectivity (optional)
   - **STOP (skip when @AUTO):** "Test API connectivity with a simple search? (y/n)"
   - If approved and PARALLEL_API_KEY is set, run a test search from the skill directory:
     `@PYTHON_CMD scripts/parallel_search.py "test query" --max-results 1`
   - Verify response is received successfully.
5. Update @SYSTEMS.md
   - **STOP (skip when @AUTO):** "Document Parallel AI tools at project level (./@SYSTEMS.md) or user level ({{ system.user_scope_dir }}/@SYSTEMS.md)?"
   - Based on user choice, set @SYSTEMS_PATH:
     - Project: `./@SYSTEMS.md` (repo root)
     - User: `{{ system.user_scope_dir }}/@SYSTEMS.md`
   - Add or update Parallel AI documentation section at @SYSTEMS_PATH:

   ````md
   ### When you need web intelligence or research capabilities

   If `--search`, `--extract`, `--task`, or `--findall` is included in a user request, use the Parallel AI scripts.

   **Requires:** `PARALLEL_API_KEY` environment variable (get from platform.parallel.ai)

   **Usage:** run commands from the skill directory:
   `@PYTHON_CMD scripts/parallel_<command>.py`

   **Available Commands:**

   - `parallel_search.py` — Web search with natural language
     - Options: `--query/-q` (repeatable), `--max-results N`, `--format json|markdown`

   - `parallel_extract.py` — Extract content from URLs to markdown
     - Options: `--objective "focus"`, `--full-content`, `--format json|markdown`

   - `parallel_task.py` — Create enrichment/research task (async)
     - Options: `--schema "output desc"`, `--processor base|core`
     - Returns: run_id (use `parallel_status.py result` to get output)

   - `parallel_findall.py` — Discover entities matching criteria (async)
     - Options: `--entity type`, `--condition` (repeatable), `--limit N`, `--generator base|core|pro|preview`
     - Returns: findall_id (use `parallel_status.py result` to get output)

   - `parallel_status.py status <id>` — Check async operation status
   - `parallel_status.py result <id>` — Fetch completed results

   **Example Usage:**

   ```bash
   # Search the web
   @PYTHON_CMD scripts/parallel_search.py "latest AI research papers on RAG"

   # Extract content from URL
   @PYTHON_CMD scripts/parallel_extract.py https://example.com --objective "key findings"

   # Generate dataset of entities
   @PYTHON_CMD scripts/parallel_findall.py "AI startups in San Francisco" --entity company --limit 50
   ```
   ````

6. Validate setup
   - Confirm API key is set.
   - Confirm scripts are accessible in the skill directory.
   - Provide usage examples and next steps.

## Output

```md
# RESULT

- Summary: Parallel AI API access validated and scripts documented

## DETAILS

- Python Command: <python|python3|full path>
- API Key Status: <set|not set - configure PARALLEL_API_KEY>
- Documentation: @SYSTEMS_PATH updated

## AVAILABLE COMMANDS

- parallel_search.py — Web search with natural language
- parallel_extract.py — Extract content from URLs
- parallel_task.py — Create enrichment/research tasks
- parallel_findall.py — Discover entities at scale
- parallel_status.py — Check status or fetch results

## VALIDATION

- API key: <✓ set | ⚠ missing>
- Script availability: <✓ available | ⚠ missing>
- API connectivity: <✓ verified | ⚠ not tested>

## NEXT STEPS

1. Set PARALLEL_API_KEY if not already configured:
   `export PARALLEL_API_KEY="your-key-here"`
2. Test with a search:
   `@PYTHON_CMD scripts/parallel_search.py "test query" --max-results 1`
3. Review @SYSTEMS_PATH for command reference
```
