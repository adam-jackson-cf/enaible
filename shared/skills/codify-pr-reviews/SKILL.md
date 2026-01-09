---
name: codify-pr-reviews
description: Analyze GitHub pull request review comments to identify recurring review patterns and convert them into code review instruction rules. USE WHEN you need to reduce repetitive PR feedback or transform historical comments into enforceable rules.
compatibility: Requires gh CLI authentication, Python 3.12+ via `PYTHON_CMD`, and a git repository with PR history.
allowed-tools: @BASH @READ @WRITE
---

# Codify PR Reviews

Turn historical PR review comments into actionable instruction rules so repeat feedback becomes automated guidance.

- You want to codify recurring PR feedback into enforceable checks, preferring tooling before system docs.
- You need a deterministic workflow with human approval gates before rules change.
- You must keep artifacts for auditability across analyzers and adapters.

## Need to...? Read This

| Goal                            | Reference                                                                                |
| ------------------------------- | ---------------------------------------------------------------------------------------- |
| Detect stack + red flags        | [references/stack-analysis-workflow.md](references/stack-analysis-workflow.md)           |
| Fetch PR review comments        | [references/fetching-workflow.md](references/fetching-workflow.md)                       |
| Deduplicate + group comments    | [references/preprocessing-workflow.md](references/preprocessing-workflow.md)             |
| Extract normalized patterns     | [references/extract-patterns-workflow.md](references/extract-patterns-workflow.md)       |
| Inventory deterministic tooling | [references/tooling-inventory-workflow.md](references/tooling-inventory-workflow.md)     |
| Inventory system doc rules      | [references/doc-rules-inventory-workflow.md](references/doc-rules-inventory-workflow.md) |
| Compare coverage (tools + docs) | [references/coverage-compare-workflow.md](references/coverage-compare-workflow.md)       |
| Enforcement review + approvals  | [references/enforcement-review-workflow.md](references/enforcement-review-workflow.md)   |
| Generate rule drafts            | [references/rule-generation-workflow.md](references/rule-generation-workflow.md)         |
| Apply approved rules            | [references/apply-rules-workflow.md](references/apply-rules-workflow.md)                 |
| Resolve system targets          | [references/system-targeting.md](references/system-targeting.md)                         |
| Rule template                   | [references/rule-template.md](references/rule-template.md)                               |
| Troubleshoot issues             | [references/troubleshooting.md](references/troubleshooting.md)                           |

## Workflow

Detailed instructions, artifacts, and checkpoint prompts live in the `references/*.md` files. This section summarizes the high-level flow.

### Step 0: Preflight + establish run directories

**Purpose**: Confirm environment readiness and guarantee deterministic storage before any analyzers run.

- Verify `gh` CLI is installed/authenticated, you are inside the target git repo (or pass `--repo`).
- Ensure `PYTHON_CMD` points to Python 3.12+, export any tokens required by helper scripts, and confirm write access to `.enaible/artifacts/`.
- Capture the UTC timestamp, create `.enaible/artifacts/codify-pr-reviews/<timestamp>`, set `@ARTIFACT_ROOT`, and export `RUN_ID="codify-pr-reviews-$(date -u +%Y%m%dT%H%M%SZ)"`.
- Store all evidence (JSON, markdown, logs) under `@ARTIFACT_ROOT` for auditability.

### Step 1: Stack analysis

**Purpose**: Detect the tech stack and generate security red flags.

- Run the stack analysis helper; refresh when `@FORCE_REFRESH` is set.
- Output `@ARTIFACT_ROOT/stack-analysis.json`.
- Workflow + success criteria: [references/stack-analysis-workflow.md](references/stack-analysis-workflow.md).

### Step 2: Fetch PR comments

**Purpose**: Retrieve PR review comments via the deterministic fetch script.

- Follow the fetch workflow preflight, then perform the full download.
- Store JSON at `@ARTIFACT_ROOT/comments.json` and preflight logs at `@ARTIFACT_ROOT/fetch-preflight.log`.
- User confirmation gates (e.g., target repo validation) are defined in [references/fetching-workflow.md](references/fetching-workflow.md) using `@ASK_USER_CONFIRMATION` markers.

### Step 3: Preprocess & deduplicate

**Purpose**: Group similar comments and reduce noise using deterministic preprocessing.

- Execute the preprocessing script to produce `@ARTIFACT_ROOT/preprocessed.json`.
- Follow [references/preprocessing-workflow.md](references/preprocessing-workflow.md) for grouping heuristics and thresholds.

### Step 4: Extract normalized patterns

**Purpose**: Convert grouped comments into normalized patterns without enforcement decisions.

- Run the pattern extraction helper to produce `@ARTIFACT_ROOT/patterns.json`.
- Workflow: [references/extract-patterns-workflow.md](references/extract-patterns-workflow.md).

### Step 5: Inventory deterministic tooling

**Purpose**: Capture current lint/analyzer configurations and rule identifiers.

- Run the tooling inventory helper to produce `@ARTIFACT_ROOT/tooling-inventory.json`.
- Workflow: [references/tooling-inventory-workflow.md](references/tooling-inventory-workflow.md).

### Step 6: Inventory system doc rules

**Purpose**: Snapshot existing system doc rules for coverage comparison.

- Resolve `@TARGET_SYSTEM` and `@INSTRUCTION_FILES` using [references/system-targeting.md](references/system-targeting.md).
- Run the doc rules inventory helper to produce `@ARTIFACT_ROOT/doc-rules.json`.
- Workflow: [references/doc-rules-inventory-workflow.md](references/doc-rules-inventory-workflow.md).

### Step 7: Compare coverage (tools + docs)

**Purpose**: Determine whether patterns are already covered by tooling or docs, and suggest enforcement paths.

- Run the coverage comparison helper to produce `@ARTIFACT_ROOT/coverage.json`.
- Workflow: [references/coverage-compare-workflow.md](references/coverage-compare-workflow.md).

### Step 8: Enforcement review (interactive)

**Purpose**: Approve enforcement decisions for tooling, docs, or both.

- Review `coverage.json` with the user and capture decisions in `@ARTIFACT_ROOT/approved-enforcement.json`.
- Workflow: [references/enforcement-review-workflow.md](references/enforcement-review-workflow.md).

### Step 9: Prepare enforcement outputs

**Purpose**: Generate doc-only pattern list and tooling change plan from approvals.

- Run the enforcement output helper to produce `@ARTIFACT_ROOT/doc-patterns.json`, `@ARTIFACT_ROOT/tooling-changes.md`, and `@ARTIFACT_ROOT/tooling-changes.json`.
- Workflow: [references/enforcement-review-workflow.md](references/enforcement-review-workflow.md).

### Step 10: Generate rule drafts

**Purpose**: Create new rules or enhance existing ones with concrete examples.

- Use `@ARTIFACT_ROOT/doc-patterns.json` from enforcement outputs with the templates in [references/rule-generation-workflow.md](references/rule-generation-workflow.md) and [references/rule-template.md](references/rule-template.md).
- Save drafts under `@ARTIFACT_ROOT/drafts/`.

### Step 11: Rule wording review (interactive)

**Purpose**: Validate and approve generated rule wording before application.

- Collect user confirmation per draft; the detailed `@ASK_USER_CONFIRMATION` prompts live in [references/rule-generation-workflow.md](references/rule-generation-workflow.md).

### Step 12: Apply enforcement changes

**Purpose**: Update instruction files and tooling configs, then capture diffs.

- Apply doc rule updates following [references/apply-rules-workflow.md](references/apply-rules-workflow.md).
- Apply tooling changes listed in `tooling-changes.md` (and mirrored in `tooling-changes.json`) and capture diffs alongside doc updates.
