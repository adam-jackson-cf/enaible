<!-- generated: enaible -->
<!-- codex prompt (frontmatter-free) -->

# plan-refactor v1.0

## Variables

### Required

- @REFACTOR_SCOPE = $1 — area or component to refactor

# plan-refactor v0.3

## Purpose

Design a staged refactoring plan that reduces technical debt, mitigates risk, and delivers measurable quality improvements.

## Instructions

- Execute the workflow phases in order and honor each STOP confirmation.
- Use Enaible analyzers for evidence gathering; store outputs in `.enaible/artifacts/plan-refactor/`.
- Anchor migration strategies in proven patterns (Strangler Fig, Module Federation, blue-green, etc.).
- Define rollback steps and monitoring at every migration phase.
- Translate the final plan into actionable todos when approved.

## Workflow

1. **Establish artifacts directory**
   - Set `ARTIFACT_ROOT=".enaible/artifacts/plan-refactor/$(date -u +%Y%m%dT%H%M%SZ)"` and create it.
2. **Run automated analyzers**

   - Execute each Enaible command, storing the JSON output:

     ```bash
     uv run --project tools/enaible enaible analyzers run quality:lizard \
       --target "@REFACTOR_SCOPE" \
       --out "$ARTIFACT_ROOT/quality-lizard.json"

     uv run --project tools/enaible enaible analyzers run architecture:coupling \
       --target "@REFACTOR_SCOPE" \
       --out "$ARTIFACT_ROOT/architecture-coupling.json"

     uv run --project tools/enaible enaible analyzers run performance:baseline \
       --target "@REFACTOR_SCOPE" \
       --out "$ARTIFACT_ROOT/performance-baseline.json"
     ```

   - Capture key hotspots, architectural risks, and performance warnings.

3. **Phase 1 — Technical Debt Assessment**
   - Summarize analyzer outputs (complexity spikes, coupling hotspots, perf regressions).
   - Identify the debt themes affecting @REFACTOR_SCOPE.
   - **STOP:** “Technical debt analysis complete. Proceed with strategy development? (y/n)”
4. **Phase 2 — Migration Strategy**
   - Research suitable refactoring patterns and outline phased migration (feature flags, decomposition, deployment plan).
   - Define rollback procedures, monitoring hooks, and stakeholder checkpoints.
   - **STOP:** “Migration strategy defined. Ready to create implementation plan? (y/n)”
5. **Phase 3 — Implementation Planning**
   - Break work into phased milestones with timelines and exit criteria.
   - Run `uv run --project tools/enaible enaible analyzers run quality:coverage --target "@REFACTOR_SCOPE" --out "$ARTIFACT_ROOT/quality-coverage.json"` to inform the testing roadmap.
   - Establish success metrics (complexity targets, performance budgets, velocity impact).
6. **Phase 4 — Finalize report**
   - Summarize assessment, strategy, roadmap, and success metrics.
   - Reference artifacts in `ARTIFACT_ROOT` and note follow-up tasks.

## Output

```md
# RESULT

- Summary: Refactoring plan created for <@REFACTOR_SCOPE>.
- Artifacts: `.enaible/artifacts/plan-refactor/<timestamp>/`

## ASSESSMENT

- Hotspots: <key findings>
- Architecture Risks: <items>
- Performance Concerns: <items>

## STRATEGY

- Pattern(s): <e.g., Strangler Fig>
- Phases: <Phase 1, Phase 2, Phase 3 titles>
- Rollback Plan: <overview>

## JUSTIFICATION

- Technical alignment with current system
- Balance of risk vs benefit
- Resource/timeline fit

## IMPLEMENTATION SUMMARY

### High Level Checklist:

<bullet summary of tasks>

### Testing Strategy:

<coverage plan, tooling>

### Success Metrics:

<targets>
```

## Examples

```bash
# Plan refactor for the payments service
/plan-refactor "payments service"

# Use verbose notes (no additional flags currently supported; reserved for future)
/plan-refactor "frontend shell"
```
