# Purpose

Develop and compare solution approaches for a technical challenge using targeted context gathering, research, and structured recommendations.

## Variables

- `CHALLENGE` ← first positional argument or prompt input describing the technical problem.
- `CRITIQUE_MODE` ← boolean flag when `--critique` present.
- `SCRIPT_PATH` ← resolved architecture analyzer directory (conditional when analyzing code).
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Begin by collecting detailed context—technical challenge, environment constraints, and delivery preferences.
- If analyzing an existing codebase, run the architecture analyzers before crafting solutions.
- Produce exactly three solution options (Conservative, Balanced, Innovative) with consistent evaluation criteria.
- Support recommendations with research citations or code insights.
- When `--critique` is used, invoke `@agent-solution-validator` after drafting the recommendation.
- Wait for approval before appending tasks to `todos.md`.

## Workflow

1. Intake context
   - Request explicit information:
     1. Technical Challenge
     2. Technical Environment Constraints
     3. Development Approach Preferences
   - **STOP:** Wait until the user provides answers or grants permission to proceed with assumptions.
2. **Conditional** system analysis (only when working against an existing codebase)
   - Locate analyzer scripts: Run `ls .claude/scripts/analyzers/architecture/pattern_evaluation.py || ls "$HOME/.claude/scripts/analyzers/architecture/pattern_evaluation.py"`; if both fail, prompt for a directory containing `pattern_evaluation.py`, `scalability_check.py`, and `coupling_analysis.py`, then exit if none is provided. Set `SCRIPT_PATH` to the resolved script path.
   - Prepare environment: Compute `SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"` and run `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`; exit immediately if it fails.
   - Run:
     - `architecture:patterns`
     - `architecture:scalability`
     - `architecture:coupling`
   - Record findings: patterns, scalability constraints, integration points, technical debt.
3. Research & option development
   - Perform targeted web/documentation research as needed.
   - Draft three solution options:
     - Solution 1: Conservative / established approach.
     - Solution 2: Balanced trade-off.
     - Solution 3: Innovative / modern approach.
   - Include approach overview, stack, complexity, risk, and suitability.
4. Comparative analysis
   - Build a matrix evaluating Development Complexity, Integration Effort, Technology Risk, and Team Readiness.
5. Recommendation & roadmap
   - Select a recommended solution with justification.
   - Outline phased implementation roadmap and success criteria.
   - If `CRITIQUE_MODE`, call `@agent-solution-validator` to review reasoning and incorporate feedback.
6. Task transfer (optional)
   - **STOP:** “Ready to transfer implementation roadmap to todos.md? (y/n)”
   - On approval:
     - Ensure `./todos/todos.md` exists.
     - Append actionable tasks derived from the roadmap.
   - Confirm transfer status in final report.

## Output

```md
# RESULT

- Summary: Solution plan generated for "<CHALLENGE>."

## SOLUTION OPTIONS

### Solution 1 — Conservative

- Approach: <summary>
- Stack: <technologies>
- Complexity: <low/medium/high>
- Risk: <assessment>

### Solution 2 — Balanced

...

### Solution 3 — Innovative

...

## COMPARATIVE ANALYSIS

| Aspect                 | Solution 1 | Solution 2 | Solution 3 |
| ---------------------- | ---------- | ---------- | ---------- |
| Development Complexity | <value>    | <value>    | <value>    |
| Integration Effort     | <value>    | <value>    | <value>    |
| Technology Risk        | <value>    | <value>    | <value>    |
| Team Readiness         | <value>    | <value>    | <value>    |

## RECOMMENDATION

- Preferred Solution: <name>
- Justification: <bullets>

## IMPLEMENTATION ROADMAP

- Phase 1: <milestones, timeline>
- Phase 2: <milestones>
- Phase 3: <milestones>
- Success Criteria: <metrics/tests>

## TODOS TRANSFERRED

- <yes/no> (list added items if applicable)
```

## Examples

```bash
# Explore solutions to a scalability challenge
/plan-solution "Scale real-time collaboration engine"

# Generate plan and trigger validator critique
/plan-solution "Modernize authentication architecture" --critique
```
