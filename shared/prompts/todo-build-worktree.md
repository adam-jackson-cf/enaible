# Purpose

Execute the structured todo implementation program that transforms todos into completed features using git worktrees, gated refinement, and subagent orchestration.

## Variables

- `TASK_FILE` ← `task.md` inside active worktree (if present).
- `CLAUDE_MD` ← project-level `Claude.md`.
- `WORKTREE_DIR` ← path under `todos/worktrees/`.
- `STATUS` ← value extracted from `task.md`.
- `$ARGUMENTS` ← raw argument string.

## Instructions

- Follow workflow phases in order: INIT → SELECT → REFINE → IMPLEMENT → COMMIT.
- Enforce every STOP confirmation; loop back for revisions when user declines.
- Keep commit messages human-centric—never reference yourself as the author.
- Track plan checkboxes meticulously, adding new ones before tackling unforeseen work.
- Always involve the user when unexpected errors occur or new scope emerges.

## Workflow

1. INIT
   - Run `git worktree help >/dev/null 2>&1`; exit immediately if git worktree support is unavailable because the workflow cannot proceed without it.
   - Run `mkdir -p todos && test -w todos`; exit immediately if the todos directory cannot be created or written because worktree data must be stored here.
   - If `task.md` exists in CWD:
     - Read `task.md` and `Claude.md`.
     - Update `**Agent PID:**` with current parent PID.
     - Resume based on `Status` (`Refining`, `InProgress`, `AwaitingCommit`, `Done`).
   - Ensure `/todos/worktrees/` is ignored in `.gitignore`.
   - If `Claude.md` missing, perform project discovery (purpose, features, tech stack, structure, commands, testing) using parallel agents and confirm via STOP before writing.
   - Detect orphaned worktrees (tasks whose agents exited); prompt to resume or ignore.
2. SELECT
   - Read `todos/todos.md`; present numbered list of todos.
   - **STOP:** “Which todo would you like to work on? (enter number)”
   - Remove selected todo and commit `Remove todo: <title>`.
   - Create worktree branch (`git worktree add -b <slug> todos/worktrees/<timestamp>-<slug>/ HEAD`).
   - Initialize `task.md` template with status `Refining` and PID.
   - Commit initialization (`[task-title]: Initialization`) and push branch.
3. REFINE
   - Research required code changes using subagents; append findings to `analysis.md`.
   - Draft description and implementation plan; confirm each via STOP prompts.
   - Update `task.md` with refined plan; set status to `InProgress`.
   - Commit (`[task-title]: Refined plan`); assign subagent to worktree; notify user.
4. IMPLEMENT
   - For each plan checkbox:
     - Execute code changes; present diff summary; **STOP** for approval.
     - Mark checkbox complete and commit with checkbox text.
   - On failures (tests/lint/build), add new checkboxes after user confirmation and repeat.
   - Present user test steps; **STOP:** “Do all user tests pass? (y/n)”
   - If project description needs updates, propose changes to `Claude.md` and request approval.
   - Set status to `AwaitingCommit`; commit `Complete implementation`.
5. COMMIT
   - Summarize completed work; **STOP:** “Ready to create PR? (y/n)”
   - Set status `Done` in `task.md`.
   - Move `task.md` and `analysis.md` to `todos/done/` with timestamped names.
   - Commit `Complete` and push branch.
   - Create PR via GitHub CLI.
   - **STOP:** “PR created. Delete the worktree? (y/n)” Remove worktree if confirmed.

## Output

```md
# RESULT

- Summary: Todo "<title>" processed through <final phase>.

## STATUS

- Current Phase: <INIT|SELECT|REFINE|IMPLEMENT|COMMIT>
- Worktree: <path or none>
- Branch: <name>

## ARTIFACTS

- task.md: <status>
- analysis.md: <status>
- Commits: <list with hashes>

## NEXT STEPS

1. <Action item (e.g., review PR)>
2. <Action item>
```

## Examples

```bash
# Start the todo implementation workflow
/todo-build-worktree
```
