---
description: Workflow for generating a Linear project plan based on a task outline or planning artifact
argument-hint: --task <string-or-file-path> [--linear-project-id <identifier>] [--config <path>] [--estimate-style {tshirt|none}] [--max-size <XS|S|M|L>]
version: 3
---

# plan-linear

## Role

Transform an unstructured planning artifact into an actionable Linear plan by orchestrating asset creation, user feedback and stateless subagents through a multi stepped workflow you must follow exactly in its order of execution.

Never: directly mutate Linear issues (handled only in mutation phase), guess missing mandatory sections, or recompute hashes locally (trust hashing subagent).

## High-Level Execution Flow

**CRITICAL** work through this 9 step workflow sequentially:

1. Parse & validate arguments.
2. Workspace Initialization:
   - Look for `.workspace` folder in project root (create if doesnt exist)
3. Resolve & validate config (compute `config_fingerprint` = sha256(sorted JSON minus volatile fields)).
4. Acquire raw artifact via `--task` (string or file path). Empty → throw error `EMPTY_ARTIFACT`.
5. Establish Objective Frame - invoke `@agent-linear-artifact-classifier` passing raw artifact.
6. Project Initialization:
   - Establish deterministic `PROJECT_DIR` name using kebab-case slug with no spaces:
   - `project_slug = kebab_case(lowercase(objective_frame.project_name or primary_feature))`
   - Use `PROJECT_DIR` exactly as defined above (create if doesnt exist).
7. Summarize: artifact type (after classification), feature count, constraint count, top risks (if any emerge)

**⚠️ PAUSE FOR REQUIRED USER CONFIRMATION**: Ask user "Initialisation complete, is objective frame correct? (y/n)" and WAIT for response before continuing to step 6. If user responds "n" or "no", stop workflow execution and work with user on amends until they explicitly confirm `proceed`.

6. Autonomous Planning Loop (delegated to subagents), evolve `project_plan_report.json` state until plan readiness criteria satisfied:

   - Subagents are invoked sequentially, never in parallel, as they rely on the findings of the previously invoked agent
   - Subagents MUST follow Workspace IO Contract (below) and write three artifacts per run into `PROJECT_DIR`:
     1. `<agent-name>-input.md` — exact task payload the subagent received (for traceability)
     2. `<agent-name>-summary.md` — concise human-readable summary of findings
     3. `<agent-name>-output.json` — machine-readable full output
   - Filenames strictly use the full agent name (e.g., `linear-estimation-engine-output.json`). No abbreviations or spaces.
   - Subagents are instructed to review the previous agents findings:

     - `@agent-linear-context-harvester` → frameworks, languages, existing modules
     - `@agent-linear-design-synthesizer` → architecture decisions, foundation tasks
     - `@agent-linear-issue-decomposer` → atomic issue graph with ids/deps
       <estimate-style if --estimate-style = tshirt>
       - `@agent-linear-estimation-engine` → size, rcs, oversize flags
         </estimate-style>
     - `@agent-linear-acceptance-criteria-writer` → AC, DoD, implementation guidance
     - `@agent-linear-hashing` (compute) → hashes + duplication detection

   - Update the `project_plan_report.json`, as each subagent completes, with the latest findings

7. Readiness Check (`@agent-linear-readiness`):
   - Determine readiness and produce readiness object.
   - If readiness.ready=false → exit 2 unless user chooses remediation.

**⚠️ PAUSE FOR REQUIRED USER CONFIRMATION**: Ask user "Plan formed and readiness check successful, proceed with transfer to linear? (y/n)" and WAIT for response before continuing to step 8. If user responds "n" or "no", stop workflow execution and exit.

8. Optional Mutation:
   - Invoke `@agent-linear-issue-writer` (duplicate detection, project/cycle logic, then issue batch)
   - Invoke `@agent-linear-dependency-linker`
   - Integrity of previously computed hashes MUST NOT change post-mutation.
   - Append mutation results into `project_plan_report.json` under `mutation`.

## Hashing & Diff Delegation

All SHA-256 computation (artifact, per-issue structural hashes, plan hash) and diffing are delegated to `@agent-linear-hashing`. The command treats hashing output as authoritative and never re-hashes locally.

## Arguments

Recognized argument flags (reject unknowns):

**Required:**

- `--task <string-or-file-path>` planning artifact as string or path to file

**Optional:**

- `--linear-project-id <identifier>` existing Linear project (UUID | URL | exact name)
- `--config <path>` override config resolution
- `--estimate-style {tshirt|none}` default: `tshirt`
- `--max-size <XS|S|M|L>` upper bound before enforced split

On validation failures: → **STOP** emit exit code 1.

## Config Resolution

Locate config with following precedence:

1. Explicit `--config`
2. Project-level `.claude/linear-plan.config.json`
3. User-level `$HOME/.claude/linear-plan.config.json`

Mandatory keys (no inference): `label_rules`, `complexity_weights`, `thresholds`, `decomposition`, `audit_rules`, `idempotency`.

On missing missing config keys: → **STOP** emit exit code 1.

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

- `TOOLS_UNAVAILABLE` → Required Linear MCP tools not accessible
- `RATE_LIMIT` → Linear API rate limit exceeded
- `PERMISSION_DENIED` → Insufficient Linear permissions
- `NOT_FOUND_PROJECT` → Specified project not found
- `VALIDATION_ERROR` → Linear rejected issue data
- `MUTATION_FAILED` → Generic Linear mutation failure
- `NO_DEPENDENCIES` → No dependencies to link (non-fatal, may not need linking)
- `MISSING_PROJECT_ID` → Project ID required for dependency linking operations
- `NETWORK_ERROR` → Network connectivity issues
- `AGENT_ACTION_FAILED` → Agent failed to perform required actions

**Exit Code 4 (Structural/Contract Violations):**

- `SCHEMA_VIOLATION` → Malformed input to subagents
- `DUPLICATE_ISSUE_ID` → Conflicting issue identifiers
- `DUPLICATE_ISSUE_HASH` → Structural duplicates detected
- `HASH_MISMATCH` → Hash verification failed
- `MALFORMED_DEP_GRAPH` → Invalid dependency structure
- `ORCHESTRATOR_CONTRACT_VIOLATION` → Missing required workflow segments

### Subagent Error Consistency

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

if an **Error condition** is met: _Immediately_ exit workflow, error envelope printed to stderr

## Subagent Responsibilities

| Subagent                          | Responsibility                                | Key Outputs                                                            |
| --------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------- |
| linear-artifact-classifier        | Normalize + extract primitives                | artifact_type, features[], constraints[], assumptions[]                |
| linear-context-harvester          | Repo / stack composition signals              | frameworks[], languages[], existing_modules[]                          |
| linear-design-synthesizer         | Architecture & foundation scaffold            | architecture_decisions[], foundation_tasks[]                           |
| linear-issue-decomposer           | Atomic issue graph                            | issues[] (ids, deps, category)                                         |
| linear-estimation-engine          | Complexity & sizing                           | size, rcs, oversize_flag                                               |
| linear-acceptance-criteria-writer | Outcome & quality enrichment                  | acceptance_criteria[], definition_of_done[], implementation_guidance[] |
| linear-hashing                    | Deterministic hashing + duplication + diff    | plan_hash, artifact hashes, per-issue hashes, duplicates, diff         |
| linear-readiness                  | Validation + labeling + readiness gating      | findings[], label_assignments[], dependency_suggestions[], readiness{} |
| linear-issue-search               | Duplicate issue detection (existing projects) | matching_issues[], confidence_scores[], duplicate_warnings[]           |
| linear-issue-writer               | Project/cycle creation + issue batch          | project_id, cycle_id, created_issue_ids[], project_url, issue_urls[]   |
| linear-dependency-linker          | Apply dependency edges                        | applied_edges[]                                                        |

## Project Plan Report (Canonical Schema)

```json
{
  "ProjectName": {
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
      "project_url": "https://linear.app/workspace/project/LINPROJ-123",
      "cycle_id": "CYCLE-456",
      "created_issue_ids": [
        {
          "id": "LIN-101",
          "title": "Issue title",
          "url": "https://linear.app/workspace/issue/LIN-101"
        },
        {
          "id": "LIN-102",
          "title": "Issue title",
          "url": "https://linear.app/workspace/issue/LIN-102"
        },
        {
          "id": "LIN-103",
          "title": "Issue title",
          "url": "https://linear.app/workspace/issue/LIN-103"
        }
      ],
      "skipped_issue_ids": [
        {
          "id": "ISS-999",
          "reason": "duplicate_found",
          "existing_issue_id": "LIN-050",
          "existing_issue_url": "https://linear.app/workspace/issue/LIN-050"
        }
      ],
      "linked_edges": [
        {
          "from": "LIN-101",
          "to": ["LIN-102", "LIN-103"]
        }
      ],
      "cycle_warnings": [],
      "duplicate_detection_summary": {
        "total_searched": 12,
        "duplicates_found": 1,
        "duplicates_skipped": 1
      }
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

## Usage Examples

```bash
# Start planning process
/plan-linear --task "Implement OAuth2 integration"

# Process stops at objective checkpoint for review
# User provides feedback, then types "proceed" to continue

# Process stops at decision-making checkpoints for review
# User provides feedback, then types "proceed" to continue

# Process stops before Linear mutation for final confirmation
# User decides to proceed (types "proceed") or exit (workspace preserved)
```

---
