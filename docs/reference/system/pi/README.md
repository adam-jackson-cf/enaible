# Pi Coding Agent System Adapter

This adapter enables enaible shared prompts and skills to render for the [Pi coding agent](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent).

## Configuration Structure

| Scope   | Directory      |
| ------- | -------------- |
| Project | `.pi/`         |
| User    | `~/.pi/agent/` |

## File Formats

### Slash Commands

Commands are markdown files in `.pi/commands/*.md` with YAML frontmatter:

```markdown
---
description: Brief description
---

Prompt template with $1 (first arg) and $@ (all args)
```

### Skills

Skills are stored in `.pi/skills/**/SKILL.md` with required frontmatter:

```markdown
---
name: skill-name
description: What this skill does (max 1024 chars)
---

## Setup

...

## Usage

...
```

**Constraints:**

- `name`: lowercase, hyphens allowed, max 64 characters
- `description`: max 1024 characters, determines auto-loading trigger

### Custom Tools

TypeScript modules in `.pi/tools/*/index.ts`:

```typescript
import { CustomToolFactory } from "@anthropic-ai/pi"

const factory: CustomToolFactory = (pi) => ({
  name: "tool-name",
  description: "Tool description",
  parameters: Type.Object({
    /* Typebox schema */
  }),
  async execute(params, onUpdate) {
    // Implementation
    return result
  },
})

export default factory
```

### Hooks

TypeScript modules in `.pi/hooks/*.ts`:

```typescript
import { HookAPI } from "@anthropic-ai/pi"

export default function (pi: HookAPI) {
  pi.on("tool_call", async (event) => {
    // Handle tool calls
  })

  pi.on("session_start", async (event) => {
    // Handle session start
  })
}
```

## Context Files

- `AGENTS.md` - Project instructions (discovered from cwd upward)
- `.pi/SYSTEM.md` - System prompt override (replaces default)

## Session Format

Pi uses JSONL session files with tree structure. Each entry has `id` and `parentId` fields enabling in-place branching via `/tree` and `/branch` commands.

## Context Compaction

Configure in settings:

```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 8000,
    "keepRecentTokens": 4000
  }
}
```

## References

- [Pi Coding Agent Repository](https://github.com/badlogic/pi-mono/tree/main/packages/coding-agent)
- [Changelog](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/CHANGELOG.md)
