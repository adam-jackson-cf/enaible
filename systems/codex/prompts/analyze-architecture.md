<!-- generated: enaible -->
<!-- codex prompt (frontmatter-free) -->

# analyze-architecture v1.0

## Variables

| Token          | Type                     | Description                                       |
| -------------- | ------------------------ | ------------------------------------------------- |
| `$TARGET_PATH` | positional #1 (REQUIRED) | Path to analyze; defaults to the current project. |

# Purpose

Evaluate project architecture for scalability, maintainability, and design-pattern alignment while producing actionable recommendations.

## Instructions

- ALWAYS execute Enaible analyzers; skip legacy script discovery entirely.
- Persist all analyzer outputs under `.enaible/artifacts/analyze-architecture/` for traceability.
- Combine quantitative metrics with qualitative reasoning before drawing conclusions.
- Tie every recommendation to concrete code references and measurable success criteria.

## Workflow

1. **Establish artifacts directory**
   - Set `ARTIFACT_ROOT=".enaible/artifacts/analyze-architecture/$(date -u +%Y%m%dT%H%M%SZ)"` and create it.
2. **Run automated analyzers**

   - Execute each Enaible command, storing the JSON output:

     ```bash
     uv run enaible analyzers run architecture:patterns \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/architecture-patterns.json"

     uv run enaible analyzers run architecture:scalability \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/architecture-scalability.json"

     uv run enaible analyzers run architecture:coupling \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/architecture-coupling.json"

     uv run enaible analyzers run architecture:dependency \
       --target "$TARGET_PATH" \
       --out "$ARTIFACT_ROOT/architecture-dependency.json"
     ```

   - Use `--summary` for quick reconnaissance when working with large codebases.

3. **Synthesize quantitative findings**
   - Extract metrics related to service boundaries, coupling indices, dependency depth, and scalability bottlenecks.
   - Flag hotspots exceeding organizational thresholds (fan-in/out, layering violations, shared-state risks).
4. **Perform qualitative assessment**
   - Map results to architecture lenses: domain boundaries, SOLID alignment, data flow consistency, observability posture.
   - Document gaps in diagrams, ADRs, or ownership models that compound technical risk.
5. **Draft recommendations**
   - Prioritize remediation steps with impact vs. effort notes and include rollout considerations.
   - Propose quick wins, medium-term refactors, and strategic investments.
6. **Deliver final report**
   - Provide a structured summary with metrics, risk assessment, and next actions.
   - Reference analyzer evidence paths from `ARTIFACT_ROOT`.

## Output

```md
# RESULT

- Summary: Architecture assessment completed for <TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-architecture/<timestamp>/`

## FINDINGS

- Service Boundaries: <observation + metric>
- Coupling & Cohesion: <observation + metric>
- Scalability Risks: <observation + metric>
- Data Flow & State: <observation + metric>

## RECOMMENDATIONS

1. <Highest-priority improvement with rationale and expected impact>
2. <Next action>

## ATTACHMENTS

- architecture:patterns → `.enaible/artifacts/analyze-architecture/<timestamp>/architecture-patterns.json`
- architecture:scalability → `.enaible/artifacts/analyze-architecture/<timestamp>/architecture-scalability.json`
- architecture:coupling → `.enaible/artifacts/analyze-architecture/<timestamp>/architecture-coupling.json`
- architecture:dependency → `.enaible/artifacts/analyze-architecture/<timestamp>/architecture-dependency.json`
```

## Examples

```bash
# Analyze repository architecture from the current directory
/analyze-architecture .

# Target a specific service directory
/analyze-architecture services/api
```
