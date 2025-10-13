# create-execplan v0.1

**Purpose**

- Produce a complete execution plan (ExecPlan) for `$USER_PROMPT` from supplied artifacts and targeted online research, conforming to `systems/codex/execplan.md`.

## Variables

- `$USER_PROMPT` ← first positional argument (required)
- `--artifact PATH_OR_URL` (repeatable) ← paths or URLs providing context (e.g., spec, inspect report)

## Instructions

- Read artifacts first (spec, then inspect); extract objective, constraints, stack, and file/module references.
- Incorporate project/user rules from `./AGENTS.md` and `~/.codex/AGENTS.md` (quality gates, stack conventions, security posture).
- Use online research and always call `/plan-solution` for analysis; cite official documentation.
- Answer clarifications autonomously from artifacts and rules; favor strict gates and established libraries.
- Output only the final ExecPlan (no preface), in `systems/codex/execplan.md` shape.

## Workflow

1. Collect Inputs

   - Load all `--artifact` values (local files or URLs). For URLs, summarize key facts; for files, extract salient sections (objective, constraints, tech stack, modules).
   - If present, read `./AGENTS.md` and `~/.codex/AGENTS.md` to form a concise rules digest.

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
   - Output the final ExecPlan text only.

## Output

- Final ExecPlan content only (no preface), compliant with `systems/codex/execplan.md`.

## Examples

- `/create-execplan "Add MFA to admin console" --artifact .workspace/orchestrate/2025-10-13/spec.md --artifact .workspace/orchestrate/2025-10-13/inspect.md`
