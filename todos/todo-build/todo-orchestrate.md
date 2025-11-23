# todo-orchestrate v0.2

**Purpose**

- Orchestrate a four-stage autonomous workflow to deliver on @TASK_INPUT by inspecting the codebase (if applicable), performing plan research with online search, creating a concrete execution plan, and building the change — passing all artifacts forward and answering any sub‑prompt interactions on the user’s behalf.

## Variables

### Required

- @TASK_INPUT = $1 — task spec (free text, file path, or Linear issue ID like ABC-123)

### Optional (derived from $ARGUMENTS)

- @EXCLUDE_GLOBS = --exclude [repeatable] — CSV globs to ignore (e.g., node_modules,dist)
- @DAYS = --days — history window for inspect (default 20)
- @REMOTE = --remote — remote name (default origin)
- @BASE = --base — base branch (optional; default main)
- @WORKTREES = --worktrees — worktrees directory (default .worktrees)

### Derived (internal)

- @SLUG = <derived>
- @TS = <derived>
- @BRANCH = <derived>
- @WORKTREE_PATH = <derived>
- @WSDIR = <derived>
- @SLUG_TS = <derived>

## Instructions

- Maintain full autonomy: whenever a sub‑prompt requests input (clarifications, continue/approve), synthesize answers from `SPEC_PATH` and accumulated artifacts, then proceed.
- Pass artifacts strictly between stages: each stage receives all prior artifacts (paths and, when asked, distilled summaries).
- Use Codex subprocess tasks (`codex exec`) for each phase; models and options are specified in the commands shown.
- Enable online search during PLAN by setting `-c tools.web_search=true` and `-c sandbox_workspace_write.network_access=true`.
- Persist all outputs under @WSDIR inside the worktree and reuse downstream. Redact secrets where necessary.
- Auto‑initialize brand‑new repositories in INIT (git init + initial commit on @BASE) before creating the worktree.

## Workflow

1. **INIT**

   - Derive identifiers from @TASK_INPUT:
     - @SLUG = kebab-case of the input (or source title for files/Linear issues)
     - @TS = timestamp YYYYmmddHHMM
     - @BRANCH = feature/@SLUG-@TS
     - @WORKTREE_PATH = @WORKTREES/@SLUG-@TS
     - @WSDIR = @WORKTREE_PATH/.enaible/orchestrate/@SLUG-@TS
     - If the repository already has commits:
       - BASE=${BASE:-$(git symbolic-ref -q --short HEAD || echo main)}
       - REMOTE=${REMOTE:-$(git remote 2>/dev/null | head -n1 || echo origin)}
     - Otherwise default to `REMOTE=origin` and `BASE=main`.
   - Ensure a git repository is available:
     - If `.git` missing or no commits: run `git init && git checkout -b ${BASE:-main}`, add a minimal tracked file, and commit (`chore: init repo`).
     - When `REMOTE` exists, fetch the base branch: `git fetch REMOTE ${BASE:-main}`.
   - Create worktree and workspace, then run all phases inside it:

     ```bash
     git worktree add -b "@BRANCH" "@WORKTREE_PATH" "${BASE:-main}"
     mkdir -p "@WSDIR"/spec "@WSDIR"/inspect "@WSDIR"/plan
     ```

   - Classify @TASK_INPUT and persist the spec at SPEC_PATH within @WSDIR:
     - Linear ID (`[A-Z]+-[0-9]+`) → fetch via Linear MCP, normalize to spec.
     - Readable file → copy/normalize into spec.
     - Otherwise → write free-text spec with a minimal header.
   - Detect new repositories: if `WORKTREE_PATH` lacks meaningful code/manifests, set `NEW_REPO=true`; otherwise `NEW_REPO=false`.

2. **INSPECT (skip when `NEW_REPO=true`)**

   - Run the inspection phase inside the worktree with sandbox writes enabled:

     ```bash
     codex exec --sandbox workspace-write -C "@WORKTREE_PATH" --model gpt-5-codex-medium \
       "/todo-inspect-codebase @TASK_INPUT . --days @DAYS${EXCLUDE_GLOBS:+ --exclude @EXCLUDE_GLOBS} --out .enaible/@SLUG_TS/inspect/report.md"
     ```

   - Pass only the full inspection report to downstream phases. If `NEW_REPO=true`, record a blocked note referencing missing code and stop.

3. **PLAN**

   - Generate the ExecPlan with online search enabled and previous artifacts attached:

     ```bash
     codex exec --sandbox workspace-write -C "@WORKTREE_PATH" --model gpt-5-high \
       -c 'tools.web_search=true' \
       -c 'sandbox_workspace_write.network_access=true' \
       "/create-execplan @TASK_INPUT --artifact .enaible/@SLUG_TS/spec/spec.md --artifact .enaible/@SLUG_TS/inspect/report.md --out .enaible/@SLUG_TS/plan/execplan.md"
     ```

   - When sub-prompts request clarification, respond using `spec/spec.md`, the inspection report, and project/user AGENTS.md rules.

4. **BUILD**

   - Execute the build phase inside the worktree and propagate updates through the ExecPlan:

     ```bash
     codex exec --sandbox workspace-write -C "@WORKTREE_PATH" --model gpt-5-codex-medium \
       "/todo-build .enaible/@SLUG_TS/plan/execplan.md @WORKTREE_PATH --remote @REMOTE${BASE:+ --base @BASE} --worktrees @WORKTREES"
     ```

   - The build process updates the ExecPlan (Progress, PR & Review, Results). No extra PR or summary files are generated.

## Output

- Final orchestration summary:
  - Task: @TASK_INPUT (type: Linear/file/text)
  - Artifacts:
    - Spec: .enaible/@SLUG_TS/spec/spec.md
    - Inspect: .enaible/@SLUG_TS/inspect/report.md
    - ExecPlan (single source of truth): .enaible/@SLUG_TS/plan/execplan.md
  - PR: captured in ExecPlan (PR & Review section) or blocker + reason
  - Timing: start/end, per‑phase durations

## Examples

- `/todo-orchestrate "Add MFA to admin console"`
- `/todo-orchestrate ./docs/prd/auth-mfa.md`
- `/todo-orchestrate SEC-1234 --exclude node_modules,dist`
