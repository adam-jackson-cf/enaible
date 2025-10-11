---
description: "Todo orchestration with automated multi-agent coordination from implementation plan to delivery"
argument-hint: <implementation-plan-path> [--prototype]
allowed-tools:
  ["Task", "Read", "Write", "Edit", "TodoWrite", "Bash", "Grep", "Glob", "LS"]
---

# Todo Build — Follow Implementation Plan

Execute a clean, phase‑driven build using sub‑agent orchestration that follows a provided implementation plan exactly.

## Usage

```bash
/todo-build <IMPLEMENTATION_PLAN_PATH> [--prototype] [--parallel]
```

## Arguments

- `IMPLEMENTATION_PLAN_PATH`: Path to the implementation plan file

## Optional Flags

- `--prototype`: Skip tests and relax gates (faster iteration)

## CRITICAL

- Follow phases in order: INIT → EXECUTE → COMMIT
- Invoke subagents sequentially, never in parallel
- Get user confirmation at each STOP checkpoint
- Do not modify the plan beyond task state updates unless explicitly instructed
- Do not mention yourself in commit messages

## Sub‑Agent Roles

- `@agent-plan-manager`: Parse plan, track task states, dependency ordering
- `@agent-solution-validator`: Validate approach against the plan (no extra context gathering)
- `@agent-senior-developer`/domain experts: Implement tasks
- `@agent-quality-monitor`: Run quality gates; respects `--prototype`
- `@agent-git-manager`: Stage and commit changes
- `@agent-problem-escalation`: Triage after repeated failures

## Phases

### INIT

1. Verify `IMPLEMENTATION_PLAN_PATH` exists and is readable.
2. Read the plan in full; hand to `@agent-plan-manager` to build a task registry:
   - Phases, tasks, dependencies
   - Each task has a clear deliverable and success criteria
3. Present a numbered summary of phases and tasks.
4. STOP → "Proceed with this plan? (y/n)"

### EXECUTE

Process tasks in phase order, honoring dependencies.

For each task:

1. Assignment → `@agent-plan-manager` marks state: pending → assigned
2. Validation → `@agent-solution-validator` checks that the proposed approach conforms to the plan scope only.
   - On reject: retry up to 2 times, then escalate to `@agent-problem-escalation`
   - On approve: state → validated
3. Implementation → use `@agent-senior-developer`:
   - Produce minimal, reviewable diffs; summarize changes
   - STOP → "Approve implementation before quality gates? (y/n)"
4. Quality → `@agent-quality-monitor` runs gates
   - Prototype: skip tests; still lint/build if available
   - Production: run lint, tests, and build where applicable
   - On pass: state → approved
   - On fail: state → in_progress; fix with `@agent-fullstack-developer`; up to 3 attempts, else escalate
5. Commit → `@agent-git-manager`
   - Use descriptive message from the task title; include file paths changed
   - On pre‑commit failure: fix and retry (max 3), else escalate
6. Completion → state → completed

Loop until all tasks in all phases are completed.

### COMMIT

1. Generate a completion summary via `@agent-plan-manager`:
   - Tasks completed vs planned; any leftovers
   - Gate results and notable fixes
   - Commit hashes and file lists
2. Produce a short user validation checklist derived from the plan’s success criteria.
3. STOP → "Create a follow‑up todo for deferred items? (y/n)"

## Output Format

- Phase summaries with task state transitions
- Per‑task: validation result, implementation summary, gate results, commit reference
- Final completion summary and optional follow‑up todos

---

Begin by reading the implementation plan at `$ARGUMENTS`, summarizing phases and tasks, and waiting at the INIT STOP.
