# Purpose

Execute an implementation plan using orchestrated subagents while enforcing sequential phases, quality gates, and explicit user approvals.

## Variables

- `PLAN_PATH` ← first positional argument; required path to implementation plan.
- `PROTOTYPE_MODE` ← boolean when `--prototype` flag present.
- `PARALLEL_MODE` ← boolean when `--parallel` flag present (default sequential; document if unsupported).
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Honor the phase order: INIT → EXECUTE → COMMIT.
- Invoke subagents sequentially; never run them in parallel unless the plan explicitly authorizes parallelism.
- Obtain user approval at every STOP checkpoint and before modifying the implementation plan.
- Avoid altering plan scope except for task state updates or user-authorized additions.
- Keep commit messages descriptive and free of self-reference.

## Workflow

1. INIT
   - Run `test -r "$PLAN_PATH"`; exit immediately if the implementation plan is missing or unreadable.
   - Read plan contents fully; hand to `@agent-plan-manager` to build task registry (phases, dependencies, success criteria).
   - Present numbered summary of phases and tasks.
   - **STOP:** “Proceed with this plan? (y/n)”
2. EXECUTE (for each phase, tasks in dependency order)
   - Assignment: `@agent-plan-manager` marks task pending → assigned.
   - Validation: `@agent-solution-validator` ensures approach aligns with plan scope; retry up to 2 times, else escalate to `@agent-problem-escalation`.
   - Implementation: `@agent-senior-developer` (or domain specialists) deliver minimal diffs; summarize results.
     - **STOP:** “Approve implementation before quality gates? (y/n)”
   - Quality: `@agent-quality-monitor` runs gates.
     - Prototype mode: skip tests but still run lint/build; record skipped gates.
     - Production mode: run lint, tests, build; on failure, use `@agent-fullstack-developer` to remediate (max 3 attempts).
   - Commit: `@agent-git-manager` stages and commits with task-derived message; retry on hook failures (max 3) before escalation.
   - Completion: mark task completed in registry; proceed to next task.
3. COMMIT
   - `@agent-plan-manager` compiles completion summary (tasks done vs planned, gate outcomes, issues encountered).
   - Generate user validation checklist derived from success criteria.
   - **STOP:** “Create a follow-up todo for deferred items? (y/n)” Append to `todos/todos.md` if approved.
   - Provide final report with commits, file paths, and validation status.

## Output

```md
# RESULT

- Summary: Implementation plan executed from "<PLAN_PATH>".

## PHASE STATUS

- INIT: <complete timestamp>
- EXECUTE: <tasks completed>/<total>
- COMMIT: <complete timestamp>

## TASKS

| Phase | Task | State | Commit |
| ----- | ---- | ----- | ------ |
| ...   | ...  | ...   | ...    |

## QUALITY GATES

- Lint: <pass|fail|skipped>
- Tests: <pass|fail|skipped>
- Build: <pass|fail|skipped>

## FOLLOW-UP

- Deferred Items: <list or none>
- Checklist for User Validation: <bullets>
```

## Examples

```bash
# Execute plan in production mode
/todo-build ./plans/feature-123.md

# Execute plan in prototype mode (relaxed gates)
/todo-build ./plans/rapid-prototype.md --prototype
```
