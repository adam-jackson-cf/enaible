# todo-orchestrate v0.2

**Purpose**

- Orchestrate a four-stage autonomous workflow to deliver on `$TASK_INPUT` by inspecting the codebase (if applicable), performing plan research with online search, creating a concrete execution plan, and building the change — passing all artifacts forward and answering any sub‑prompt interactions on the user’s behalf.

## Variables

- `$TASK_INPUT` ← task spec (free text, file path, or Linear issue ID like `ABC-123`)
- `$EXCLUDE_GLOBS` ← CSV globs to ignore (optional; e.g., `node_modules,dist`)

## Instructions

- Maintain full autonomy: whenever a sub‑prompt requests input (clarifications, continue/approve), synthesize answers from `$SPEC_PATH` and accumulated artifacts, then proceed.
- Pass artifacts strictly between stages: each stage receives all prior artifacts (paths and, when asked, distilled summaries).
- Use Codex subprocess tasks (`codex exec`) for each phase; models and options are specified in the commands shown.
- Enable online search during PLAN by setting `-c tools.web_search=true` and `-c sandbox_workspace_write.network_access=true`.
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
    - If repository is initialized (has commits):
      - `BASE=${BASE:-$(git symbolic-ref -q --short HEAD || echo main)}`
      - `REMOTE=${REMOTE:-$(git remote 2>/dev/null | head -n1 || echo origin)}`
    - If not initialized yet: default to `REMOTE=origin` and `BASE=main`.
  - Ensure git repository:
    - If `.git` missing or no commits: `git init && git checkout -b ${BASE:-main}`; create a minimal tracked file (e.g., `README.md` or `.gitkeep`) and commit (`chore: init repo`).
    - If `$REMOTE` is configured, run `git fetch $REMOTE ${BASE:-main}`.
  - Create worktree and workspace (then run all phases inside it):
    - `git worktree add -b "$BRANCH" "$WORKTREE_PATH" "${BASE:-main}"`
    - `mkdir -p "$WSDIR/spec" "$WSDIR/inspect" "$WSDIR/plan"`
  - Classify `$TASK_INPUT` and write `$SPEC_PATH` inside `$WSDIR`:
    - Linear ID `[A-Z]+-[0-9]+` → fetch via Linear MCP; normalize to `$SPEC_PATH` (title/description/acceptance).
    - Readable file → copy/normalize to `$SPEC_PATH`.
    - Otherwise → write free‑text spec to `$SPEC_PATH` with minimal header.
  - Detect new repository: if negligible code/manifests in `$WORKTREE_PATH`, set `NEW_REPO=true`; otherwise `NEW_REPO=false`.

- INSPECT (skip when `NEW_REPO=true`)

  - Run (in worktree, with write sandbox):
    - `codex exec --sandbox workspace-write -C "$WORKTREE_PATH" --model gpt-5-codex-medium "/todo-inspect-codebase \"$TASK_INPUT\" . --days $DAYS${EXCLUDE_GLOBS:+ --exclude $EXCLUDE_GLOBS} --out .workspace/$SLUG_TS/inspect/report.md"`
  - Pass only the full report downstream (no digest).
  - If `NEW_REPO=true`, write a short blocked note and stop.

- PLAN

  - Run (online search enabled, in worktree with write sandbox):
    - `codex exec --sandbox workspace-write -C "$WORKTREE_PATH" --model gpt-5-high -c 'tools.web_search=true' -c 'sandbox_workspace_write.network_access=true' "/create-execplan \"$TASK_INPUT\" --artifact .workspace/$SLUG_TS/spec/spec.md --artifact .workspace/$SLUG_TS/inspect/report.md --out .workspace/$SLUG_TS/plan/execplan.md"`
  - When the sub‑task requests context/clarifications, answer using `spec/spec.md`, the full inspect report, and project/user AGENTS.md rules.

- BUILD
  - Run (in worktree with write sandbox):
    - `codex exec --sandbox workspace-write -C "$WORKTREE_PATH" --model gpt-5-codex-medium "/todo-build .workspace/$SLUG_TS/plan/execplan.md $WORKTREE_PATH --remote $REMOTE${BASE:+ --base $BASE} --worktrees $WORKTREES"`
  - Build updates the ExecPlan in place (Progress, PR & Review, Results). No separate PR/summary files.

## Output

- Final orchestration summary:
  - Task: `$TASK_INPUT` (type: Linear/file/text)
  - Artifacts:
    - Spec: `.workspace/$SLUG_TS/spec/spec.md`
    - Inspect: `.workspace/$SLUG_TS/inspect/report.md`
    - ExecPlan (single source of truth): `.workspace/$SLUG_TS/plan/execplan.md`
  - PR: captured in ExecPlan (PR & Review section) or blocker + reason
  - Timing: start/end, per‑phase durations

## Examples

- `/todo-orchestrate "Add MFA to admin console"`
- `/todo-orchestrate ./docs/prd/auth-mfa.md`
- `/todo-orchestrate SEC-1234 --exclude node_modules,dist`
