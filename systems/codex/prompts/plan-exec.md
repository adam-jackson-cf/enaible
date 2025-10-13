# plan-exec v0.1

**Purpose**

- Transform a user objective (`USER_PROMPT`) into a concrete execution plan formatted exactly to `systems/codex/execplan.md`.

**Arguments**

- `USER_PROMPT` (required): The objective/problem to solve. Provide as a quoted argument.
- `--artifact PATH_OR_URL` (optional, repeatable): Supplemental context to ground the plan. May be a file path or an HTTP(S) URL. Specify multiple times to include multiple artifacts.

## Instructions

- Expect to be provided sufficient context via the prompt and optional artifacts; produce a detailed plan in the required ExecPlan format.
- Use a two-gate interactive flow:
  - Gate A (Clarify): Ask targeted questions to resolve ambiguities. Allow multiple back-and-forth rounds until the user replies "continue".
  - Gate B (Review): Present a full Draft ExecPlan for redlines. Allow multiple rounds ("revise:") until user replies "approve" to finalize.
- When artifacts are provided:
  - For file paths: read relevant portions only; reference findings with `path:line` when useful.
  - For URLs: fetch text content only; ignore binaries; summarize key facts; cite source.
- Evidence-led writing: tie each plan element to available context or artifacts; when unknowns remain after Gate A, document explicit assumptions and proceed.
- Output only the requested block at each gate (Clarification → Draft → Final). Do not include extra narrative around the plan in the final output.

## Workflow

1. Parse Inputs

   - Capture `USER_PROMPT` and any `--artifact` values in order.
   - Normalize artifacts into a list; classify each as `file` or `url` by scheme/presence on disk.

2. Artifact Collection (Optional)

   - Files: inspect size and peek headers (e.g., `sed -n '1,200p' <file>`); skip clearly binary files; extract relevant snippets.
   - URLs: `curl -Ls --max-time 20` text responses only; strip HTML to text if needed; record title/headers.
   - Build a brief evidence index with pointers: `source`, `path_or_url`, and a one-line summary.

3. Initial Analysis

   - Derive scope, constraints, stakeholders, data/contracts, and risks from prompt + artifacts.
   - Draft acceptance tests and initial success metrics.
   - Identify unknowns/assumptions requiring user input.

4. Gate A — Clarification Loop

   - Output a "Clarification" block (see Output section) containing:
     - A one-paragraph synopsis of the problem as currently understood
     - An enumerated list of clarifying questions
     - A compact list of explicit assumptions (only those necessary to proceed)
     - A minimal list of inputs/artifacts still desired (if any)
   - Wait for user responses. Repeat this step until the user replies "continue".

5. Draft Plan Construction

   - Populate an ExecPlan using the canonical section structure from `systems/codex/execplan.md`.
   - Set `Status: Proposed`; `Start: <today>`; `Last Updated: <ISO8601 UTC>`.
   - Include concrete, verifiable Acceptance Tests and a file-scoped Plan of Work (paths + symbol names).
   - Reference evidence from artifacts where applicable.

6. Gate B — Review Loop

   - Output a "DRAFT ExecPlan" block for redlines. Invite "revise: <instructions>" or "approve".
   - Incorporate user feedback and re-issue the draft until "approve".

7. Finalization
   - Output the final ExecPlan only (no preface), fully conforming to the template and reflecting all accepted feedback.

## Output

### Clarification Block (Gate A)

```markdown
# Clarification

**Understanding**

- <one-paragraph synopsis>

**Questions**

1. <question>
2. <question>

**Assumptions (to proceed)**

- <assumption>

**Optional Inputs**

- <artifact or data still useful>
```

### Draft ExecPlan (Gate B)

Label the plan as DRAFT at the top and follow the ExecPlan structure exactly.

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

## Handoff & Next Steps

- Remaining work to productionize: <docs, training, tickets>
- Follow‑ups/backlog: <links or bullets>

## Outcomes & Retrospective

- Result vs Goals: <met/partial/not> • Evidence: <links>
- What went well: <bullets>
- What to change next time: <bullets>
```

After emitting the draft, append the following single line to initiate Gate B:

```
STOP → "Provide redlines with `revise: ...` or reply `approve` to finalize."
```

### Final ExecPlan (Approval Granted)

- Output only the finalized ExecPlan content (same structure as above, without the DRAFT label or STOP line). No preamble.

## Examples

- `/plan-exec "Implement feature-flagged staged rollout for the new checkout"`
- `/plan-exec "Migrate from local SQLite to managed Postgres with Drizzle" --artifact ./services/api/src/db/schema.ts --artifact https://example.com/current-sla`
- `/plan-exec "Reduce React hydration cost on marketing pages" --artifact web/src/routes/_layout.tsx`

$ARGUMENTS
