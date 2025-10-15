# Purpose

Evaluate project architecture for scalability, maintainability, and design-pattern alignment while producing actionable recommendations.

## Variables

- `TARGET_PATH` ← $1 (defaults to `./`).

## Instructions

- ALWAYS verify analyzer scripts exist and are readable before running any checks.
- NEVER substitute per-module CLIs; use the registry-driven runner exclusively.
- Capture each analyzer’s JSON output for reporting; do not discard raw metrics.
- Assess architecture dimensions using both quantitative (script output) and qualitative reasoning.
- Summaries must connect findings to concrete improvement recommendations.

## Workflow

1. Locate analyzer scripts
   - Run `ls .claude/scripts/analyzers/architecture/*.py || ls "$HOME/.claude/scripts/analyzers/architecture/"`; if both fail, exit and request a valid path.
   - When scripts are missing locally, prompt the user for a directory containing `pattern_evaluation.py`, `scalability_check.py`, and `coupling_analysis.py`, then set `SCRIPT_PATH`.
2. Prepare environment
   - Derive `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"`.
   - Run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
3. Run automated analyzers
   - Execute sequentially:
     - `architecture:patterns`
     - `architecture:scalability`
     - `architecture:coupling`
     - `architecture:dependency`
   - Store JSON reports alongside timestamps and command invocations.
4. Synthesize quantitative findings
   - Extract metrics: service boundaries, coupling indices, dependency depth, scalability bottlenecks.
   - Highlight hotspots exceeding thresholds (complexity, fan-in/out, layering).
5. Perform qualitative assessment
   - Map findings to architectural concerns: service boundary clarity, SOLID adherence, data flow consistency, deployment topology.
   - Identify design-pattern compliance and anti-patterns with traceable evidence.
6. Draft recommendations
   - Prioritize remediation steps with impact vs. effort notes.
   - Include architecture diagrams or hierarchy sketches when beneficial.
7. Deliver final report
   - Provide structured summary with metrics, risk assessment, and next actions.
   - Attach raw analyzer outputs or inlined excerpts in an appendix section.

## Output

```md
# RESULT

- Summary: Architecture assessment completed for <TARGET_PATH>.

## FINDINGS

- Service Boundaries: <observation + metric>
- Coupling & Cohesion: <observation + metric>
- Scalability Risks: <observation + metric>
- Data Flow & State: <observation + metric>

## RECOMMENDATIONS

1. <Highest-priority improvement with rationale and expected impact>
2. <Next action>

## ATTACHMENTS

- architecture:patterns → <path to JSON>
- architecture:scalability → <path to JSON>
- architecture:coupling → <path to JSON>
- architecture:dependency → <path to JSON>
```

## Examples

```bash
# Analyze repository architecture from the current directory
/analyze-architecture .

# Target a specific service directory
/analyze-architecture services/api
```
