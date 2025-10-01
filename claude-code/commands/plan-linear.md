---
description: Lean objective→autonomous planning→final report workflow for generating a Linear project plan
argument-hint: <artifact-path-or-description> [--project <identifier>] [--config <path>] [--estimate-style {tshirt|none}] [--max-size <XS|S|M|L>] [--dry-run] [--auto] [--diff <baseline.json>] [--report-format {json|markdown|both}] [--debug]
version: 1
---

# plan-linear

## Role

Transform an unstructured planning artifact into an actionable Linear plan by orchestrating stateless subagents:

- Validate arguments & resolve config
- Acquire artifact & extract primitives
- Invoke subagents in strict order to enrich plan state
- Delegate hashing + diff to `@agent-linear-hashing`
- Delegate semantic / structural completeness & gating to `@agent-linear-readiness`
- Assemble and emit a single Final Report (JSON or Markdown)

Never: directly mutate Linear issues (handled only in mutation phase), guess missing mandatory sections, or recompute hashes locally (trust hashing subagent).

## High-Level Execution Flow

1. Parse & validate arguments.
2. Resolve & validate config (compute `config_fingerprint` = sha256(sorted JSON minus volatile fields)).
3. Acquire raw artifact (stdin, piped, or prompt). Empty → error `EMPTY_ARTIFACT`.
4. Establish Objective Frame (`@agent-linear-artifact-classifier`):
   - Summarize: artifact type (after classification), feature count, constraint count, top risks (if any emerge).
   - Construct objective object (see Final Report schema).
5. Autonomous Planning Loop (delegated to subagents):
   - Command gathers initial state (artifact + config subset).
   - Subagents evolve state until plan readiness criteria satisfied:
     - `@agent-linear-context-harvester` → frameworks, languages, existing modules
     - `@agent-linear-design-synthesizer` → architecture decisions, foundation tasks
     - `@agent-linear-issue-decomposer` → atomic issue graph with ids/deps
     - `@agent-linear-estimation-engine` → size, rcs, oversize flags
     - `@agent-linear-acceptance-criteria-writer` → AC, DoD, implementation guidance
     - `@agent-linear-hashing` (compute) → hashes + duplication detection
6. Readiness Check (`@agent-linear-readiness`):
   - Determine readiness and produce readiness object.
   - If readiness.ready=false → abort (exit 2) unless user chooses remediation (not handled inside command; user re-runs after artifact/config edits).
7. Final Report Emission:
   - Build output + enrich with objective + metadata.
   - If `--diff` provided, include change summary (`@agent-linear-hashing` diff).
   - Output according to `--report-format`.
8. Optional Mutation:
   - If not `--dry-run`, confirm (unless `--auto`) then invoke:
     - `@agent-linear-issue-writer` (project init if needed, then issue batch)
     - `@agent-linear-dependency-linker`
     - Integrity of previously computed hashes MUST NOT change post-mutation.
   - Append mutation results into final report under `mutation`.

## Hashing & Diff Delegation

All SHA-256 computation (artifact, per-issue structural hashes, plan hash) and diffing are delegated to `@agent-linear-hashing`. The command treats hashing output as authoritative and never re-hashes locally.

## Arguments

Recognized flags (reject unknowns):

- `--project <identifier>` existing Linear project (UUID | URL | exact name)
- `--config <path>` override config resolution
- `--estimate-style {tshirt|none}` default: `tshirt`
- `--max-size <XS|S|M|L>` upper bound before enforced split (optional)
- `--dry-run` never mutate Linear
- `--auto` skip interactive confirmations (still stops if audit errors)
- `--diff <baseline.json>` structural diff vs prior saved plan (delegated to @agent-linear-hashing diff)
- `--report-format {json|markdown|both}` default: `json`
- `--debug` (optional) include intermediary orchestrator state hashes (no raw large payload dump)

Validation failures: print concise JSON error envelope + exit code 1.

## Config Resolution

Locate config with following precedence:

1. Explicit `--config`
2. Project-level `.opencode/linear-plan.config.json`
3. User-level `$HOME/.config/opencode/linear-plan.config.json`

Mandatory keys (no inference): `label_rules`, `complexity_weights`, `thresholds`, `decomposition`, `audit_rules`, `idempotency`.
If any missing → **STOP** emit exit code 1.

## Subagent Responsibilities

| Subagent                          | Responsibility                             | Key Outputs                                                            |
| --------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------- |
| linear-artifact-classifier        | Normalize + extract primitives             | artifact_type, features[], constraints[], assumptions[]                |
| linear-context-harvester          | Repo / stack composition signals           | frameworks[], languages[], existing_modules[]                          |
| linear-design-synthesizer         | Architecture & foundation scaffold         | architecture_decisions[], foundation_tasks[]                           |
| linear-issue-decomposer           | Atomic issue graph                         | issues[] (ids, deps, category)                                         |
| linear-estimation-engine          | Complexity & sizing                        | size, rcs, oversize_flag                                               |
| linear-acceptance-criteria-writer | Outcome & quality enrichment               | acceptance_criteria[], definition_of_done[], implementation_guidance[] |
| linear-hashing                    | Deterministic hashing + duplication + diff | plan_hash, artifact hashes, per-issue hashes, duplicates, diff         |
| linear-readiness                  | Validation + labeling + readiness gating   | findings[], label_assignments[], dependency_suggestions[], readiness{} |
| linear-issue-writer               | Project / issue creation                   | project_id, created_issue_ids[]                                        |
| linear-dependency-linker          | Apply dependency edges                     | applied_edges[]                                                        |

## Readiness Handling

The command delegates all readiness determination to `@agent-linear-readiness`. If `readiness.ready=false`, the command aborts with exit code 2 and displays the readiness object including `pending_steps` for user remediation. If `readiness.ready=true`, the command proceeds to final report emission and optional mutation.

## Diff Mode

When `--diff <baseline.json>` is provided, the command compares the current plan against a previously saved plan and embeds the change summary under `"diff"` in the final report.

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
    "readiness": {
      "ready": true,
      "requires_split": false,
      "pending_steps": [],
      "advisories": [],
      "plan_hash": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "timestamp": "2025-09-30T12:34:56Z"
    },
    "diff": { "added": [], "removed": [], "changed": [] } // present only when --diff used
  }
}
```

> Markdown output (if selected) is a faithful rendering of the JSON with a deterministic section order; JSON is canonical.

## Final Report Output

The command generates appropriately named output files based on the selected format:

### File Naming Convention

**Default naming** (when no project specified):

- JSON: `plan-linear-report-YYYY-MM-DDTHH-MM-SSZ.json`
- Markdown: `plan-linear-report-YYYY-MM-DDTHH-MM-SSZ.md`

**Project-specific naming** (when `--project` provided):

- JSON: `plan-linear-{project-slug}-YYYY-MM-DDTHH-MM-SSZ.json`
- Markdown: `plan-linear-{project-slug}-YYYY-MM-DDTHH-MM-SSZ.md`

**Examples:**

```bash
# Default naming
/plan-linear "Add user authentication" --report-format json
# Output: plan-linear-report-2025-09-30T15-30-00Z.json

# Project-specific naming
/plan-linear "Add user authentication" --project "Auth Q4 2025" --report-format markdown
# Output: plan-linear-auth-q4-2025-2025-09-30T15-30-00Z.md

# Both formats
/plan-linear "Add user authentication" --report-format both
# Output: plan-linear-report-2025-09-30T15-30-00Z.json + plan-linear-report-2025-09-30T15-30-00Z.md
```

### Output Behavior

- **JSON format**: Always written to file, also printed to stdout
- **Markdown format**: Written to file, summary printed to stdout
- **Both formats**: Both files written, JSON content printed to stdout
- **Dry-run**: Files created with `-dry-run` suffix in filename
- **Error conditions**: No output files created, error envelope printed to stderr

### File Content Structure

**JSON files** contain the complete `PlanLinearReport` object as shown in the schema above.

**Markdown files** contain:

- Executive summary (objective, issue counts, readiness status)
- Detailed sections (decisions, foundation tasks, issues by category)
- Complexity analysis and sizing breakdown
- Dependencies and labels summary
- Readiness findings and any advisories
- Hash verification section
- Mutation results (if applicable)
- Diff summary (if `--diff` used)

Files are written to the current working directory unless `--output-dir` is specified (future enhancement).

## Failure & Exit Codes

| Code | Meaning                                               |
| ---- | ----------------------------------------------------- |
| 0    | Success (dry-run or mutation complete)                |
| 1    | Argument or config validation failure                 |
| 2    | Plan readiness failures or blocking validation errors |
| 3    | Linear mutation failures (writer/linker errors)       |
| 4    | Structural integrity or contract violations           |

All errors must output a machine-parsable JSON envelope with `exit_code` and `error.code` fields.

### Error Code Mapping

**Exit Code 1 (Argument/Config Failures):**

- `CONFIG_MISSING_KEYS` → Required configuration keys absent
- `ARG_VALIDATION` → Invalid flag combinations or values
- `EMPTY_ARTIFACT` → No planning input provided

**Exit Code 2 (Readiness/Validation Failures):**

- `READINESS_BLOCKING` → Plan not ready for Linear (from @agent-linear-readiness)
- `MISSING_FEATURES` → No extractable features from artifact
- `NO_ISSUES` → Issue decomposition produced no issues or no issues available for enrichment
- `EMPTY_REPO` → No source code context available
- `NO_FOUNDATION` → Features require foundation tasks but none provided
- `SPLIT_TARGET_NOT_FOUND` → Cannot locate target for issue splitting
- `MISSING_OBJECTIVES` → Objectives empty and cannot reference success alignment

**Exit Code 3 (Linear Mutation Failures):**

- `RATE_LIMIT` → Linear API rate limit exceeded
- `PERMISSION_DENIED` → Insufficient Linear permissions
- `NOT_FOUND_PROJECT` → Specified project not found
- `VALIDATION_ERROR` → Linear rejected issue data
- `MUTATION_FAILED` → Generic Linear mutation failure
- `NO_DEPENDENCIES` → No dependencies to link (non-fatal, may not need linking)
- `MISSING_PROJECT_ID` → Project ID required for dependency linking operations

**Exit Code 4 (Structural/Contract Violations):**

- `SCHEMA_VIOLATION` → Malformed input to subagents
- `DUPLICATE_ISSUE_ID` → Conflicting issue identifiers
- `DUPLICATE_ISSUE_HASH` → Structural duplicates detected
- `HASH_MISMATCH` → Hash verification failed
- `MALFORMED_DEP_GRAPH` → Invalid dependency structure
- `ORCHESTRATOR_CONTRACT_VIOLATION` → Missing required workflow segments

### Subagent Error Consistency

All subagents follow the same error envelope pattern:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {
      /* optional context */
    }
  }
}
```

Subagents return findings/warnings in normal output; only hard failures use the error envelope. The command maps subagent error codes to appropriate exit codes as listed above.

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
# Output: plan-linear-report-2025-09-30T15-30-00Z.json
```

> Attach to an existing project and output Markdown

```bash
/plan-linear "Add deep research agent using vercel AI Agent SDK" --project "Auth Hardening 2025" --report-format markdown
# Output: plan-linear-auth-hardening-2025-2025-09-30T15-30-00Z.md
```

> Set out plan based on prd artifact with tshirt sizing and max size of L

```bash
/plan-linear prd.md --estimate-style tshirt --max-size L
# Output: plan-linear-report-2025-09-30T15-30-00Z.json
```

> Non-interactive apply (attach to project and apply changes)

```bash
/plan-linear "add website visitor ticket to home page" --project PROJ-123 --auto
# Output: plan-linear-website-visitor-ticket-2025-09-30T15-30-00Z.json + Linear mutations
```

### Diff mode example

This shows exactly how adding MFA requirements changed the issue breakdown, sizing, and dependencies.

> First run

```bash
/plan-linear "Add user authentication" --dry-run > plan-v1.json
```

> Later, after modifying requirements

```bash
/plan-linear "Add user authentication with MFA" --diff plan-v1.json --dry-run
```

---
