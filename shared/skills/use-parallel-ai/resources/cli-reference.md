# Parallel AI Script Reference

Use the standalone scripts via the Python command you confirmed in setup:

```bash
$PYTHON_CMD scripts/parallel_search.py <args>
```

## Commands

### search

- Script: `scripts/parallel_search.py`
- Usage: `$PYTHON_CMD scripts/parallel_search.py "objective"`
- Options: `--query/-q` (repeatable), `--max-results`, `--format json|markdown`

### extract

- Script: `scripts/parallel_extract.py`
- Usage: `$PYTHON_CMD scripts/parallel_extract.py <url>`
- Options: `--objective`, `--full-content`, `--format json|markdown`

### task

- Script: `scripts/parallel_task.py`
- Usage: `$PYTHON_CMD scripts/parallel_task.py "input"`
- Options: `--schema/-s`, `--processor base|core`

### findall

- Script: `scripts/parallel_findall.py`
- Usage: `$PYTHON_CMD scripts/parallel_findall.py "objective" --entity company`
- Options: `--condition/-c` (repeatable), `--limit`, `--generator base|core|pro|preview`

### status

- Script: `scripts/parallel_status.py`
- Usage: `$PYTHON_CMD scripts/parallel_status.py status <run_id> [--type task|findall]`

### result

- Script: `scripts/parallel_status.py`
- Usage: `$PYTHON_CMD scripts/parallel_status.py result <run_id> [--type task|findall] [--output file] [--format json|markdown]`
