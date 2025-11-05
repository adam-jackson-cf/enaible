# analyze-root-cause v1.0

# Purpose

Discover the fundamental cause of an incident or defect through evidence-based investigation across code changes, execution traces, and environment factors.

## Variables

### Required

- @ISSUE_DESCRIPTION = $1 — description of the defect or incident

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @TARGET_PATH = --target-path — path to analyze; defaults to repo root
- @VERBOSE = --verbose — enable verbose diagnostics capture
- @MIN_SEVERITY = --min-severity — defaults to "high"; accepts critical|high|medium|low
- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude (e.g., test_codebase/\*\*)

### Derived (internal)

- @ARTIFACT_ROOT — timestamped artifacts path used for evidence capture

## Instructions

- ALWAYS capture the issue description before running analyzers; stop if details are insufficient.
- Validate @TARGET_PATH (default `.`) exists and is readable before executing analyzers.
- Use Enaible analyzers exclusively—do not probe for scripts or import modules manually.
- Persist artifacts under `.enaible/artifacts/analyze-root-cause/` for traceability.
- Correlate findings across recent changes, error patterns, and traces; clearly separate hypotheses from confirmed evidence.
- When @VERBOSE is provided, gather extended diagnostics (logs, stack traces) and document how they influence the conclusion.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. **Validate inputs**
   - Confirm @ISSUE_DESCRIPTION is present. If missing, request more information or explicit approval to proceed with assumptions.
   - Resolve @TARGET_PATH (default `.`) and ensure it is readable.
   - Note whether @VERBOSE is enabled.
2. **Establish artifacts directory**
   - Set `@ARTIFACT_ROOT=".enaible/artifacts/analyze-root-cause/$(date -u +%Y%m%dT%H%M%SZ)"` and create it.
3. **Run automated analyzers**

   - Execute each Enaible command, storing the JSON output:

     ```bash
     uv run --project tools/enaible enaible analyzers run root_cause:trace_execution \
       --target "@TARGET_PATH" \
       --out "@ARTIFACT_ROOT/root-cause-trace.json"

     uv run --project tools/enaible enaible analyzers run root_cause:recent_changes \
       --target "@TARGET_PATH" \
       --out "@ARTIFACT_ROOT/root-cause-recent-changes.json"

     uv run --project tools/enaible enaible analyzers run root_cause:error_patterns \
       --target "@TARGET_PATH" \
       --out "@ARTIFACT_ROOT/root-cause-error-patterns.json"
     ```

   - When @VERBOSE is provided, capture additional evidence (stack traces, logs) and note their locations inside `ARTIFACT_ROOT`.
   - Add `--exclude "<glob>"` or adjust `--min-severity` to limit noise while focusing on the suspected components.
   - If any invocation fails, review options with `uv run --project tools/enaible enaible analyzers run --help` before retrying.

4. **Analyze results**
   - Correlate change timelines with error occurrences.
   - Map stack traces to code locations and execution paths.
   - Identify recurring error signatures and environment triggers.
5. **Perform causal reasoning**
   - Apply techniques such as Five Whys, timeline reconstruction, and hypothesis testing.
   - Distinguish primary root causes from contributing factors or unknowns that require follow-up.
6. **Recommend remediation**
   - Propose fixes, regression tests, and preventive measures.
   - Surface open questions or missing data that must be resolved before rollout.
7. **Deliver report**
   - Summarize evidence, findings, and next actions in a structured format.
   - Reference analyzer outputs using the artifact paths recorded earlier.

## Output

```md
# RESULT

- Summary: Root cause identified for "<ISSUE_DESCRIPTION>".
- Artifacts: `.enaible/artifacts/analyze-root-cause/<timestamp>/`

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

- root_cause:trace_execution → `.enaible/artifacts/analyze-root-cause/<timestamp>/root-cause-trace.json`
- root_cause:recent_changes → `.enaible/artifacts/analyze-root-cause/<timestamp>/root-cause-recent-changes.json`
- root_cause:error_patterns → `.enaible/artifacts/analyze-root-cause/<timestamp>/root-cause-error-patterns.json`
```

## Examples

```bash
# Investigate a crash reported in production
/analyze-root-cause "API returns 500 when updating invoices"

# Capture extended diagnostics
/analyze-root-cause "Payment queue stuck in processing" --verbose
```

<!-- generated: enaible -->
