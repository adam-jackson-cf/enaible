# Purpose

Develop and compare solution approaches for a `$USER_PROMPT` using targeted context gathering, research, and structured recommendations.

## Variables

- `$USER_PROMPT` ← first positional argument or prompt input describing the technical problem.

## Instructions

- Begin by collecting detailed context based on `$USER_PROMPT`, environment constraints, and delivery preferences.
- If analyzing an existing codebase, run the architecture analyzers before crafting solutions.
- Produce exactly three solution options (Conservative, Balanced, Innovative) with consistent evaluation criteria.
- Support recommendations with research citations or code insights.
- When `--critique` is used, invoke `@agent-solution-validator` after drafting the recommendation.
- Wait for approval before appending tasks to `todos.md`.

## Workflow

1. Intake context
   - Request explicit information when missing from `$USER_PROMPT` - frame with assumptions:
     1. Defintion of problem to solve or feature to create
     2. Any technical constraints or predetermined tech stack choices
     3. Development approach preferences
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
   - Write a summary using below output format with no additional commentary.

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
