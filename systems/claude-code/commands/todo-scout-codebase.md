---
argument-hint: [--user-prompt USER_PROMPT] [--out $OUT] [--exclue $EXCLUDE_GLOBS]
description: Analyse a codebase in relation to a specific user request to create a supporting context
---

# todo-scout-codebase v0.3

## Purpose

Explore the entire project and generate a comprehensive codebase analysis that supports the `$USER_PROMPT`.

## Variables

- `$USER_PROMPT` ← first positional argument (required)
- `$TARGET_PATH` ← second positional argument (default `.`)
- `$OUT` ← `--out` (required) — write the final Markdown to this path and also print the same Markdown to stdout (no preface, no fences)
- `$DAYS` ← `--days` (default `20`)
- `$EXCLUDE_GLOBS` ← `--exclude` CSV (optional; e.g., `node_modules,dist`)

## Instructions

- Operate read-only (apart from writing the report). Do not run builds or install tools.
- Use repository commands (`ls`, `rg`, `git`, `sed`, etc.) to gather facts, then summarize findings in clear prose;
- Avoid dumping raw command syntax unless you are showing an illustrative example.
- Format every section for quick scanning: short paragraphs, bullet lists, and tables. Keep guidance concise and documentation-focused.
- When secrets are encountered, note file and nature only—never print the secret.
- Default to the repository root when `$TARGET_PATH` is not supplied; respect `$EXCLUDE_GLOBS` for all searches.

## Workflow

1. **Scope & Setup**

   - Resolve `$TARGET_PATH`; record working directory.
   - Review `.gitignore` (and `.git/info/exclude` if present) to collect default ignore globs; merge these with `$EXCLUDE_GLOBS` to build `${EXCLUDE_ARG}` (`--glob '!{glob1,glob2,...}'`).

2. **Deep Analysis** (LLM + file-driven)

Analyse the the following aspects of the target codebase in relation to how they affect or add context to the $USER_PROMPT:

- Architecture & Orchestration
- Backend Patterns & Practices
- Frontend Patterns & Practices
- Data & State
- Performance & Security
- Observability
- Quality gates and Testing Practices
- Identify entry points, apps/services, CLIs, servers, and routing surfaces.
- Inspect key configurations, manifests and framework signals

3. **Git History & Pattern Recognition** (last `$DAYS` days)

   - `git status`, `git log --since`, `git shortlog`, churn analysis.
   - Summarize recent work: new features, notable fixes, issues resolved.
   - Detect recurring patterns or smells to highlight.

4. **Synthesis**
   - Compose the Markdown report exactly in the template below.
   - This document should build create context that should support the activities required by the `$USER_PROMPT`
   - Deliver concise, documentation-style guidance with structured bullets, tables, and brief paragraphs, dont duplicate information or file paths.
   - Write the final Markdown to `$OUT` and also print the same Markdown to stdout.
   - Do not emit prefaces, patch fences, tool logs, or JSON.

## Output

````markdown
# Project: <Name>

---

## Executive Summary

[Concise description of what this project is and does]

- **Current Readiness**: <headline insight>
- **Immediate Gaps**: <headline risk or opportunity>

## Features

- [Key feature 1]
- [Key feature 2]
- [Additional features...]

## Tech Stack

- **Languages**: [e.g., TypeScript, Python, Rust]
- **Frameworks**: [e.g., React, FastAPI, Actix]
- **Build Tools**: [e.g., Webpack, Poetry, Cargo]
- **Package Managers**: [e.g., npm, pip, cargo]
- **Testing**: [e.g., Jest, pytest, cargo test]

## Structure

```markdown
project-root/
├── src/ # [Description]
├── tests/ # [Description]
├── docs/ # [Description]
└── ... # [Other key directories]
```
````

**Key Files**:

- `[file]` - [Purpose]
- `[file]` - [Purpose]

**Entry Points**:

- `[file]` - [Description]

## Architecture

[Description of how components interact, main modules, data flow]

### Key Components:

- **[Component]**: [Role and responsibility]
- **[Component]**: [Role and responsibility]

## Backend Patterns and Practices

[Description for how to implement backend, database and service code in keeping with existing project standards]

- <observation1>
- <observation2>
- <...>

## Frontend Patterns and Practices

[Description for how to implement frontend, visual design and user experience approach in keeping with existing project standards]

- <observation1>
- <observation2>
- <...>

## Data & State

[Description for how to implement data persistence]

- <observation1>
- <observation2>
- <...>

## Performance & Security

[Description on performance considerations and security practices adopted]

- <observation1>
- <observation2>
- <...>

## Observability

| Aspect          | Current State | Note |
| --------------- | ------------- | ---- |
| Logging         | <…>           | <…>  |
| Metrics         | <…>           | <…>  |
| Analytics/Flags | <…>           | <…>  |

## Build & Quality Gates

| Purpose     | Command | Notes         |
| ----------- | ------- | ------------- |
| Lint        | `<cmd>` | <tool/config> |
| Type        | `<cmd>` | <tool/config> |
| Test        | `<cmd>` | <scope>       |
| Duplication | `<cmd>` | <threshold>   |
| Complexity  | `<cmd>` | <threshold>   |

## Testing Practices

| Test type                        | File path                                                    | Command                                                                                  |
| -------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests                       | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests                | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration (all analyzers) | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage                         | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |
| E2E / System (controlled apps)   | `test_codebase/`                                             | `PYTHONPATH=shared pytest shared/tests/integration -k e2e -v`                            |

## Git History Insights (<DAYS> days)

- Theme or initiative • supporting evidence
- Notable fix/feature • reference

---

## Task Impact Analysis

| File/Area   | Rationale                      |
| ----------- | ------------------------------ |
| `path:line` | <why change impacts this area> |

---

## Risks & Recommendations

| Risk   | Mitigation           |
| ------ | -------------------- |
| <risk> | <recommended action> |

---

## Open Questions

<!-- optional section -->

[Desription of unclear or unfinished implementation]

- <question1>
- <question2>
- <...>

```

## Examples

- `/todo-inspect-codebase "Map data flow for refunds"`
- `/todo-inspect-codebase "Identify auth risks in API" . --exclude node_modules,dist`
- `/todo-inspect-codebase "Assess React route performance" web/`
```
