# Purpose

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

1. Confirm repository context
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not inside a git repository because commit history analysis is mandatory.
2. Resolve target directory
   - Default to `.` unless a path argument is provided.
   - Change working context for subsequent commands as required.
3. Collect documentation
   - Attempt to read, in order: `CLAUDE.md`, `AGENTS.md`, `README.md`/`README.rst`/`README.*`.
   - Store key excerpts for inclusion in the primer.
4. Analyze codebase
   - Preferred: use Serena MCP (`find_symbol`, `find_referencing_symbols`, `search_for_pattern`, etc.).
   - Fallback: `ls`, `tree`, `rg`, `grep`.
   - Capture insights for:
     - Purpose & Features
     - Tech Stack (languages, frameworks, package managers)
     - Architecture & structure (directory layout, key components)
     - Commands (package scripts, Makefiles, setup scripts)
     - Testing strategy (frameworks, command to run tests)
5. Review git history
   - `git log -3 --stat --decorate=short --date=relative`.
   - Summarize objectives, modified areas, and approaches from recent commits.
6. Synthesize primer
   - Populate the standardized primer template (see Output).
   - Provide concise bullet points and clear file references.
7. Deliver results
   - Share primer content in markdown.
   - Note open questions or missing documentation for follow-up.

## Output

```md
# Project: <Name>

<One-paragraph description>

## Features

- <Feature summary>

## Tech Stack

- **Languages**: <list>
- **Frameworks**: <list>
- **Build Tools**: <list>
- **Package Managers**: <list>
- **Testing**: <frameworks/commands>

## Structure
```

project-root/
├── <dir> # <description>
└── …

````

**Key Files**
- <path> — <purpose>

**Entry Points**
- <path> — <description>

## Architecture
- <component interactions, data flow, deployment model>

## Commands
- **Build**: `<command>`
- **Test**: `<command>`
- **Lint**: `<command>`
- **Dev**: `<command>`

## Testing
- Framework: <name>
- Run: ```bash
<command>
````

- Creating Tests: <guidance>

## Recent Activity

1. <commit hash> — <message> (<author>, <relative date>)
   - Files: <summary>
   - Notes: <key changes>

````

## Examples

```bash
# Generate primer for current repo
/get-primer

# Target a subdirectory
/get-primer packages/service
````
