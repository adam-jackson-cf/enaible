# get-primer v0.3

## Purpose

Generate a comprehensive project primer covering purpose, architecture, tech stack, commands, and testing practices.

## Variables

- `TARGET_PATH` ← first positional argument; defaults to current directory.
- `DOC_FILES[]` ← list of documentation files discovered (e.g., CLAUDE.md, AGENTS.md, README\*).
- `$ARGUMENTS` ← raw argument string (for logging).

## Instructions

- Read all relevant docs (CLAUDE.md, AGENTS.md, README variants) before synthesizing conclusions.
- Use Serena MCP tools when available for codebase discovery; fall back to CLI tools otherwise.
- Capture findings for purpose, features, tech stack, architecture, commands, and testing.
- Summaries must be concise yet comprehensive, referencing concrete files and directories.
- Include recent git history insights to surface active development themes.

## Workflow

1. **Run inspect codebase**

   - Run prompt "/todo-inspect-codebase" pointed at current project

2. **Generate Project Primer**

   - Compile findings into standardized markdown format
   - Present comprehensive project overview

## Output

````markdown
# Project: [Name]

[Concise description of what this project is and does]

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

## Backend Patterns and Practices to follow

[Description for how to implement backend, database and service code in keeping with existing project standards]

## Frontend Patterns and Practices to follow

[Description for how to implement frontend, visual design and user experience approach in keeping with existing project standards]

## Build & Quality Gate Commands

- **Build**: `[command]` - [Description if needed]
- **Test**: `[command]` - [Description if needed]
- **Lint**: `[command]` - [Description if needed]
- **Dev/Run**: `[command]` - [Description if needed]
- **[Other]**: `[command]` - [Description if needed]

## Testing

**Framework**: [Testing framework used]

**Running Tests**:

```bash
[command to run tests]
```

**Creating New Tests**:
[Instructions on where tests go and basic test structure example]

````

## Examples

```bash
# Generate primer for current repo
/get-primer

# Target a subdirectory
/get-primer packages/service
````
