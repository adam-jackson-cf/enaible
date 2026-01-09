# Purpose

Explore the codebase and produce a task primer tailored to @USER_PROMPT, covering context, risks, and next actions with deterministic evidence.

## Variables

### Required

- @USER_PROMPT = $1 — task brief to guide the analysis

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @TARGET_PATH = --target — root to analyze (default .)
- @OUT = --out — write the final Markdown to this path (also print to stdout)
- @DAYS = --days — history window for insights (default 20)
- @EXCLUDE_GLOBS = --exclude [repeatable] — CSV or repeated flags (e.g., node_modules,dist)

### Derived (internal)

- @PROJECT_ROOT = <derived> — absolute path to repository root
- @TARGET_ABS = <derived> — resolved absolute path for analysis
- @ARTIFACT_ROOT = <derived> — timestamped artifact directory for task primer evidence

## Instructions

- Establish @ARTIFACT_ROOT before running commands; store every referenced output under this directory for auditing.
- Operate read-only except for writing artifacts/report; capture deterministic command outputs (`ls`, `rg`, `git`, analyzers) into files within @ARTIFACT_ROOT.
- Run Enaible analyzers relevant to the scoped task to ground architecture/code-quality/security claims; cite the resulting JSON files.
- Respect @EXCLUDE_GLOBS and document applied exclusions in the artifact set.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.

## Workflow

1. **Scope, resolve paths, create artifact root**
   - Resolve directories:

     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     TARGET_PATH="@TARGET_PATH"
     if [ -z "$TARGET_PATH" ] || [ "$TARGET_PATH" = "." ]; then
       TARGET_PATH="$PROJECT_ROOT"
     elif [ "${TARGET_PATH#/}" = "$TARGET_PATH" ]; then
       TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
     fi
     TARGET_ABS="$(cd "$TARGET_PATH" && pwd)"
     ARTIFACT_ROOT="$PROJECT_ROOT/.enaible/artifacts/get-task-primer/$(date -u +%Y%m%dT%H%M%SZ)"
     mkdir -p "$ARTIFACT_ROOT"
     export PROJECT_ROOT TARGET_ABS ARTIFACT_ROOT
     ```

   - Save the task brief, assumptions, and STOP responses into `"$ARTIFACT_ROOT/notes.md"`.
   - Derive exclusion arguments (merge `.gitignore`, `.git/info/exclude`, and @EXCLUDE_GLOBS) and persist them to `"$ARTIFACT_ROOT/excludes.txt"`.

2. **Run targeted analyzers**
   - Execute Enaible analyzers necessary for the task scope (adjust severity/exclusions when needed):

     ```bash
     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run architecture:coupling \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/architecture-coupling.json" \
       @EXCLUDE_GLOBS

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/quality-lizard.json" \
       --summary-out "$ARTIFACT_ROOT/quality-lizard-summary.json" \
       @EXCLUDE_GLOBS

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run security:semgrep \
       --target "$TARGET_ABS" --min-severity high \
       --out "$ARTIFACT_ROOT/security-semgrep.json" \
       @EXCLUDE_GLOBS
     ```

   - Log analyzer rationale and any skips in `notes.md`.

3. **Repository reconnaissance**
   - Capture deterministic evidence for architecture, components, configs, and entry points:

     ```bash
     ls "$TARGET_ABS" > "$ARTIFACT_ROOT/dir-listing.txt"
     rg --files "$TARGET_ABS" > "$ARTIFACT_ROOT/file-inventory.txt"
     ```

   - Use `rg`, `sed`, or helper scripts to extract signals (e.g., service manifests, routes). Summaries belong in `notes.md` with file references.

4. **Git history & pattern recognition**
   - Gather git status/history for the specified window:

     ```bash
     (cd "$TARGET_ABS" && git status) > "$ARTIFACT_ROOT/git-status.txt"
     (cd "$TARGET_ABS" && git log --since="${DAYS:-20} days ago" --stat --date=iso) > "$ARTIFACT_ROOT/git-log.txt"
     (cd "$TARGET_ABS" && git shortlog -sn --since="${DAYS:-20} days ago") > "$ARTIFACT_ROOT/git-shortlog.txt"
     ```

   - Note recurring themes, regressions, and contributor hotspots referencing these files.

5. **Synthesis**
   - Populate the output template below, citing artifacts for every major claim (architecture → `architecture-coupling.json`, complexity hotspots → `quality-lizard-summary.json`, recent failures → `git-log.txt`).
   - Write the final Markdown to @OUT if provided and store the same content at `"$ARTIFACT_ROOT/report.md"`.

## Output

````markdown
# Project: <Name>

Artifacts: `<@ARTIFACT_ROOT>`

---

## Executive Summary

[Concise description of what this project is and does, citing analyzer artifacts and repo notes]

- **Current Readiness**: <headline insight + artifact reference>
- **Immediate Gaps**: <headline risk or opportunity + artifact reference>

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

**Key Files**

- `[file]` – [Purpose, cite evidence]
- `[file]` – [...]

**Entry Points**

- `[file]` – [Description/evidence]

## Architecture

[Description referencing `architecture-coupling.json`, repo configs, etc.]

### Key Components

- **[Component]** – [Role/responsibility + evidence]
- **[Component]** – [...]

## Backend Patterns and Practices

- <observation + artifact reference>
- <observation>

## Frontend Patterns and Practices

- <observation + artifact reference>

## Data & State

- <observation + evidence>

## Performance & Security

- <observation referencing analyzers/security artifacts>

## Observability

| Aspect          | Current State | Note (artifact/source) |
| --------------- | ------------- | ---------------------- |
| Logging         | <…>           | <…>                    |
| Metrics         | <…>           | <…>                    |
| Analytics/Flags | <…>           | <…>                    |

## Build & Quality Gates

| Purpose     | Command | Notes / Evidence    |
| ----------- | ------- | ------------------- |
| Lint        | `<cmd>` | README/scripts refs |
| Type        | `<cmd>` | README/scripts refs |
| Test        | `<cmd>` | README/scripts refs |
| Duplication | `<cmd>` | analyzer references |
| Complexity  | `<cmd>` | analyzer references |

## Testing Practices

| Test type          | File path / location | Command     |
| ------------------ | -------------------- | ----------- |
| Unit tests         | `<path>`             | `<command>` |
| Integration tests  | `<path>`             | `<command>` |
| System / E2E tests | `<path>`             | `<command>` |
| Coverage           | `<path>`             | `<command>` |

## Git History Insights (<@DAYS> days)

- Theme or initiative • reference `git-log.txt`
- Notable fix/feature • reference `git-log.txt`
- Contributor focus • reference `git-shortlog.txt`

---

## Task Impact Analysis

| File/Area   | Rationale (cite artifacts)         |
| ----------- | ---------------------------------- |
| `path:line` | Impact reason referencing evidence |

---

## Risks & Recommendations

| Risk   | Mitigation (artifact support) |
| ------ | ----------------------------- |
| <risk> | <recommended action>          |

---

## Open Questions

- <question1 + evidence>
- <question2>
````
