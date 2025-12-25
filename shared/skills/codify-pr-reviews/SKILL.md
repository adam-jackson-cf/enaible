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

## Resources

| Goal                              | Resource                                                                             |
| --------------------------------- | ------------------------------------------------------------------------------------ |
| Detect stack + red flags          | [resources/stack-analysis-workflow.md](resources/stack-analysis-workflow.md)         |
| Fetch PR review comments          | [resources/fetching-workflow.md](resources/fetching-workflow.md)                     |
| Deduplicate + group comments      | [resources/preprocessing-workflow.md](resources/preprocessing-workflow.md)           |
| Triage patterns vs existing rules | [resources/pattern-analysis-workflow.md](resources/pattern-analysis-workflow.md)     |
| Run interactive approvals         | [resources/interactive-review-workflow.md](resources/interactive-review-workflow.md) |
| Generate rule drafts              | [resources/rule-generation-workflow.md](resources/rule-generation-workflow.md)       |
| Troubleshoot issues               | [resources/troubleshooting.md](resources/troubleshooting.md)                         |

## Mandatory checkpoints

This skill requires explicit user confirmation at multiple stages. Use the interactive review workflow to enforce:

1. Preflight approval before fetching full PR history.
2. Pattern-by-pattern approval decisions.
3. Rule-by-rule wording approval.
4. Final confirmation before applying edits to instruction files.

Do not batch confirmations. Always ask one item at a time.
