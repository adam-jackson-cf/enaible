# Parallel AI CLI Reference

Use the CLI via:

```bash
uv run --directory tools/parallel parallel <command>
```

## Commands

### search

- Script: `scripts/parallel_search.py`
- Usage: `parallel search "objective"`
- Options: `--query/-q` (repeatable), `--max-results`, `--format json|markdown`

### extract

- Script: `scripts/parallel_extract.py`
- Usage: `parallel extract <url>`
- Options: `--objective`, `--full-content`, `--format json|markdown`

### task

- Script: `scripts/parallel_task.py`
- Usage: `parallel task "input"`
- Options: `--schema/-s`, `--processor base|core`

### findall

- Script: `scripts/parallel_findall.py`
- Usage: `parallel findall "objective" --entity company`
- Options: `--condition/-c` (repeatable), `--limit`, `--generator base|core|pro`

### status

- Script: `scripts/parallel_status.py`
- Usage: `parallel status <run_id> [--type task|findall]`

### result

- Script: `scripts/parallel_status.py`
- Usage: `parallel result <run_id> [--type task|findall] [--output file] [--format json|markdown]`
