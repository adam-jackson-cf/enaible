# Purpose

Identify performance bottlenecks across backend, frontend, and data layers using automated analyzers coupled with contextual investigation.

## Variables

- `$TARGET_PATH` ← $1 (defaults to `./`).

## Instructions

- ALWAYS execute the registry-driven analyzers; never call the individual modules directly.
- Treat analyzer outputs as evidence—cite metrics when highlighting bottlenecks.
- Consider database, frontend, algorithmic, and network layers; avoid tunnel vision.
- Tie each recommendation to measurable performance goals.
- Document assumptions and required follow-up experiments (profiling, load tests).

## Workflow

1. Locate analyzer scripts
   - Run `ls .codex/scripts/analyzers/performance/*.py || ls "$HOME/.codex/scripts/analyzers/performance/"`; if both fail, prompt for a directory containing `ruff_analyzer.py`, `analyze_frontend.py`, and `sqlglot_analyzer.py`, then exit if none is provided.
2. Prepare environment
   - Derive `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
3. Run automated analyzers
   - Execute sequentially:
     - `performance:ruff`
     - `performance:frontend`
     - `performance:sqlglot`
     - `performance:semgrep` (universal heuristics; deferred install if missing)
   - Save JSON outputs and note start/end timestamps.
4. Aggregate findings
   - Parse slow hotspots (function-level metrics, lint warnings, SQL anti-patterns).
   - Map findings to system components (API endpoints, React routes, SQL migrations).
5. Investigate context
   - Examine code around flagged areas for caching gaps, unnecessary re-renders, unindexed queries.
   - Consider infrastructure or configuration contributors (rate limits, memory caps).
6. Prioritize remediations
   - Group issues by impact: critical (user-facing latency, OOM risks), high, medium.
   - Recommend targeted actions (index creation, memoization, batching, background jobs).
7. Produce report
   - Provide a structured summary, include metric tables, and outline validation steps (profiling, load tests).

## Output

```md
# RESULT

- Summary: Performance analysis completed for <TARGET_PATH>.

## BOTTLENECKS

| Layer    | Location              | Finding                            | Evidence Source      |
| -------- | --------------------- | ---------------------------------- | -------------------- |
| Backend  | api/orders.py#L142    | N+1 query detected                 | performance:sqlglot  |
| Frontend | src/App.tsx#L88       | Expensive re-render (missing memo) | performance:frontend |
| Database | migrations/202310.sql | Full table scan on large dataset   | performance:sqlglot  |

## RECOMMENDED ACTIONS

1. <High priority optimization with expected impact and verification plan>
2. <Secondary optimization>

## VALIDATION PLAN

- Benchmark: <command or script>
- Success Criteria: <quantitative target>

## ATTACHMENTS

- performance:ruff → <path>
- performance:frontend → <path>
- performance:sqlglot → <path>
- performance:semgrep → <path>
```

## Examples

```bash
# Run full performance assessment
/analyze-performance .

# Target a service directory
/analyze-performance services/api
```
