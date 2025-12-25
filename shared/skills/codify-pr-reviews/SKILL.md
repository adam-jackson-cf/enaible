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

## Resources

| Goal                              | Resource                                                                                     |
| --------------------------------- | -------------------------------------------------------------------------------------------- |
| Detect stack + red flags          | [resources/stack-analysis-workflow.md](resources/stack-analysis-workflow.md)                 |
| Fetch PR review comments          | [resources/fetching-workflow.md](resources/fetching-workflow.md)                             |
| Deduplicate + group comments      | [resources/preprocessing-workflow.md](resources/preprocessing-workflow.md)                   |
| Triage patterns vs existing rules | [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)             |
| Generate rule drafts              | [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)               |
| Apply approved rules              | [resources/apply-rules-workflow.md](resources/apply-rules-workflow.md)                       |
| Resolve system targets            | [resources/system-targeting.md](resources/system-targeting.md)                               |
| Rule template (Copilot)           | [resources/templates/copilot-rule-template.md](resources/templates/copilot-rule-template.md) |
| Rule template (Other systems)     | [resources/templates/rule-template.md](resources/templates/rule-template.md)                 |
| Troubleshoot issues               | [resources/troubleshooting.md](resources/troubleshooting.md)                                 |

## Orchestration Overview

### Stage 1: Stack Analysis

**Purpose**: Detect tech stack and generate security red flags.
**When**: First run or with `@FORCE_REFRESH`.
**Details**: [resources/stack-analysis-workflow.md](resources/stack-analysis-workflow.md)

### Stage 2: Fetch PR Comments

**Purpose**: Retrieve PR comments via the deterministic fetch script.

**Process**:

1. Run the preflight fetch to confirm auth + sampling.
2. Review preflight results with the user.
3. **MANDATORY CHECKPOINT 1**: @ASK_USER_CONFIRMATION before full fetch.
4. Run the full fetch and capture outputs.

**Details**: [resources/fetching-workflow.md](resources/fetching-workflow.md)

### Stage 3: Preprocess & Deduplicate

**Purpose**: Group similar comments and reduce noise using deterministic preprocessing.
**Details**: [resources/preprocessing-workflow.md](resources/preprocessing-workflow.md)

### Stage 4: Pattern Analysis

**Purpose**: Identify recurring patterns and triage against existing rules for the target system.
**Details**: [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)

### Stage 5: Interactive Pattern Review

**Purpose**: Review identified patterns and decide on actions (create/strengthen/skip).
**MANDATORY CHECKPOINT 2**: For each pattern, pause and @ASK_USER_CONFIRMATION.

**Details**: [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)

### Stage 6: Generate Rules

**Purpose**: Create new rules or enhance existing ones with concrete examples.
**Details**: [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)

### Stage 7: Interactive Rule Wording Review

**Purpose**: Review and approve generated rule wording before application.
**MANDATORY CHECKPOINT 3**: For each rule, pause and @ASK_USER_CONFIRMATION.

**Details**: [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)

### Stage 8: Apply Rules

**Purpose**: Update instruction files for the target system.
**MANDATORY CHECKPOINT 4**: Pause and @ASK_USER_CONFIRMATION before modifying files.

**Details**: [resources/apply-rules-workflow.md](resources/apply-rules-workflow.md)
