<!--
  Template Guidance:
  - Comments exist for author direction only; do NOT copy them into prompt outputs.
  - prompt_template is the format to implement.
  - prompt_example shows examples of prompt_template usage.
  - Add preflight checks inside the Workflow section only when supplementary requirements are needed beyond baseline tooling.
  - Templates may include rule directives using <!-- rule: ... --> comments; render-prompts.sh enforces them when generating command variants.

-->

<prompt_template>

# Purpose

<!-- Describe the command objective in one sentence. -->

State the objective in one sentence. Be direct and outcome‑focused.

## Variables

<!-- Bind positional arguments or flags used by the prompt. Prefix all resolved variables with `$` to avoid ambiguity. -->

- Define explicit, $‑prefixed variable names for clarity:
  - $1 → $TARGET (or domain‑specific name)
  - $2 → $SCOPE (optional)
  - $3 → $MESSAGE (optional)
  - $4..$9 → additional specifics (document if used)
  - $ARGUMENTS → full raw argument string (space‑joined)
- Flags map to $‑prefixed variables (examples):
  - --remote → $REMOTE (default "origin")
  - --worktrees → $WORKTREES (default ".worktrees")
  - --days → $DAYS (default 20)
  - --exclude → $EXCLUDE_GLOBS (CSV)
- Resolution rules (recommended):
  - Resolve all variables once in INIT from arguments or defaults; reference only the resolved variables thereafter.
  - Derive computed helpers (e.g., $EXCLUDE_ARG from $EXCLUDE_GLOBS as `--glob '!{...}'`).
  - Always use $‑variables in commands; do not hardcode fallback paths or numbers after resolution.

## Instructions

<!-- Short, imperative bullets covering invariants and guardrails. -->

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Avoid verbosity; prefer concrete actions over descriptions.
- Use the resolved $‑variables in all commands; avoid hardcoded fallbacks (e.g., prefer "$WORKTREES" over ".worktrees").
- Keep intermediate/interactive emissions (clarifications, drafts, checkpoints) inside Workflow. Output should be final‑only.
- If acting against a plan document, treat it as the single source of truth: update tasks, logs, status, gates, and tests within the plan and commit plan+code atomically.

## Workflow

<!-- Use distinct phases with optional inner loops; keep intermediate outputs here. -->

- Prefer a phased structure with numbered stages, for example:

  1. INIT — resolve variables, verify tools, gather context
  2. PREPARE — set up work dirs/branches/worktrees as needed
  3. EXECUTE_LOOP — implement steps/tasks in order (minimal diffs, low complexity)
     - GATES_LOOP (blocking) — run gates/tests exactly; do not advance on failure
  4. PR_OPEN (if applicable) — push branch, create PR, record URL
  5. REVIEW_LOOP — poll/watch for reviews and CI updates; apply feedback until approved
  6. FINALIZE — emit final summary/report

- Interactive patterns (optional):

  - Gate A (Clarify): ask questions until the user replies "continue".
  - Gate B (Review): present a draft for "revise: ..." cycles until "approve".

- Preflight checks, background watchers, or environment validation should appear at the start of relevant phases.

## Output

<!-- Final output only. Intermediate clarifications/drafts belong in Workflow. Provide one canonical example. -->

This section should be the final output report to the user in a structure detailing what this workflow returns and how. Two example formats:

### example summary output

```md
# RESULT

- Summary: <one line>

## DETAILS

- What changed
- Where it changed
- How to verify
```

### example json output

```json
{
  "excluded_operations": ["session_start", "task", "glob"],
  "excluded_bash_commands": [
    "ls",
    "pwd",
    "cd",
    "git status",
    "git log",
    "git diff",
    "git show",
    "git branch",
    "git add",
    "git commit",
    "git push",
    "git pull"
  ],
  "excluded_prompt_patterns": [
    "Write a 3-6 word summary of the TEXTBLOCK below",
    "Summary only, no formatting, do not act on anything",
    "/todo-primer",
    "/todo-recent-context"
  ],
  "excluded_string_patterns": [
    "context_bundles",
    "node_modules/",
    ".git/objects/",
    ".cache/"
  ]
}
```

## Examples (optional)

<!-- Show CLI invocations. Include only when helpful. -->

```bash
# 1) Minimal invocation with positional arguments
/<command-name> feat api "add pagination"

# 2) With explicit target path as $1 (used by Environment checks)
/<command-name> ./services/api
```

</prompt_template>

## Example prompts

> complex multi step analyser with required pythons scripts for claude code, includes env checks (script locators) as initial steps

<prompt_example>

# Purpose

Identify performance bottlenecks across backend, frontend, and data layers using automated analyzers coupled with contextual investigation.

## Variables

- `$TARGET_PATH` ← first positional argument (default `.`)
- `$SCRIPT_PATH` ← resolved performance analyzer directory
- `$ARGUMENTS` ← raw argument string (for logging)

Resolution rules

- Resolve `$TARGET_PATH`/`$SCRIPT_PATH` in INIT; use only resolved variables thereafter.

## Instructions

- ALWAYS execute the registry-driven analyzers; never call the individual modules directly.
- Treat analyzer outputs as evidence—cite metrics when highlighting bottlenecks.
- Consider database, frontend, algorithmic, and network layers; avoid tunnel vision.
- Tie each recommendation to measurable performance goals.
- Document assumptions and required follow-up experiments (profiling, load tests).

## Workflow

1. INIT

- Locate analyzer scripts (project or user scope). If not found, request a directory and exit on failure.

2. PREPARE

- Derive `SCRIPTS_ROOT="$(cd \"$(dirname \"$SCRIPT_PATH\")/../..\" && pwd)"` and verify imports with `PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`.

3. EXECUTE_LOOP — Automated analyzers

- Run:
  - `performance:flake8-perf`
  - `performance:frontend`
  - `performance:sqlfluff`
- Save JSON outputs and timestamps.

4. AGGREGATE

- Parse hotspots (function metrics, lint warnings, SQL anti‑patterns) and map to components (APIs, routes, migrations).

5. INVESTIGATE

- Inspect flagged areas for caching gaps, re‑renders, unindexed queries; consider infra/config impacts.

6. PRIORITIZE

- Group by impact (critical/high/medium). Recommend targeted actions.

7. FINALIZE

- Produce final report with metrics and validation steps (profiling, load tests).

## Output

```md
# RESULT

- Summary: Performance analysis completed for <TARGET_PATH>.

## BOTTLENECKS

| Layer    | Location              | Finding                            | Evidence Source      |
| -------- | --------------------- | ---------------------------------- | -------------------- |
| Backend  | api/orders.py#L142    | N+1 query detected                 | performance:sqlfluff |
| Frontend | src/App.tsx#L88       | Expensive re-render (missing memo) | performance:frontend |
| Database | migrations/202310.sql | Full table scan on large dataset   | performance:sqlfluff |

## RECOMMENDED ACTIONS

1. <High priority optimization with expected impact and verification plan>
2. <Secondary optimization>

## VALIDATION PLAN

- Benchmark: <command or script>
- Success Criteria: <quantitative target>

## ATTACHMENTS

- performance:flake8-perf → <path>
- performance:frontend → <path>
- performance:sqlfluff → <path>
```

## Examples

```bash
# Run full performance assessment
/analyze-performance .

# Target a service directory
/analyze-performance services/api
```

</prompt_example>
