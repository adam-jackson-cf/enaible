# todo-orchestrate v0.1

**Purpose**

- Orchestrate a four-stage autonomous workflow to deliver on `$TASK_INPUT` by inspecting the codebase (if applicable), performing plan research with online search, creating a concrete execution plan, and building the change — passing all artifacts forward and answering any sub‑prompt interactions on the user’s behalf.

## Variables

- `$TASK_INPUT` ← task spec (free text, file path, or Linear issue ID like `ABC-123`)
- `$TARGET_PATH` ← project root (default `.`)
- `$REMOTE` ← git remote (default `origin`)
- `$WORKTREES` ← worktree root (default `.worktrees`)
- `$BASE` ← base branch for build (optional; else read from plan)
- `$DAYS` ← investigation window (default `20`)
- `$EXCLUDE_GLOBS` ← CSV globs to ignore (optional; e.g., `node_modules,dist`)
- `$SLUG` ← derived from `$TASK_INPUT` (kebab-case)
- `$TS` ← timestamp `YYYYmmddHHMM`
- `$BRANCH` ← feature branch (e.g., `feature/$SLUG-$TS`)
- `$WORKTREE_PATH` ← `$WORKTREES/$SLUG-$TS`
- `$WSDIR` ← `$WORKTREE_PATH/.workspace/orchestrate/$SLUG-$TS`
- `$SPEC_PATH` ← `$WSDIR/spec.md`
- `$INSPECT_REPORT` ← `$WSDIR/inspect.md`
- `$PLAN_PATH` ← `$WSDIR/execplan.md`
- `$BUILD_SUMMARY` ← `$WSDIR/build.md`
- `$PR_URL` ← populated during BUILD

## Instructions

- Maintain full autonomy: whenever a sub‑prompt requests input (clarifications, continue/approve), synthesize answers from `$SPEC_PATH` and accumulated artifacts, then proceed.
- Pass artifacts strictly between stages: each stage receives all prior artifacts (paths and, when asked, distilled summaries).
- Use Codex subprocess tasks (`cdx-exec`) for each phase; models and options are specified in the commands shown.
- Enable online search during PLAN by setting `-c tools.web_search=true` and `-c sandbox_workspace_write.network_access=true` in `cdx-exec`.
- Persist all outputs under `$WSDIR` inside the worktree and reuse downstream. Redact secrets where necessary.
- Auto‑initialize brand‑new repositories in INIT (git init + initial commit on `$BASE`) before creating the worktree.

## Workflow

- INIT

  - Derive identifiers:
    - `$SLUG` = kebab‑case of `$TASK_INPUT` (or source title when from file/Linear)
    - `$TS` = current timestamp `YYYYmmddHHMM`
    - `$BRANCH` = `feature/$SLUG-$TS`
    - `$WORKTREE_PATH` = `$WORKTREES/$SLUG-$TS`
    - `$WSDIR` = `$WORKTREE_PATH/.workspace/orchestrate/$SLUG-$TS`
  - Ensure git repository:
    - If `.git` missing or no commits: `git init && git checkout -b ${BASE:-main}`; create a minimal tracked file (e.g., `README.md` or `.gitkeep`) and commit (`chore: init repo`).
    - If `$REMOTE` is configured, run `git fetch $REMOTE ${BASE:-main}`.
  - Create worktree and workspace:
    - `git worktree add -b "$BRANCH" "$WORKTREE_PATH" "${BASE:-main}"`
    - `mkdir -p "$WSDIR"`
  - Classify `$TASK_INPUT` and write `$SPEC_PATH` inside `$WSDIR`:
    - Linear ID `[A-Z]+-[0-9]+` → fetch via Linear MCP; normalize to `$SPEC_PATH` (title/description/acceptance).
    - Readable file → copy/normalize to `$SPEC_PATH`.
    - Otherwise → write free‑text spec to `$SPEC_PATH` with minimal header.
  - Detect new repository: if negligible code/manifests in `$WORKTREE_PATH`, set `NEW_REPO=true`; otherwise `NEW_REPO=false`.

- INSPECT (skip when `NEW_REPO=true`)

  - Run (in worktree):
    - `cdx-exec -C "$WORKTREE_PATH" --model gpt-5-codex-medium "/todo-inspect-codebase \"$TASK_INPUT\" $WORKTREE_PATH --days $DAYS${EXCLUDE_GLOBS:+ --exclude $EXCLUDE_GLOBS}"`
  - Save full output to `$INSPECT_REPORT` and append a 10–15 line digest (tech stack, key modules, notable risks).
  - If `NEW_REPO=true`, write a stub `$INSPECT_REPORT` with: “Inspection skipped: new repository; no code to analyze yet.”

- PLAN

  - Run (online search enabled, in worktree):
    - `cdx-exec -C "$WORKTREE_PATH" --model gpt-5-high -c 'tools.web_search=true' -c 'sandbox_workspace_write.network_access=true' "/create-execplan \"$TASK_INPUT\" --artifact $SPEC_PATH --artifact $INSPECT_REPORT"`
  - When the sub‑task requests context/clarifications, answer using `$SPEC_PATH`, the inspection digest (or stub), and project/user AGENTS.md rules; proceed until a complete ExecPlan is produced.
  - Persist the final approved plan to `$PLAN_PATH`.

- BUILD
  - Run (in worktree):
    - `cdx-exec -C "$WORKTREE_PATH" --model gpt-5-codex-medium "/todo-build $PLAN_PATH $WORKTREE_PATH --remote $REMOTE${BASE:+ --base $BASE} --worktrees $WORKTREES"`
  - Let its quality gates and PR review loop complete; extract PR URL and status summary to `$BUILD_SUMMARY` and set `$PR_URL`.

## Output

- Final orchestration summary:
  - Task: `$TASK_INPUT` (type: Linear/file/text)
  - Artifacts:
    - Spec: `$SPEC_PATH`
    - Inspect: `$INSPECT_REPORT`
    - ExecPlan: `$PLAN_PATH`
    - Build: `$BUILD_SUMMARY`
  - PR: `$PR_URL` (or blocker + reason)
  - Timing: start/end, per‑phase durations

## Examples

- `/todo-orchestrate "Add MFA to admin console"`
- `/todo-orchestrate ./docs/prd/auth-mfa.md --worktrees .worktrees --remote origin`
- `/todo-orchestrate SEC-1234 --days 30 --exclude node_modules,dist`
