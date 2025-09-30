---
description: Lean objective→autonomous planning→final report workflow for generating a Linear project plan
version: 1
---

# plan-linear

## Role

Transform an unstructured planning artifact into an actionable Linear plan:

- Validates arguments + resolves config
- Verifies readiness (no blocking audit errors)
- Emits a single Final Report (JSON or Markdown)

You do so by running the linear workflow - invoking relevant subagents, managing their required inputs and outputs:

1. Merge incremental subagent JSON outputs into a single canonical `plan_state` object.
2. Compute and verify stable SHA-256 hashes for: raw_artifact, normalized_artifact, issues[].
3. Perform structural validation (schema presence / required fields) before each STOP gate.
4. Generate a deterministic `plan_preview` (Phase 5) when requested.
5. Provide diff summaries (added/changed/removed issues) across re-runs using hash lineage.

Never: create issues, mutate Linear, apply labels, or infer missing sections.

## High-Level Execution Flow

1. Parse & validate arguments.
2. Resolve & validate config (compute `config_fingerprint` = sha256(sorted JSON minus volatile fields)).
3. Acquire raw artifact (stdin, piped, or prompt). Empty → error `EMPTY_ARTIFACT`.
4. Establish Objective Frame:
   - Summarize: artifact type (after classification), feature count, constraint count, top risks (if any emerge).
   - Construct objective object (see Final Report schema).
5. Autonomous Planning Loop (delegated to subagents):
   - Command gathers initial state (artifact + config subset).
   - Subagents evolve state until plan readiness criteria satisfied.
6. Readiness Check:
   - Marks `readiness.ready=true` with enumerated unmet optional enhancements (`advisories[]`).
   - If `audit.errors` non-empty → abort (exit 2) unless user chooses remediation (not handled inside command; user re-runs after artifact/config edits).
7. Final Report Emission:
   - Build output + enrich with objective + metadata.
   - Output according to `--report-format`.
8. Optional Mutation:
   - If not `--dry-run`, confirm (unless `--auto`) then invoke:
     - `@linear-issue-writer` (project init if needed, then issue batch)
     - `@linear-dependency-linker`
     - `@linear-quality-auditor` verify project tasks coherence and consistency
   - Append mutation results into final report under `mutation`.

## Arguments

Recognized flags (reject unknowns):

- `--project <identifier>` existing Linear project (UUID | URL | exact name)
- `--config <path>` override config resolution
- `--estimate-style {tshirt|none}` default: `tshirt`
- `--max-size <XS|S|M|L>` upper bound before enforced split (optional)
- `--dry-run` never mutate Linear
- `--auto` skip interactive confirmations (still stops if audit errors)
- `--report-format {json|markdown|both}` default: `json`
- `--list-subagents` list subagent index (from orchestrator) then exit 0
- `--debug` (optional) include intermediary orchestrator state hashes (no raw large payload dump)

Validation failures: print concise JSON error envelope + exit code 1.

## Config Resolution

Precedence:

1. Explicit `--config`
2. Project-level `.opencode/linear-plan.config.json`
3. User-level `$HOME/.config/opencode/linear-plan.config.json`

Mandatory keys (no inference): `label_rules`, `complexity_weights`, `thresholds`, `decomposition`, `audit_rules`, `idempotency`.
If any missing → **STOP** emit exit code 1.

## Subagent Responsibilities

| Subagent                          | Role Focus                        | Key Signal                      |
| --------------------------------- | --------------------------------- | ------------------------------- |
| linear-artifact-classifier        | Normalize + extract primitives    | artifact_type, features[]       |
| linear-context-harvester          | Repo composition signals          | frameworks[], languages[]       |
| linear-design-synthesizer         | Decisions + foundation scaffold   | foundation_tasks[]              |
| linear-issue-decomposer           | Atomic issue set                  | issues[] (provisional)          |
| linear-estimation-engine          | RCS + size                        | rcs, size                       |
| linear-acceptance-criteria-writer | AC + DoD + guidance               | acceptance_criteria[]           |
| linear-quality-auditor            | Validation & labeling hints       | findings[], label_assignments[] |
| linear-orchestrator               | Merge, hashes, readiness, preview | plan_state, readiness           |
| linear-issue-writer               | Project / issue creation          | created_issue_ids[]             |
| linear-dependency-linker          | Apply blocking edges              | applied_edges[]                 |

## Plan Readiness Criteria

Set `readiness.ready=true` only if ALL:

- Classified artifact fields present (`features[]`, `constraints[]` maybe empty but defined)
- Context harvested (`frameworks[]` OR `languages[]` non-empty)
- Design synthesized (`architecture_decisions[]` & `foundation_tasks[]` may be empty only if provably unnecessary)
- Issues decomposed (≥1)
- Estimation applied (`size`, `rcs` for all issues)
- Enrichment applied (`acceptance_criteria` & `definition_of_done` present per issue)
- Audit executed with `audit.errors.length == 0`
- Plan hash computed

"readiness": { "ready": true|false, "pending_steps": ["estimation","audit"], "advisories": ["Some large issues could be further split"], "plan_hash": "sha256" }

## Final Output Report (Canonical Schema)

```json
{
  "PlanLinearReport": {
    "version": 2,
    "objective": {
      "summary": "Deliver authentication hardening for user-facing API",
      "artifact_type": "prd",
      "features": [
        "mfa-for-admins",
        "rotate-api-keys",
        "session-expiry-improvements"
      ],
      "constraints": ["no-db-schema-changes", "release-window:2025-Q4"],
      "success_criteria": [
        "all critical endpoints require MFA for admin roles",
        "no regressions in login latency > 100ms"
      ],
      "assumptions": [
        "backwards-compatible client SDKs",
        "sufficient QA cycles"
      ],
      "risks": [
        "third-party SSO outage impact",
        "increased support tickets post-launch"
      ],
      "open_questions": [
        "Which identity provider is canonical for SSO?",
        "Do we deprecate legacy API keys?"
      ]
    },
    "planning": {
      "decisions": [
        {
          "decision": "Adopt staged rollout for MFA",
          "rationale": "Mitigates support load and enables telemetry-driven adjustments"
        }
      ],
      "foundation_tasks": [
        {
          "id": "FT-001",
          "title": "Create MFA onboarding docs"
        },
        {
          "id": "FT-002",
          "title": "Add feature flag for staged rollout"
        }
      ],
      "issue_totals": {
        "total": 12,
        "foundation": 2,
        "feature": 8,
        "risk": 2
      },
      "complexity": {
        "sizes": {
          "XS": 1,
          "S": 4,
          "M": 5,
          "L": 2,
          "XL": 0
        },
        "rcs_min": 1,
        "rcs_max": 8,
        "oversize": ["ISS-010"]
      },
      "labels": {
        "by_category": {
          "foundation": ["type:foundation"],
          "feature": ["type:feature"]
        }
      },
      "glossary": [
        {
          "term": "RCS",
          "definition": "Relative complexity score used for sizing"
        }
      ],
      "dependencies": {
        "edges": 5,
        "roots": ["ISS-001"],
        "leaves": ["ISS-020"]
      },
      "audit": {
        "errors": [],
        "warnings": [
          {
            "code": "WARN_SPLIT_RECOMMENDATION",
            "issue_id": "ISS-010",
            "message": "Consider splitting large issue ISS-010 into smaller deliverables"
          }
        ]
      },
      "hashes": {
        "artifact_raw": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "artifact_normalized": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "plan": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
        "config_fingerprint": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
      }
    },
    "mutation": {
      "project_id": "LINPROJ-123",
      "created_issue_ids": ["LIN-101", "LIN-102", "LIN-103"],
      "skipped_issue_ids": ["ISS-999"],
      "linked_edges": [
        {
          "from": "LIN-101",
          "to": "LIN-102"
        }
      ],
      "cycle_warnings": []
    },
    "status": {
      "ready": true,
      "requires_split": false,
      "timestamp": "2025-09-30T12:34:56Z"
    }
  }
}
```

> Markdown output (if selected) is a faithful rendering of the JSON with a deterministic section order; JSON is canonical.

## Idempotency

- Trust orchestrator hashes (`plan_hash`, `hash_issue`).
- Command does NOT recompute or mutate structure; it only verifies shape presence.
- Re-run with unchanged artifact + config → identical `plan_hash` and deterministic output ordering.

## Failure & Exit Codes

| Code | Meaning                                                                                           |
| ---- | ------------------------------------------------------------------------------------------------- |
| 0    | Success (dry-run or mutation complete)                                                            |
| 1    | Argument or config validation failure (e.g., CONFIG_MISSING_KEYS)                                 |
| 2    | Audit blocking errors (plan not ready, e.g., AUDIT_BLOCKING)                                      |
| 3    | Linear mutation failure (writer/linker error, e.g., LINEAR_MUTATION_FAILURE)                      |
| 4    | Orchestrator contract violation (missing required segment, e.g., ORCHESTRATOR_CONTRACT_VIOLATION) |

Errors must output a machine-parsable JSON envelope that includes a numeric exit_code and an error.code string that corresponds to the numeric exit code above.

Common error.code → exit_code mapping:

- CONFIG_MISSING_KEYS → 1
- ARG_VALIDATION → 1
- AUDIT_BLOCKING → 2
- LINEAR_MUTATION_FAILURE → 3
- ORCHESTRATOR_CONTRACT_VIOLATION → 4

Example JSON error envelope (config-missing example, exit code 1):

```json
{
  "exit_code": 1,
  "error": {
    "code": "CONFIG_MISSING_KEYS",
    "message": "Required configuration keys are missing",
    "details": {
      "missing": [
        "label_rules",
        "complexity_weights",
        "thresholds",
        "decomposition",
        "audit_rules",
        "idempotency"
      ],
      "path": "/home/adam/.config/opencode/linear-plan.config.json",
      "attempted_sources": [
        "--config (not provided)",
        ".opencode/linear-plan.config.json",
        "$HOME/.config/opencode/linear-plan.config.json"
      ]
    }
  }
}
```

## Usage Examples

> Dry run (JSON only)

```bash
/plan-linear "Add google signin support to authentication module" --dry-run --estimate-style tshirt
```

> Attach to an existing project and output Markdown

```bash
/plan-linear "Add deep research agent using vercel AI Agent SDK" --project "Auth Hardening 2025" --report-format markdown
```

> Set out plan based on prd artifact with tshirt sizing and max size of L

```bash
/plan-linear prd.md --estimate-style tshirt --max-size L
```

> Non-interactive apply (attach to project and apply changes)

```bash
/plan-linear "add website visitor ticket to home page" --project PROJ-123 --auto
```
