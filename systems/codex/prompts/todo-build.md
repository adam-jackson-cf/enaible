# todo-build v0.1

**Purpose**

- Execute a provided plan end-to-end: implement changes, enforce the plan’s gates and tests, create a branch in an isolated git worktree, open a PR, and iterate on PR review feedback until approved with all checks passing — keeping the plan file as the single source of truth.

## Variables

- `$PLAN_PATH` ← first positional argument (required)
- `$TARGET_PATH` ← second positional (default `.`)
- `$REMOTE` ← `--remote` (default `origin`)
- `$WORKTREES` ← `--worktrees` (default `.worktrees`)
- `$BASE` ← `--base` (optional; else derive from plan metadata or default `main`)
- `$TITLE` ← `--title` (optional; default from plan title)
- `$LABELS` ← `--labels` CSV (optional; e.g., `codex-review,ready-for-qa`)

## Instructions

- Autonomous; no interactive prompts. Fail fast on INIT critical failures.
- Always use git worktrees; do not modify the primary working directory.
- Treat `$PLAN_PATH` as the single source of truth; update status, tasks, logs, gates, and test entries in that file.
- Update the plan whenever there is relevant change to comment on that reflects its requested detail.
- Commit code and plan updates together (atomic commits).
- Enforce gates/tests exactly; do not advance on failures or relax thresholds.
- Never commit secrets; if detected, halt and record locations in the plan.
- Use the resolved variables in all commands (e.g., `git worktree add -b "$BRANCH" "$WORKTREES/$TS-$SLUG" "$BASE"`).

## Workflow

- 1. INIT
- Resolve effective variables from arguments/defaults: `$PLAN_PATH`, `$TARGET_PATH`, `$REMOTE`, `$WORKTREES`, `$BASE`, `$TITLE`, `$LABELS`.
- Verify tools: `git` (worktree), `gh` (authenticated), and commands referenced by the plan’s gates/tests.
- Ensure `$PLAN_PATH` exists and the plan defines: title/objective, repository/base branch, actionable tasks, gate commands/thresholds, test commands, and completion criteria.
- Fetch `$REMOTE` and determine `$BASE`; derive branch slug from the plan’s title.

2. PREPARE

- Ensure `$WORKTREES` exists (create if missing) and is gitignored (append if missing).
- Create worktree and new branch from `$BASE`: `$WORKTREES/$TS-$SLUG`.
- If the plan tracks metadata (status/branch/timestamps), set Status=In Progress, set branch name, update timestamps.

3. EXECUTE_LOOP (per task in plan order)

- Implement the step with minimal diffs (keep function complexity ≤ 10).
- If tests are implied, add/modify tests and update the plan’s test entries.
- Stage and commit code + plan changes atomically.
- In the plan, mark the step complete and add a timestamped progress/log entry.

  GATES_LOOP (blocking)

  - Run each gate exactly as written; compare to thresholds; record pass/fail and key metrics in the plan.
  - Run the plan’s test commands; record results in the plan. All required tests must pass.
  - On failure: do not proceed; record details; apply fixes; re-run. After 3 failed attempts on the same step, set Status=Blocked and stop.

- 4. PR_OPEN
- Push branch to `$REMOTE`. Create PR with `gh`; title from plan (or `$TITLE`); apply `$LABELS`.
- Record PR URL in the plan’s progress/log.

5. REVIEW_LOOP (final quality gate)

- Start a lightweight background watcher that polls the PR for new reviews/comments and CI check updates (e.g., `gh pr view --json reviews,reviewDecision,comments,checks`). On actionable feedback or failing checks, wake the loop to apply changes.
- If changes are requested, add/modify tasks directly in the plan to capture feedback, implement changes, update tests/gates, and commit atomically.
- Repeat until APPROVED and all checks pass.
- If the plan tracks metadata, set Status=Complete and update timestamps.

6. FINALIZE

- Leave the worktree intact for verification.
- Emit a concise final summary (see Output).

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

$ARGUMENTS
