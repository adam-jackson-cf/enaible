# plan-exec v0.1

## Purpose

Transform a user objective into a concrete execution plan formatted exactly to ExecPlan.

## Variables

- `$USER_PROMPT` ← first positional argument (required)
- `$ARTIFACT` ← `--artifact PATH_OR_URL` (optional, repeatable)
- `$ARGUMENTS` ← raw argument string

Resolution rules

- Resolve `$USER_PROMPT` and collect all `$ARTIFACT` values at INIT; treat artifacts as an ordered list `$ARTIFACTS`.
- Classify each `$ARTIFACT` as `file` (exists on disk) or `url` (http/https). Use only resolved variables in the workflow.

## Instructions

- Expect sufficient context via `$USER_PROMPT` and optional `$ARTIFACTS`; produce a detailed plan in ExecPlan format.
- Two-gate interactive flow with multi‑round loops:
  - Gate A (Clarify): Ask targeted questions until the user replies `continue`.
  - Gate B (Review): Present a Draft ExecPlan for redlines; iterate on `revise: ...` until the user replies `approve`.
- When artifacts are provided:
  - Files: read relevant portions only; reference findings with `path:line` when useful.
  - URLs: fetch text content only; ignore binaries; summarize key facts; cite source.
- Evidence‑led writing: tie plan elements to context or artifacts; if unknowns remain after Gate A, state assumptions explicitly.
- Output only the requested block at each gate within the Workflow. The final Output section returns the approved plan only.

## Workflow

1. INIT — Parse Inputs

- Resolve `$USER_PROMPT`; collect `$ARTIFACTS` in order and classify each as file/url.

2. COLLECT — Artifact Collection (Optional)

- Files: peek headers (e.g., `sed -n '1,200p' "$FILE"`); skip binaries; extract relevant snippets.
- URLs: `curl -Ls --max-time 20 "$URL"` for text only; strip HTML where needed; capture title/headers.
- Build a brief evidence index: source, path_or_url, one‑line summary.

3. ANALYZE — Initial Analysis

- Derive scope, constraints, stakeholders, data/contracts, and risks from `$USER_PROMPT` + `$ARTIFACTS`.
- Draft acceptance tests and initial success metrics.
- Identify unknowns/assumptions for Gate A.

4. Gate A — Clarification Loop

- Emit a Clarification block and wait for responses; repeat until `continue`.

```markdown
# Clarification

**Understanding**

- <one‑paragraph synopsis>

**Questions**

1. <question>
2. <question>

**Assumptions (to proceed)**

- <assumption>

**Optional Inputs**

- <artifact or data still useful>
```

5. DRAFT — Plan Construction

- Populate an ExecPlan per `systems/codex/execplan.md`.
- Set `Status: Proposed`; set dates (`Start: <today>`, `Last Updated: <ISO8601 UTC>`).
- Include concrete, verifiable Acceptance Tests; file‑scoped Plan of Work (paths + symbols).
- Reference evidence from `$ARTIFACTS` where applicable.

6. Gate B — Review Loop

- Emit a DRAFT ExecPlan for redlines; accept `revise: ...` or `approve`.

```markdown
# DRAFT — ExecPlan: <Short, action‑oriented title>

- Status: Proposed
- Repo/Branch: `<owner>/<repo>` • `<branch>`
- Scope: <feature/bug/ops task> • Priority: <P0–P3>
- Start: <YYYY-MM-DD> • Last Updated: <ISO8601 UTC>
- Links: <issue/PR/runbook/design/PRD>

## Purpose / Big Picture

<concise description>

## Success Criteria / Acceptance Tests

- [ ] <Deterministic check 1>
- [ ] <Deterministic check 2>
- Non‑Goals: <excluded areas>

## Context & Orientation

- Code: `path/to/fileA:line`, `path/to/moduleB`
- Data/Contracts: <APIs, schemas, events>
- Constraints/Assumptions: <performance, security, platform>

## Plan of Work (Prose)

- Edit 1: `path/to/file.ts:functionName` — <what/why>
- Edit 2: `path/to/other.py:Class.method` — <what/why>

## Concrete Steps (Checklist)

- [ ] <step>
- [ ] <step>

## Progress (Running Log)

- (<ISO8601>) <update>

## Surprises & Discoveries

- Observation: <what> • Evidence: `<path/log>`

## Decision Log

- Decision: <what>
  Rationale: <why>
  Date/Author: <YYYY-MM-DD • name>

## Risks & Mitigations

- Risk: <impact • likelihood> • Mitigation: <plan>

## Dependencies

- Upstream/Downstream: <services, libraries>
- External Events: <releases, migrations>

## Security / Privacy / Compliance

- Data touched: <PII/none> • Storage/Transit: <details>
- Secrets: <none | how managed> • Threats: <summary>
- Checks: <linters/scanners/tests to run>

## Observability (Optional)

- Metrics: <names, targets>
- Logs/Traces: <keys>

## Test Plan

- Unit: <scope>
- Integration/E2E: <paths>
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
```

After emitting the draft, append this line:

```
STOP → "Provide redlines with `revise: ...` or reply `approve` to finalize."
```

7. FINAL — Finalization

- Output the approved ExecPlan only (no preface), conforming to the template and all accepted feedback.

## Output

- Final approved ExecPlan only (no preface), formatted per ExecPlan.

## Examples

- `/plan-exec "Implement feature-flagged staged rollout for the new checkout"`
- `/plan-exec "Migrate from local SQLite to managed Postgres with Drizzle" --artifact ./services/api/src/db/schema.ts --artifact https://example.com/current-sla`
- `/plan-exec "Reduce React hydration cost on marketing pages" --artifact web/src/routes/_layout.tsx`

$ARGUMENTS
