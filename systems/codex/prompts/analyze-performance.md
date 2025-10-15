<!-- generated: enaible -->
<!-- codex prompt (frontmatter-free) -->

# analyze-performance v1.0

# Purpose

Identify performance bottlenecks across backend, frontend, and data layers using automated analyzers coupled with contextual investigation.

## Variables

- `$TARGET_PATH` ← $1 (defaults to `./`).

## Instructions

- ALWAYS leverage Enaible analyzers; avoid manual script path discovery.
- Persist analyzer results under `.enaible/artifacts/analyze-performance/` and cite them in the final report.
- Investigate bottlenecks holistically (compute, IO, frontend rendering, data access, configuration).
- Tie each recommendation to measurable outcomes and validation steps.

## Workflow

1. **Establish artifacts directory**
   - Set `ARTIFACT_ROOT=".enaible/artifacts/analyze-performance/$(date -u +%Y%m%dT%H%M%SZ)"` and create it.
2. **Run Enaible performance analyzers**

   - Execute the analyzer suite, persisting JSON outputs:

     ```bash
     uv run enaible analyzers run performance:ruff \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/performance-ruff.json"

     uv run enaible analyzers run performance:frontend \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/performance-frontend.json"

     uv run enaible analyzers run performance:sqlglot \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/performance-sqlglot.json"

     uv run enaible analyzers run performance:semgrep \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/performance-semgrep.json"
     ```

   - Append `--summary` when triaging large repositories; rerun full reports before publishing.

3. **Aggregate findings**
   - Parse hotspots across layers: backend N+1 patterns, frontend re-render costs, SQL anti-patterns, lint warnings.
   - Map each issue to system components (API endpoints, React routes, migrations, jobs).
4. **Investigate context**
   - Inspect flagged areas for caching gaps, over-fetching, synchronous IO, or configuration constraints.
   - Consider infrastructure contributors (rate limits, autoscaling thresholds, memory footprints).
5. **Prioritize remediations**
   - Group issues by impact (critical, high, medium) and outline validation experiments (profiling, load tests).
6. **Produce report**
   - Summarize bottlenecks, attach metric tables, and define success metrics for remediation.

## Output

```md
# RESULT

- Summary: Performance analysis completed for <TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-performance/<timestamp>/`

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

- performance:ruff → `.enaible/artifacts/analyze-performance/<timestamp>/performance-ruff.json`
- performance:frontend → `.enaible/artifacts/analyze-performance/<timestamp>/performance-frontend.json`
- performance:sqlglot → `.enaible/artifacts/analyze-performance/<timestamp>/performance-sqlglot.json`
- performance:semgrep → `.enaible/artifacts/analyze-performance/<timestamp>/performance-semgrep.json`
```

## Examples

```bash
# Run full performance assessment
/analyze-performance .

# Target a service directory
/analyze-performance services/api
```
