# Purpose

Generate a comprehensive project primer covering purpose, architecture, tech stack, commands, and testing practices backed by deterministic artifacts.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @TARGET_PATH = --target-path — path to analyze; defaults to the project
- @OUT = --out — write the final Markdown to this path (also print to stdout)

### Derived (internal)

- @PROJECT_ROOT = <derived> — absolute path to repository root
- @TARGET_ABS = <derived> — resolved absolute path for analysis
- @ARTIFACT_ROOT = <derived> — timestamped artifact directory for analyzers + evidence

## Instructions

- Establish @ARTIFACT_ROOT before collecting evidence; every command output cited in the report must live under that directory.
- Run Enaible analyzers (architecture, quality, security) to support conclusions and cite their JSON artifacts directly.
- After analyzers succeed, read supporting docs (README, AGENTS, CLAUDE) to add narrative context tied to the artifact evidence.
- Redirect git status/history output to files under @ARTIFACT_ROOT so future sessions can audit the same facts.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. **Establish paths + artifact root**
   - Resolve directories and create the artifact path:

     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     TARGET_PATH="@TARGET_PATH"
     if [ -z "$TARGET_PATH" ] || [ "$TARGET_PATH" = "." ]; then
       TARGET_PATH="$PROJECT_ROOT"
     elif [ "${TARGET_PATH#/}" = "$TARGET_PATH" ]; then
       TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
     fi
     TARGET_ABS="$(cd "$TARGET_PATH" && pwd)"
     ARTIFACT_ROOT="$PROJECT_ROOT/.enaible/artifacts/get-codebase-primer/$(date -u +%Y%m%dT%H%M%SZ)"
     mkdir -p "$ARTIFACT_ROOT"
     export PROJECT_ROOT TARGET_ABS ARTIFACT_ROOT
     ```

   - Record STOP confirmations and manual observations inside `"$ARTIFACT_ROOT/notes.md"` for traceability.

2. **Run mandatory analyzers**
   - Execute Enaible analyzers, writing results beneath @ARTIFACT_ROOT:

     ```bash
     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run architecture:patterns \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/architecture-patterns.json"

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/quality-lizard.json" \
       --summary-out "$ARTIFACT_ROOT/quality-lizard-summary.json"

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run security:semgrep \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/security-semgrep.json"
     ```

   - Log analyzer selection + exclusions in `"$ARTIFACT_ROOT/analyzers.log"` so downstream reviewers understand coverage.

3. **Collect repository facts**
   - Inventory structure, frameworks, and tooling using deterministic commands and store the outputs:

     ```bash
     ls "$TARGET_ABS" > "$ARTIFACT_ROOT/dir-listing.txt"
     rg --files "$TARGET_ABS" > "$ARTIFACT_ROOT/file-inventory.txt"
     ```

   - Extract snippets from README/AGENTS/CLAUDE as needed, referencing the lines inside `notes.md`.
   - Map architecture, backend/frontend practices, data, observability, and quality gates using analyzer artifacts plus captured listings.

4. **Git status & history review**
   - Capture source control signals for at least the last 30 days (adjust window when @TARGET_PATH differs):

     ```bash
     (cd "$TARGET_ABS" && git status) > "$ARTIFACT_ROOT/git-status.txt"
     (cd "$TARGET_ABS" && git log --since="30 days ago" --stat --date=iso) > "$ARTIFACT_ROOT/git-log.txt"
     (cd "$TARGET_ABS" && git shortlog -sn --since="30 days ago") > "$ARTIFACT_ROOT/git-shortlog.txt"
     ```

   - Summarize themes, contributors, and churn hotspots with references to these files.

5. **Generate the primer**
   - Compile findings into the standardized markdown format below.
   - Cite artifacts for every major claim (e.g., “architecture boundary” → `architecture-patterns.json`, “hot functions” → `quality-lizard-summary.json`).
   - Write the final report to @OUT and save a copy as `"$ARTIFACT_ROOT/report.md"` to keep evidence + narrative together.

## Output

````markdown
# Project: <Name>

Artifacts: `<@ARTIFACT_ROOT>`

---

## Executive Summary

[Concise description of what this project is and does with citations, e.g., README.md §Overview, architecture-patterns.json]

- **Current Readiness**: <headline insight with artifact reference>
- **Immediate Gaps**: <headline risk or opportunity with artifact reference>

## Features

- [Key feature 1 (cite README/notes)]
- [Key feature 2]
- [Additional features...]

## Tech Stack

- **Languages**: [...]
- **Frameworks**: [...]
- **Build Tools**: [...]
- **Package Managers**: [...]
- **Testing**: [...]

## Structure

```markdown
project-root/
├── src/ # [Description]
├── tests/ # [Description]
├── docs/ # [Description]
└── ... # [Other key directories]
```

## Architecture

[Description with references to `architecture-patterns.json` and supporting evidence]

### Key Components:

- **[Component]**: [Role and responsibility + artifact reference]
- **[Component]**: [...]

## Backend Patterns and Practices to Follow

[Grounded summary referencing analyzer outputs and repo docs]

## Frontend Patterns and Practices to Follow

[Grounded summary referencing analyzer outputs and repo docs]

## Build & Quality Gate Commands

| Purpose | Command | Notes / Evidence |
| ------- | ------- | ---------------- |
| Build   | `<cmd>` | README / scripts |
| Test    | `<cmd>` | README / scripts |
| Lint    | `<cmd>` | README / scripts |
| Dev     | `<cmd>` | README / scripts |

## Testing

**Framework**: [Testing framework used]

**Running Tests**:

```bash
[command to run tests]
```

**Creating New Tests**:
[Instructions on where tests go and basic structure]

## Git History Insights (last 30 days unless overridden)

- Theme or initiative • reference `git-log.txt`
- Notable fix/feature • reference `git-log.txt`
- Contributor focus • reference `git-shortlog.txt`

---
````
