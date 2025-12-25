---
name: codify-pr-reviews
description: Analyze GitHub pull request review comments to identify recurring review patterns and convert them into code review instruction rules; use when you want to reduce repetitive PR feedback.
compatibility: Requires gh CLI authentication and a git repository with PR history.
allowed-tools: Bash Read Write
---

# Codify PR Reviews

Turn historical PR review comments into actionable instruction rules so repeat feedback becomes automated guidance.

## When to use

- You want to codify recurring review feedback into instruction rules.
- You want a repeatable workflow with human approval checkpoints before rules change.

## Prerequisites

- `gh` CLI installed and authenticated.
- Run inside the target git repository (or provide an explicit repo).
- Instruction files exist or can be created (Copilot, Codex, etc.).
- User must specify a single target system for rule format: `claude-code`, `codex`, `copilot`, `cursor`, or `gemini`.
- Default settings live in `config/defaults.json`.
- Set `PYTHON_CMD` to the system Python command (must be 3.12+).
- Set a timestamped artifacts root under `.enaible/artifacts/codify-pr-reviews/$(date -u +%Y%m%dT%H%M%SZ)` before running any stage.
- Export `RUN_ID="codify-pr-reviews-$(date -u +%Y%m%dT%H%M%SZ)"` for traceability across scripts.

### Derived directories

- `@ARTIFACT_ROOT = .enaible/artifacts/codify-pr-reviews/<timestamp>` — persistent evidence (stack analysis, fetched comments, grouped comments, patterns, approved rules).

## Resources

| Goal                              | Resource                                                                         |
| --------------------------------- | -------------------------------------------------------------------------------- |
| Detect stack + red flags          | [resources/stack-analysis-workflow.md](resources/stack-analysis-workflow.md)     |
| Fetch PR review comments          | [resources/fetching-workflow.md](resources/fetching-workflow.md)                 |
| Deduplicate + group comments      | [resources/preprocessing-workflow.md](resources/preprocessing-workflow.md)       |
| Triage patterns vs existing rules | [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md) |
| Generate rule drafts              | [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)   |
| Apply approved rules              | [resources/apply-rules-workflow.md](resources/apply-rules-workflow.md)           |
| Resolve system targets            | [resources/system-targeting.md](resources/system-targeting.md)                   |
| Rule template                     | [resources/templates/rule-template.md](resources/templates/rule-template.md)     |
| Troubleshoot issues               | [resources/troubleshooting.md](resources/troubleshooting.md)                     |

## Orchestration Overview

### Stage 0: Establish run directories

**Purpose**: Guarantee deterministic storage just like other Enaible analyzers.

- Capture the UTC timestamp, create `.enaible/artifacts/codify-pr-reviews/<timestamp>`, and export `@ARTIFACT_ROOT` plus `RUN_ID`.
- Store all evidence (JSON, markdown, logs) under `@ARTIFACT_ROOT` for auditability.

### Stage 1: Stack Analysis

**Purpose**: Detect tech stack and generate security red flags.
**When**: First run or with `@FORCE_REFRESH`.
**Details**: [resources/stack-analysis-workflow.md](resources/stack-analysis-workflow.md)

- Artifacts: `@ARTIFACT_ROOT/stack-analysis.json`.

### Stage 2: Fetch PR Comments

**Purpose**: Retrieve PR comments via the deterministic fetch script.

**Details**: [resources/fetching-workflow.md](resources/fetching-workflow.md)

- Follow the resource workflow: run preflight, pause for **MANDATORY CHECKPOINT 1**, then execute the full fetch.
- Artifacts: store full fetch JSON at `@ARTIFACT_ROOT/comments.json`; capture any preflight output at `@ARTIFACT_ROOT/fetch-preflight.log`.

### Stage 3: Preprocess & Deduplicate

**Purpose**: Group similar comments and reduce noise using deterministic preprocessing.
**Details**: [resources/preprocessing-workflow.md](resources/preprocessing-workflow.md)

- Artifacts: `@ARTIFACT_ROOT/preprocessed.json`.

### Stage 4: Pattern Analysis

**Purpose**: Identify recurring patterns and triage against existing rules for the target system.
**Details**: [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)

- Artifacts: `@ARTIFACT_ROOT/patterns.json`.

### Stage 5: Interactive Pattern Review

**Purpose**: Review identified patterns and decide on actions (create/strengthen/skip).
**MANDATORY CHECKPOINT 2**: For each pattern, pause and @ASK_USER_CONFIRMATION.

**Details**: [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)

### Stage 6: Generate Rules

**Purpose**: Create new rules or enhance existing ones with concrete examples.
**Details**: [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)

- Artifacts: draft markdown lives under `@ARTIFACT_ROOT/drafts/`.

### Stage 7: Interactive Rule Wording Review

**Purpose**: Review and approve generated rule wording before application.
**MANDATORY CHECKPOINT 3**: For each rule, pause and @ASK_USER_CONFIRMATION.

**Details**: [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)

### Stage 8: Apply Rules

**Purpose**: Update instruction files for the target system.
**MANDATORY CHECKPOINT 4**: Pause and @ASK_USER_CONFIRMATION before modifying files.
**Details**: [resources/apply-rules-workflow.md](resources/apply-rules-workflow.md)

- Artifacts: record the apply summary at `@ARTIFACT_ROOT/apply-summary.json` (or `.md`) plus any diff outputs captured during the edit.
