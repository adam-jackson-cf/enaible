---
name: codify-pr-reviews
description: Analyze GitHub pull request review comments to identify recurring review patterns and convert them into code review instruction rules. USE WHEN you need to reduce repetitive PR feedback or transform historical comments into enforceable rules.
compatibility: Requires gh CLI authentication, Python 3.12+ via `PYTHON_CMD`, and a git repository with PR history.
allowed-tools: @BASH @READ @WRITE
---

# Codify PR Reviews

Turn historical PR review comments into actionable instruction rules so repeat feedback becomes automated guidance.

- You want to codify recurring PR feedback into enforceable instruction rules.
- You need a deterministic workflow with human approval gates before rules change.
- You must keep artifacts for auditability across analyzers and adapters.

## Need to...? Read This

| Goal                              | Reference                                                                          |
| --------------------------------- | ---------------------------------------------------------------------------------- |
| Detect stack + red flags          | [references/stack-analysis-workflow.md](references/stack-analysis-workflow.md)     |
| Fetch PR review comments          | [references/fetching-workflow.md](references/fetching-workflow.md)                 |
| Deduplicate + group comments      | [references/preprocessing-workflow.md](references/preprocessing-workflow.md)       |
| Triage patterns vs existing rules | [references/pattern-analysis-workflow.md](references/pattern-analysis-workflow.md) |
| Generate rule drafts              | [references/rule-generation-workflow.md](references/rule-generation-workflow.md)   |
| Apply approved rules              | [references/apply-rules-workflow.md](references/apply-rules-workflow.md)           |
| Resolve system targets            | [references/system-targeting.md](references/system-targeting.md)                   |
| Rule template                     | [references/rule-template.md](references/rule-template.md)                         |
| Troubleshoot issues               | [references/troubleshooting.md](references/troubleshooting.md)                     |

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

### Step 4: Pattern analysis

**Purpose**: Identify recurring patterns and triage against existing rules for the target system.

- Compare grouped comments with existing instruction files.
- Record findings in `@ARTIFACT_ROOT/patterns.json`.
- The in-depth checklist lives in [references/pattern-analysis-workflow.md](references/pattern-analysis-workflow.md).

### Step 5: Pattern review (interactive)

**Purpose**: Review identified patterns and decide on actions (create / strengthen / skip).

- Pause for user input before committing to rule changes; checkpoints are scripted in the pattern analysis reference file.
- Document approvals directly in the artifact directory.

### Step 6: Generate rule drafts

**Purpose**: Create new rules or enhance existing ones with concrete examples.

- Use the templates + prompts in [references/rule-generation-workflow.md](references/rule-generation-workflow.md) and [references/rule-template.md](references/rule-template.md).
- Save drafts under `@ARTIFACT_ROOT/drafts/`.

### Step 7: Rule wording review (interactive)

**Purpose**: Validate and approve generated rule wording before application.

- Collect user confirmation per draft; the detailed `@ASK_USER_CONFIRMATION` prompts live in [references/rule-generation-workflow.md](references/rule-generation-workflow.md).

### Step 8: Apply rules

**Purpose**: Update instruction files for the target system and capture diffs.

- Follow the apply workflow to edit files safely, record `@ARTIFACT_ROOT/apply-summary.json` (or `.md`), and attach diffs.
- All approval gates for file edits are described in [references/apply-rules-workflow.md](references/apply-rules-workflow.md).
