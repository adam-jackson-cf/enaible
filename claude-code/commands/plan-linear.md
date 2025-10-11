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
4. Establish Objective Definition - invoke `@agent-linear-objective-definition` passing raw artifact from `--task`.
5. Cycle Initialization:
   - Establish deterministic name using kebab-case slug with no spaces:
   - `cycle_slug = kebab_case(lowercase(objective_frame.task_objective))`
   - Set `CYCLE_DIR` to cycle_slug deterministic value and create the folder (if doesnt exist)
   - Move `linear-objective-definition-output.json` to `CYCLE_DIR`.
6. Clarification Loop:
   - Summarize task objective, purpose, affected users, requirements, and constraints discovered.
   - Present `open_questions` gathered by the objective-definition agent back to the user.
   - Capture user-provided clarifications and append them to `cycle_plan_report.json` under `objective.clarifications`.

**⚠️ PAUSE FOR REQUIRED USER CONFIRMATION**: Ask user "Objective frame prepared. Provide clarifications or type proceed to continue." WAIT for the user to either answer the questions or explicitly type `proceed`. Do not continue until confirmation is received. If user supplies new information, update the clarification record and restate the summary before requesting confirmation again.

7. Autonomous Planning Loop (delegated to subagents), evolve `cycle_plan_report.json` state until plan readiness criteria satisfied:

   - Subagents are invoked sequentially, never in parallel.
   - Each subagent must emit traceability artifacts into `CYCLE_DIR`:

     1. `<agent-name>-input.md` — exact task payload the subagent received.
     2. `<agent-name>-summary.md` — concise human-readable summary of findings.
     3. `<agent-name>-output.json` — machine-readable full output.

   - Filenames strictly use the full agent name (e.g., `-linear-issue-decomposer-output.json`). No abbreviations or spaces.

     - `@agent-linear-issue-decomposer` → atomic issue graph with ids/deps derived from confirmed requirements.
       <estimate-style if --estimate-style = tshirt>
       - `@agent-linear-estimation-engine` → size, rcs, oversize flags
         </estimate-style>
     - `@agent-linear-acceptance-criteria-writer` → acceptance criteria only (no DoD or guidance sections)
     - `@agent-linear-hashing` (compute) → hashes + duplication detection

   - Update the `cycle_plan_report.json`, as each subagent completes, with the latest findings.

8. Readiness Check (`@agent-linear-readiness`):
   - Determine readiness and produce readiness object.
   - If readiness.ready=false → exit 2 unless user chooses remediation.

**⚠️ PAUSE FOR REQUIRED USER CONFIRMATION**: Ask user "Plan formed and readiness check successful, proceed with transfer to linear? (y/n)" and WAIT for response before continuing to step 9. If user responds "n" or "no", stop workflow execution and exit.

9. Optional Mutation:
   - Invoke `@agent-linear-issue-writer` (duplicate detection, project/cycle logic, then issue batch)
   - Invoke `@agent-linear-dependency-linker`
   - Integrity of previously computed hashes MUST NOT change post-mutation.
   - Append mutation results into `cycle_plan_report.json` under `mutation`.

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

## Failure & Exit Codes & Output format

| Code | Meaning                                               |
| ---- | ----------------------------------------------------- |
| 0    | Success (dry-run or mutation complete)                |
| 1    | Argument or config validation failure                 |
| 2    | Plan readiness failures or blocking validation errors |
| 3    | Linear mutation failures (writer/linker errors)       |
| 4    | Structural integrity or contract violations           |

All errors must output a machine-parsable JSON envelope with `exit_code` and `error.code` fields.

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

| Subagent                          | Responsibility                                    | Key Outputs                                                                 |
| --------------------------------- | ------------------------------------------------- | --------------------------------------------------------------------------- |
| linear-objective-definition       | Normalize objective, purpose, users, requirements | task_objective, purpose, affected_users[], requirements[], open_questions[] |
| linear-issue-decomposer           | Atomic issue graph                                | issues[] (ids, deps, category)                                              |
| linear-estimation-engine          | Complexity & sizing                               | size, rcs, oversize_flag                                                    |
| linear-acceptance-criteria-writer | Acceptance criteria enrichment                    | acceptance_criteria[]                                                       |
| linear-hashing                    | Deterministic hashing + duplication + diff        | plan_hash, artifact hashes, per-issue hashes, duplicates, diff              |
| linear-readiness                  | Validation + labeling + readiness gating          | findings[], label_assignments[], dependency_suggestions[], readiness{}      |
| linear-issue-search               | Duplicate issue detection (existing projects)     | matching_issues[], confidence_scores[], duplicate_warnings[]                |
| linear-issue-writer               | Project/cycle creation + issue batch              | project_id, cycle_id, created_issue_ids[], project_url, issue_urls[]        |
| linear-dependency-linker          | Apply dependency edges                            | applied_edges[]                                                             |

## Cycle Plan Report (Canonical Schema)

```json
{
  "CycleName": {
    "version": 3,
    "objective": {
      "task_objective": "Deliver authentication hardening for user-facing API",
      "purpose": "Reduce takeover risk for privileged accounts while keeping login latency flat.",
      "affected_users": ["admin-operators", "support-analysts"],
      "requirements": [
        "Require MFA for admin roles",
        "Provide backup codes during enrollment",
        "Log MFA events for audit export"
      ],
      "constraints": ["no-db-schema-changes", "release-window:2025-Q4"],
      "assumptions": ["backwards-compatible client SDKs"],
      "open_questions": [],
      "clarifications": [
        {
          "question": "Do support analysts require MFA on first login?",
          "answer": "Yes, enforce MFA immediately after first login."
        }
      ]
    },
    "issues": {
      "totals": {
        "total": 12,
        "feature": 8,
        "foundation": 2,
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
      "items": [
        {
          "id": "ISS-001",
          "title": "Require MFA for admin login",
          "category": "feature",
          "deps": ["ISS-004"],
          "size": "M",
          "rcs": 5,
          "oversize_flag": false,
          "requirements": [
            "Prompt admin users for second factor on login",
            "Provide recovery backup codes"
          ],
          "acceptance_criteria": [
            "Admin login enforces second factor before granting session",
            "Backup codes can be generated once per user and invalidate older codes"
          ]
        }
      ],
      "dependencies": {
        "edges": 5,
        "roots": ["ISS-001"],
        "leaves": ["ISS-020"]
      }
    },
    "hashes": {
      "artifact_raw": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "artifact_normalized": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "plan": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "config_fingerprint": "sha256:dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
    },
    "readiness": {
      "findings": [],
      "label_assignments": [
        {
          "issue_id": "ISS-001",
          "labels": ["type:feature", "planning:ai-linear"]
        }
      ],
      "dependency_suggestions": [],
      "ready": true,
      "requires_split": false,
      "pending_steps": [],
      "advisories": [],
      "plan_hash": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
      "timestamp": "2025-09-30T12:34:56Z"
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
