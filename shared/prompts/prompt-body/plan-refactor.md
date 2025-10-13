# Purpose

Design a staged refactoring plan that reduces technical debt, mitigates risk, and delivers measurable quality improvements.

## Variables

- `REFACTOR_SCOPE` ← first positional argument; defines area or component.
- `SCRIPT_PATH` ← resolved analyzer root (quality, architecture, performance).
- `VERBOSE_FLAGS` ← flags passed through `$ARGUMENTS` (none currently defined).

## Instructions

- Execute the workflow phases in order and honor each STOP confirmation.
- Run registry-driven analyzers only; capture outputs for quality documentation.
- Anchor migration strategies in proven patterns (Strangler Fig, Module Federation, blue-green, etc.).
- Define rollback steps and monitoring at every migration phase.
- Translate the final plan into actionable todos when approved.

## Workflow

1. Resolve analyzer scripts
   - Run `ls .claude/scripts/analyzers/quality/complexity_lizard.py || ls "$HOME/.claude/scripts/analyzers/quality/complexity_lizard.py"`; if both fail, prompt for a directory containing `quality/complexity_lizard.py`, `architecture/coupling_analysis.py`, and `performance/performance_baseline.py`, then exit if none is provided. Set `SCRIPT_PATH` to the resolved script path.
   - Once resolved, compute `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
2. Phase 1 — Technical Debt Assessment
   - Execute analyzers:
     - `quality:lizard`
     - `architecture:coupling`
     - `performance:baseline`
   - Identify hotspots, architectural debt, security overlaps.
   - Generate technical debt summary.
   - **STOP:** “Technical debt analysis complete. Proceed with strategy development? (y/n)”
3. Phase 2 — Migration Strategy
   - Research industry patterns tailored to `REFACTOR_SCOPE`.
   - Outline phased migration (feature flags, decomposition, deployment strategy).
   - Define rollback procedures and monitoring hooks.
   - **STOP:** “Migration strategy defined. Ready to create implementation plan? (y/n)”
4. Phase 3 — Implementation Planning
   - Break work into phases with timelines and checkpoints.
   - Run `quality:coverage` analyzer to inform testing strategy.
   - Establish success metrics (complexity targets, performance budgets, velocity impact).
5. Phase 4 — Quality Validation & Task Transfer
   - Confirm quality gates:
     - Hotspots prioritized.
     - Strategy aligns with proven patterns.
     - Rollback and monitoring defined.
     - Testing strategy in place.
     - Success metrics measurable.
   - **STOP:** “Implementation plan complete and validated. Transfer to todos.md? (y/n)”
   - On approval, append structured tasks (Phase headers with checkboxes) to `todos.md`.

## Output

```md
# RESULT

- Summary: Refactoring plan created for <REFACTOR_SCOPE>.

## ASSESSMENT

- Hotspots: <key findings>
- Architecture Risks: <items>
- Performance Concerns: <items>

## STRATEGY

- Pattern(s): <e.g., Strangler Fig>
- Phases: <Phase 1, Phase 2, Phase 3 titles>
- Rollback Plan: <overview>

## IMPLEMENTATION PLAN

- Checklist: <bullet summary of tasks>
- Testing Strategy: <coverage plan, tooling>
- Success Metrics: <targets>

## TODOS TRANSFERRED

- <yes/no> (if yes, list added sections)
```

## Examples

```bash
# Plan refactor for the payments service
/plan-refactor "payments service"

# Use verbose notes (no additional flags currently supported; reserved for future)
/plan-refactor "frontend shell"
```
