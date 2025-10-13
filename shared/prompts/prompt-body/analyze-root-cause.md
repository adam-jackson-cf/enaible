# Purpose

Discover the fundamental cause of an incident or defect through evidence-based investigation across code changes, execution traces, and environment factors.

## Variables

- `ISSUE_DESCRIPTION` ← first positional argument; required narrative of the problem.
- `VERBOSE_MODE` ← boolean flag set when `--verbose` is present.
- `SCRIPT_PATH` ← resolved root cause analyzer directory.
- `$ARGUMENTS` ← raw argument string for logging.

## Instructions

- ALWAYS collect the user-provided issue description before running analyzers; stop if missing.
- Use the registry-driven analyzers only; do not call module scripts directly.
- Correlate findings across recent code changes, error patterns, and trace outputs; avoid single-source conclusions.
- Clearly distinguish confirmed root causes from contributing factors and unknowns.
- In `VERBOSE_MODE`, capture extended diagnostics (logs, stack traces) and include them in the report.

## Workflow

1. Validate inputs
   - Ensure `ISSUE_DESCRIPTION` is present; prompt for details when absent.
   - Store any CLI flags, notably `--verbose`.
2. Locate analyzer scripts
   - Run `ls .claude/scripts/analyzers/root_cause/*.py || ls "$HOME/.claude/scripts/analyzers/root_cause/"`; if both fail, prompt the user for a path containing `trace_execution.py`, `recent_changes.py`, and `error_patterns.py`, and exit if none is provided.
3. Prepare environment
   - Compute `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
4. Execute automated investigation
   - Run sequentially:
     - `root_cause:trace_execution`
     - `root_cause:recent_changes`
     - `root_cause:error_patterns`
   - Store JSON outputs and note relevant timestamps.
5. Analyze results
   - Correlate change timelines with error occurrences.
   - Map stack traces to code locations and execution paths.
   - Identify recurring error signatures and environmental triggers.
   - In `VERBOSE_MODE`, gather additional diagnostics (process logs, tracing output, profiling data).
6. Perform causal reasoning
   - Apply techniques such as the Five Whys, timeline reconstruction, and hypothesis testing.
   - Differentiate primary root cause(s) from secondary contributing factors.
7. Recommend remediation
   - Propose fixes, regression tests, and preventive measures.
   - Surface open questions or missing data that requires follow-up.
8. Deliver report
   - Summarize evidence, findings, and next actions in a structured format.
   - Attach analyzer outputs or reference paths for traceability.

## Output

```md
# RESULT

- Summary: Root cause identified for "<ISSUE_DESCRIPTION>".

## EVIDENCE

- Recent Changes: <commit ids / files>
- Error Patterns: <signature, frequency>
- Execution Trace: <primary failure point>
- Environment Factors: <config, dependency versions>

## ROOT CAUSE

1. <Primary cause with supporting evidence>
2. <Contributing factor(s)>

## REMEDIATION PLAN

- Fix: <action items with owners or files>
- Verification: <tests, monitors, checkpoints>
- Preventive Measures: <telemetry, guardrails, process updates>

## ATTACHMENTS

- root_cause:trace_execution → <path>
- root_cause:recent_changes → <path>
- root_cause:error_patterns → <path>
```

## Examples

```bash
# Investigate a crash reported in production
/analyze-root-cause "API returns 500 when updating invoices"

# Capture extended diagnostics
/analyze-root-cause "Payment queue stuck in processing" --verbose
```
