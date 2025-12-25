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
- User must specify a single target system for rule format: `claude-code` or `codex`.
- Default settings live in `config/defaults.json`.
- Set `PYTHON_CMD` to the user-confirmed Python command (must be 3.12+).

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
| Rule templates                    | [resources/templates](resources/templates)                                       |
| Troubleshoot issues               | [resources/troubleshooting.md](resources/troubleshooting.md)                     |

## Scripts

The following deterministic helpers live in `scripts/`:

- `scripts/stack_analysis.py`
- `scripts/fetch_comments.py`
- `scripts/preprocess_comments.py`
- `scripts/analyze_patterns.py`
- `scripts/generate_rules.py`
