# create-execplan v0.3

**Purpose**

- Produce a complete execution plan for `$USER_PROMPT`, using supplied artifacts (spec, inspect report) and targeted research.

## Variables

- `$USER_PROMPT` ← $1 (required)
- `--artifact PATH_OR_URL` (repeatable) ← context files or URLs (e.g., spec, inspect report)
- `--out PATH` (required) ← write the final ExecPlan Markdown to this path and also print the same Markdown to stdout (no preface)

## Instructions

- Read artifacts first (spec, then inspect); extract objectives, constraints, stack details, file references.
- Incorporate global rules (coding standards, quality gates, design principles).
- Use online research for additional analysis; cite official documentation.
- Respond autonomously to any clarifications requested by sub-prompts; favor strict gates and established libraries.
- Output only the final ExecPlan—no preamble—using the template below. Write to `--out` and echo the same Markdown to stdout.

## Workflow

1. **Collect Inputs** – Load all artifacts; summarize salient information (objectives, constraints, target files, success criteria).
2. **Analyze** – Run web search for strategy options; capture reasoning for final approach.
3. **Synthesize** – Convert the recommended solution into the structured plan:
   - Purpose / Big Picture
   - Success Criteria / Acceptance Tests (checkbox list)
   - Context & Orientation (files/modules, constraints)
   - Plan of Work (Prose)
   - Concrete Steps (comprehensive table with file, action type, action)
   - Test Plan & Quality Gates (tables)
   - Progress, Surprises, Decision Log (initial stubs)
   - Risks & Mitigations, Dependencies, Security/Privacy, Observability
   - PR & Review placeholders, Handoff, Outcomes
4. **Emit Plan** – Write to `--out` and print to stdout with no additional commentary.

## Output Template

```markdown
# ExecPlan: <Short, action-oriented title>

- Status: <Proposed|In Progress|Blocked|Complete>
- Repo/Branch: `<owner>/<repo>` • `<branch>`
- Scope: <feature/bug/ops> • Priority: <P0–P3>
- Start: <YYYY-MM-DD> • Last Updated: <ISO8601 UTC>
- Links: <issue/PR/runbook/design/PRD>

## Purpose / Big Picture

<Explain user-visible outcome and business value.>

## Success Criteria / Acceptance Tests

- [ ] <Deterministic check 1>
- [ ] <Deterministic check 2>
- Non-Goals: <explicit exclusions>

## Context & Orientation

- Code: `path/to/file:line`, `path/to/module`
- Data/Contracts: <APIs, schemas, events>
- Constraints/Assumptions: <performance, security, platform>

## Plan of Work (Prose)

1. <High-level action and rationale>
2. <High-level action and rationale>

## Concrete Steps (Checklist)

<!-- a comprehensive list of every single action to be carried out from start to finish -->

| #   | File              | Type  | Action                                                                |
| --- | ----------------- | ----- | --------------------------------------------------------------------- |
| 1   | path/to/file:~123 | Write | Create Authenticate.cs and add login function with email and password |
| 2   | ...               | ...   | ...                                                                   |

## Progress (Running Log)

- (YYYY-MM-DDThh:mmZ) Plan created; awaiting build.

## Surprises & Discoveries

- Observation: <what> • Evidence: `<path/log>`

## Decision Log

- Decision: <what>
  Rationale: <why>
  Date/Author: <YYYY-MM-DD • name>

## Risks & Mitigations

- Risk: <impact • likelihood> • Mitigation: <plan/owner/trigger>

## Dependencies

- Upstream/Downstream: <services, libraries, teams>
- External Events: <releases, approvals>

## Security / Privacy / Compliance

- Data touched: <PII/none>
- Secrets: <none | how managed>
- Checks: <security linters/tests>

## Observability (Optional)

- Metrics: <names, targets>
- Logs/Traces: <keys, sampling>
- Feature Flags/Experiments: <keys, rollout plan>

## Test Plan

- Unit: <scope>
- Integration/E2E: <scope>
- Performance/Accessibility: <budget>
- How to run: `<commands>`

### Quality Gates

| Gate        | Command | Threshold / Expectation |
| ----------- | ------- | ----------------------- |
| Lint        | `<cmd>` | 0 errors                |
| Type        | `<cmd>` | 0 errors                |
| Tests       | `<cmd>` | 100% passing            |
| Duplication | `<cmd>` | ≤ 3%                    |
| Complexity  | `<cmd>` | Max CC ≤ 10             |

## PR & Review

- PR URL: <to be filled>
- PR Number/Status: <number> • <OPEN/APPROVED/MERGED>
- Required Checks: <list> • Last CI run: <status/link>

## Handoff & Next Steps

- Remaining work to productionize: <docs, training, tickets>
- Follow-ups/backlog: <items>

## Outcomes & Retrospective

- Result vs Goals: <met/partially/not met> • Evidence: <links>
- What went well: <bullets>
- What to change next time: <bullets>
```

## Examples

- `/create-execplan "Add MFA to admin console" --artifact .workspace/2025-10-13-add-mfa/spec/spec.md --artifact .workspace/2025-10-13-add-mfa/inspect/report.md --out .workspace/2025-10-13-add-mfa/plan/execplan.md`
