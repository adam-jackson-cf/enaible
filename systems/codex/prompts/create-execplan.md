# create-execplan v0.1

**Purpose**

- Produce a complete execution plan (ExecPlan) for `$USER_PROMPT` from supplied artifacts and targeted online research, conforming to `systems/codex/execplan.md`.

## Variables

- `$USER_PROMPT` ← first positional argument (required)
- `--artifact PATH_OR_URL` (repeatable) ← paths or URLs providing context (e.g., spec, inspect report)

## Instructions

- Read artifacts first (spec, then inspect); extract objective, constraints, stack, and file/module references.
- Incorporate global project/user rules (coding preferences, quality gates, stack conventions, security posture).
- Use online research and always call `/plan-solution` for analysis; cite official documentation.
- Answer clarifications autonomously from artifacts and rules; favor strict gates and established libraries.
- Output only the final ExecPlan (no preface), in `systems/codex/execplan.md` shape.

## Workflow

1. Collect Inputs

   - Load all `--artifact` values (local files or URLs). For URLs, summarize key facts; for files, extract salient sections (objective, constraints, tech stack, modules).

2. Analyze (online)

   - Run `/plan-solution` with web search enabled to produce approaches and a recommended solution:
     - `cdx-exec --model gpt-5-high -c 'tools.web_search=true' -c 'sandbox_workspace_write.network_access=true' "/plan-solution \"$USER_PROMPT\""`
   - Provide clarifications from artifacts and the rules digest as requested.
   - Capture the recommendation and rationale for the ExecPlan.

3. Synthesize ExecPlan

   - Convert the recommended solution into a complete plan with sections:
     - Purpose / Big Picture — user‑visible outcome and business value
     - Success Criteria / Acceptance Tests — deterministic checks (how to verify)
     - Context & Orientation — files/modules by path, APIs/events, constraints/assumptions
     - Plan of Work (Prose) — file:function edits with what/why
     - Concrete Steps (Checklist) — actionable, minimal tasks
     - Test Plan — unit/integration/perf; include “how to run” commands (local/CI)
     - Quality Gates — strict thresholds (lint, type, complexity ≤ 10, duplication ≤ 3%, tests 100% passing)
     - Risks & Mitigations — impact • likelihood with mitigation plan
     - Dependencies — upstream/downstream services, releases, approvals
     - Security / Privacy / Compliance — data touched, secrets handling, checks
     - Observability (Optional) — metrics, logs/traces, flags
     - Running Logs — Progress, Decisions, Surprises (initial stubs)
   - Ensure all required sections are present and tailored to the project stack indicated by artifacts.

4. Emit Plan

   - Output the final ExecPlan.

## Output

- Final ExecPlan in the below format:

```markdown
# ExecPlan: <Short, action‑oriented title>

- Status: Proposed
- Repo/Branch: `<owner>/<repo>` • `<branch>`
- Scope: <feature/bug/ops task> • Priority: <P0–P3>
- Start: <YYYY-MM-DD> • Last Updated: <ISO8601 UTC>
- Links: <issue/PR/runbook/design/PRD>

## Purpose / Big Picture

Explain the user‑visible outcome and business value.

## Success Criteria / Acceptance Tests

- [ ] <Deterministic check 1 (how to verify)>
- [ ] <Deterministic check 2>
- Non‑Goals: <explicitly excluded areas>

## Context & Orientation

- Code: `path/to/fileA:line`, `path/to/moduleB`
- Data/Contracts: <APIs, schemas, events>
- Constraints/Assumptions: <performance, security, platform, SLAs>

## Plan of Work (Prose)

- Edit 1: `path/to/file.ts:functionName` — <what/why>
- Edit 2: `path/to/other.py:Class.method` — <what/why>

## Concrete Steps (Checklist)

- [ ] <step 1>
- [ ] <step 2>
- [ ] <step 3>

## Progress (Running Log)

- (YYYY-MM-DDThh:mmZ) <what changed, where, evidence>
- (YYYY-MM-DDThh:mmZ) <next focus / blocker>

## Surprises & Discoveries

- Observation: <what> • Evidence: `<path/log/screenshot>`

## Decision Log

- Decision: <what>
  Rationale: <why this over alternatives>
  Date/Author: <YYYY-MM-DD • name>

## Risks & Mitigations

- Risk: <impact • likelihood> • Mitigation: <plan/owner/trigger>

## Dependencies

- Upstream/Downstream: <services, libraries, teams>
- External Events: <releases, migrations, flags, approvals>

## Security / Privacy / Compliance

- Data touched: <PII/none> • Storage/Transit: <details>
- Secrets: <none | how managed> • Threats: <summary>
- Checks: <linters/scanners/tests to run>

## Observability (Optional)

- Metrics: <names, targets>
- Logs/Traces: <keys to search, sampling>
- Feature Flags/Experiments: <keys, rollout plan, guardrails>

## Test Plan

- Unit: <scope, fast cases>
- Integration/E2E: <paths, fixtures, environments>
- Performance/Accessibility: <budgets, tools>
- How to run: `<commands>` (local/CI)

### Quality Gates

| Gate                  | Command                                            | Threshold / Expectation |
| --------------------- | -------------------------------------------------- | ----------------------- |
| Lint (Ruff/Ultracite) | `uv run ruff check .` / `bunx ultracite check src` | 0 errors                |
| Type Check            | `uv run mypy src` / `bunx tsc --noEmit`            | 0 errors                |
| Complexity            | `uv run lizard -C 10 <paths>`                      | Max CC ≤ 10             |
| Duplication           | `npx jscpd --min-tokens 50`                        | Duplication ≤ 3%        |
| Tests                 | `pytest -q` / `bun run test`                       | 100% passing            |

## Handoff & Next Steps

- Remaining work to productionize: <docs, training, tickets>
- Follow‑ups/backlog: <links or bullets>

## Outcomes & Retrospective

- Result vs Goals: <met/partially/not met> • Evidence: <links>
- What went well: <bullets>
- What to change next time: <bullets>
```

## Examples

- `/create-execplan "Add MFA to admin console" --artifact .workspace/orchestrate/2025-10-13/spec.md --artifact .workspace/orchestrate/2025-10-13/inspect.md`
