# ExecPlan: <Short, action‑oriented title>

- Status: <Proposed | In Progress | Blocked | Complete>
- Repo/Branch: `<owner>/<repo>` • `<branch>`
- Scope: <feature/bug/ops task> • Priority: <P0–P3>
- Start: <YYYY-MM-DD> • Last Updated: <ISO8601 UTC>
- Links: <issue/PR/runbook/design/PRD>

## Purpose / Big Picture

Explain in a few sentences what someone gains after this change and how they can see it working. State the user‑visible behavior and business outcome you will enable.

## Success Criteria / Acceptance Tests

- [ ] <Deterministic check 1 (how to verify)>
- [ ] <Deterministic check 2>
- Non‑Goals: <explicitly excluded areas>

## Context & Orientation

Describe the current state as if the reader knows nothing. Name key files and modules by full path, and define any non‑obvious terms.

- Code: `path/to/fileA:line`, `path/to/moduleB`
- Data/Contracts: <APIs, schemas, events>
- Constraints/Assumptions: <performance, security, platform, SLAs>

## Plan of Work (Prose)

Describe the sequence of edits/additions. For each edit, name the file and location (function/module) and what to insert/change with line number and offset; keep it concrete and minimal.

- Edit 1: `path/to/file.ts:functionName` — <what/why>
- Edit 2: `path/to/other.py:Class.method` — <what/why>

## Concrete Steps (Checklist)

Track granular steps; split partial work into “done vs remaining.” Timestamp entries to measure rate of progress.

- [x] (2025-01-01T12:00Z) <example completed step>
- [ ] <example incomplete step>
- [ ] <example partial step> (completed: X; remaining: Y)

## Progress (Running Log)

Summaries at each stopping point; always reflect the actual current state.

- (YYYY-MM-DDThh:mmZ) <what changed, where, evidence link(s)>
- (YYYY-MM-DDThh:mmZ) <next focus / blocker>

## Surprises & Discoveries

Document unexpected behaviors, bugs, optimizations, or insights with concise evidence.

- Observation: <what you saw>
  Evidence: `<path/log/screenshot>` or command output
- Observation: <…>
  Evidence: <…>

## Decision Log

Record every decision in this format:

- Decision: <what was chosen>
  Rationale: <why this over alternatives>
  Date/Author: <YYYY-MM-DD • name/handle>
- Decision: <…>
  Rationale: <…>
  Date/Author: <…>

## Risks & Mitigations

- Risk: <impact • likelihood> • Mitigation: <plan/owner/trigger>
- Risk: <…> • Mitigation: <…>

## Dependencies

- Upstream/Downstream: <services, libraries, teams>
- External Events: <releases, migrations, flags, approvals>

## Security / Privacy / Compliance

- Data touched: <PII/none> • Storage/Transit: <details>
- Secrets: <none | how managed> • Threats: <summary>
- Checks: <linters/scanners/tests to run>

## Observability (Optional)

- Metrics: <names, targets, owner>
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

Summarize outcomes, gaps, and lessons learned at milestones or completion. Compare the result against the original purpose and success criteria.

- Result vs Goals: <met/partially/not met> • Evidence: <links>
- What went well: <bullets>
- What to change next time: <bullets>

<!-- Usage Notes:
- Keep Progress, Surprises & Discoveries, Decision Log, and Outcomes & Retrospective up to date as a living document.
- Use ISO‑8601 UTC timestamps (e.g., 2025-10-13T19:00Z).
- Cite exact file paths and symbol names in Plan of Work.
- Acceptance tests are the definition of done.
-->
