# todo-build v0.2

## Purpose

Execute a provided plan end-to-end: implement changes, enforce the plan’s gates and tests, create a branch in an isolated git worktree, open a PR, and iterate on PR review feedback until approved with all checks passing — keeping the plan file as the single source of truth.

## Variables

### Required

- @PLAN_PATH = $1 — path to implementation plan

### Optional (derived from $ARGUMENTS)

- @REMOTE = --remote — remote name (default origin)
- @WORKTREES = --worktrees — worktrees directory (default .worktrees)
- @BASE = --base — base branch (optional; else derive from plan metadata or default main)
- @TITLE = --title — PR title override (optional)
- @LABELS = --labels — CSV labels (optional; e.g., codex-review,ready-for-qa)

### Derived (internal)

- @SLUG = <derived>
- @TS = <derived>
- @BRANCH = <derived>

## Instructions

- Autonomous; no interactive prompts. Fail fast on INIT critical failures.
- Always use git worktrees; do not modify the primary working directory. If CWD is already a git worktree, reuse it and skip creating a new one.
- Treat @PLAN_PATH as the single source of truth; update status, tasks, logs, gates, and test entries in that file.
- Commit code and plan updates together (atomic commits).
- Enforce gates/tests exactly; do not advance on failures or relax thresholds.
- Never commit secrets; if detected, halt and record locations in the plan.

## Workflow

1. **INIT**

   - Resolve core variables (@PLAN_PATH, @REMOTE, @WORKTREES, @BASE, @TITLE, @LABELS).
   - Verify required tooling (`git` for worktrees, authenticated `gh`, and every gate/test command referenced in the plan).
   - Validate the plan: title/objective, repository/base branch, actionable tasks, gate thresholds, test commands, completion criteria.
   - Derive working identifiers from the plan title (@SLUG, @TS, @BRANCH).

2. **PREPARE**

   - Ensure @WORKTREES exists (create and gitignore if needed).
   - Reuse the current worktree when possible; otherwise attach or create the branch/worktree:
     - If @BRANCH exists, attach a worktree or reuse the existing path.
     - Otherwise run `git worktree add -b "@BRANCH" "@WORKTREES/@TS-@SLUG" "${BASE:-main}"`.
   - Update plan metadata (Status=In Progress, branch name, timestamps) when applicable.

3. **EXECUTE_LOOP (per task order)**

   - Implement minimal diffs (keep function complexity ≤ 10) and update or create tests as implied by each task.
   - Stage and commit code plus plan updates atomically; rerun pre-commit hooks and restage if they modify files.
   - Mark plan steps complete with timestamped log entries.
   - **GATES_LOOP (blocking):**
     - Run each gate command exactly as specified, capture metrics, and record pass/fail.
     - Execute required tests, logging outcomes in the plan; all must pass before proceeding.
     - After three failed attempts on the same step, set Status=Blocked and stop.

4. **PR_OPEN**

   - Push the branch to `REMOTE`, create the PR with `gh` (title from plan or `TITLE`, apply `LABELS`), and log the PR URL in the plan.

5. **REVIEW_LOOP (final quality gate)**

   - Poll PR reviews, comments, and checks (`gh pr view --json reviews,reviewDecision,comments,checks`).
   - Apply requested changes by updating plan tasks, implementing code adjustments, rerunning gates/tests, and committing atomically.
   - Repeat until the PR is approved and all checks pass; then mark the plan Status=Complete with timestamps.

6. **FINALIZE**
   - Leave the worktree intact for verification and refrain from generating additional summary files—the ExecPlan remains the single source of truth (Progress, PR & Review, Results).

## Output

- Final summary to the user:
  - Title, Branch, Worktree path, PR URL
  - Gates Summary: each gate command with pass/fail and key metric vs threshold
  - Tests Summary: commands executed and status
  - Completed task count vs total and last commit hash
  - If stopped: Status=Blocked with failing command and where to see details in the plan

## Examples

- `/todo-build ./plans/feature-x-plan.md`
- `/todo-build ./plans/feature-x-plan.md --remote origin --labels codex-review,ready-for-qa`
- `/todo-build ./plans/feature-x-plan.md --base develop --worktrees .worktrees`
