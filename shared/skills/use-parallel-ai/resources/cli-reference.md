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
- Examples:
  - `$PYTHON_CMD scripts/parallel_search.py "latest PCI compliance updates" --max-results 5`
  - `$PYTHON_CMD scripts/parallel_search.py "edge caching best practices" -q "CDN cache invalidation" --format markdown`

### extract

- Script: `scripts/parallel_extract.py`
- Usage: `$PYTHON_CMD scripts/parallel_extract.py <url>`
- Options: `--objective`, `--full-content`, `--format json|markdown`
- Examples:
  - `$PYTHON_CMD scripts/parallel_extract.py https://example.com --objective "key takeaways" --format markdown`
  - `$PYTHON_CMD scripts/parallel_extract.py https://example.com/docs --full-content`

### task

- Script: `scripts/parallel_task.py`
- Usage: `$PYTHON_CMD scripts/parallel_task.py "input"`
- Options: `--schema/-s`, `--processor base|core`
- Examples:
  - `$PYTHON_CMD scripts/parallel_task.py "OpenAI" --schema "funding rounds, valuation, top investors"`
  - `$PYTHON_CMD scripts/parallel_task.py "US SOC 2 requirements" --schema "summary + key controls" --processor core`

### findall

- Script: `scripts/parallel_findall.py`
- Usage: `$PYTHON_CMD scripts/parallel_findall.py "objective" --entity company`
- Options: `--condition/-c` (repeatable), `--limit`, `--generator base|core|pro|preview`
- Examples:
  - `$PYTHON_CMD scripts/parallel_findall.py "AI observability tools" --entity company --limit 25`
  - `$PYTHON_CMD scripts/parallel_findall.py "fintech startups" --entity company -c "focus on SMBs" -c "founded after 2020"`

### status

- Script: `scripts/parallel_status.py`
- Usage: `$PYTHON_CMD scripts/parallel_status.py status <run_id> [--type task|findall]`
- Examples:
  - `$PYTHON_CMD scripts/parallel_status.py status trun_1234567890`
  - `$PYTHON_CMD scripts/parallel_status.py status fa_abcdef1234 --type findall`

### result

- Script: `scripts/parallel_status.py`
- Usage: `$PYTHON_CMD scripts/parallel_status.py result <run_id> [--type task|findall] [--output file] [--format json|markdown]`
- Examples:
  - `$PYTHON_CMD scripts/parallel_status.py result trun_1234567890 --format markdown`
  - `$PYTHON_CMD scripts/parallel_status.py result fa_abcdef1234 --type findall --output findall.json`
