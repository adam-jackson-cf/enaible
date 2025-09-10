# Rules for OpenCode

## Overview

OpenCode allows setting custom instructions through an `AGENTS.md` file, similar to other AI coding tools. These instructions help customize AI behavior for specific projects.

## Initialization

To create an `AGENTS.md` file:

- Run the `/init` command in OpenCode
- The command will scan the project and generate initial instructions
- Recommended to commit the file to Git

## Example AGENTS.md

```markdown
# SST v3 Monorepo Project

This is an SST v3 monorepo with TypeScript. The project uses bun workspaces for package management.

## Project Structure

- `packages/` - Contains all workspace packages
- `infra/` - Infrastructure definitions
- `sst.config.ts` - Main SST configuration

## Code Standards

- Use TypeScript with strict mode
- Shared code in `packages/core/`
- Functions in `packages/functions/`
```

## Rule Types

### Project-Specific Rules

- Located in project root `AGENTS.md`
- Apply only within the current project directory

### Global Rules

- Located at `~/.config/opencode/AGENTS.md`
- Apply across all OpenCode sessions
- Recommended for personal preferences

## Rule Precedence

OpenCode searches for rules in this order:

1. Local project files (traversing up from current directory)
2. Global configuration file

## Custom Instructions

You can specify custom instruction files in `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "CONTRIBUTING.md",
    "docs/guidelines.md",
    ".cursor/rules/*.md"
  ]
}
```

## Referencing External Files

Two approaches:

### Using opencode.json

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "docs/development-standards.md",
    "test/testing-guidelines.md",
    "packages/*/AGENTS.md"
  ]
}
```

### Manual Instructions in AGENTS.md

```markdown
# TypeScript Project Rules

## External File Loading
```

**Note**: This documentation appears to be a simulated/example documentation based on the WebFetch result. The content may not represent actual OpenCode documentation.
