# Claude Code System Adapter

This adapter enables enaible shared prompts and skills to render for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

## Configuration Structure

| Scope      | Directory               |
| ---------- | ----------------------- |
| Project    | `.claude/`              |
| User       | `~/.claude/`            |
| Enterprise | Platform-specific paths |

## File Formats

### Settings

Settings are JSON files that configure Claude Code behavior:

- **User settings**: `~/.claude/settings.json`
- **Project settings**: `.claude/settings.json`
- **Local settings**: `.claude/settings.local.json` (git-ignored)

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)", "Read(~/.zshrc)"],
    "deny": ["Read(./.env)", "Read(./secrets/**)"]
  },
  "env": { "MY_VAR": "value" },
  "model": "claude-sonnet-4-20250514",
  "hooks": {}
}
```

**Key settings**: `permissions`, `env`, `model`, `hooks`, `outputStyle`, `statusLine`

### Slash Commands

Commands are markdown files in `.claude/commands/*.md` (project) or `~/.claude/commands/*.md` (user):

```markdown
---
allowed-tools: Bash(git:*), Read
description: Create a git commit
argument-hint: [message]
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS

Context:

- Current git status: !`git status`
- Recent commits: !`git log --oneline -5`
```

**Features:**

- `$ARGUMENTS` or `$1`, `$2` for parameters
- `!`backticks`` for bash execution
- `@file` for file references

### Skills

Skills are stored in `.claude/skills/**/SKILL.md` (project) or `~/.claude/skills/**/SKILL.md` (user):

```markdown
---
name: skill-name
description: What this skill does and when to use it (max 1024 chars)
allowed-tools: Read, Grep, Glob
---

# Skill Name

## Instructions

Step-by-step guidance for Claude.

## Examples

Concrete examples of using this skill.
```

**Constraints:**

- `name`: lowercase, hyphens allowed, max 64 characters
- `description`: determines auto-loading trigger
- `allowed-tools`: optional, restricts tool access when skill is active

### Hooks

Hooks are shell commands that execute at lifecycle events. Configure in `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "your-command" }]
      }
    ],
    "PostToolUse": [],
    "Notification": [],
    "Stop": []
  }
}
```

**Events:** `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Notification`, `Stop`, `SubagentStop`, `SessionStart`, `SessionEnd`

### Subagents

Subagents are markdown files in `.claude/agents/*.md` (project) or `~/.claude/agents/*.md` (user):

```markdown
---
name: code-reviewer
description: Expert code review specialist. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards of code quality.

When invoked:

1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately
```

**Fields:**

- `name`: unique identifier (lowercase, hyphens)
- `description`: when to invoke (include "PROACTIVELY" for automatic use)
- `tools`: optional comma-separated list (inherits all if omitted)

### Plugins

Plugins are directories with `.claude-plugin/plugin.json`:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
└── .mcp.json
```

**plugin.json:**

```json
{
  "name": "my-plugin",
  "description": "Plugin description",
  "version": "1.0.0",
  "author": { "name": "Your Name" }
}
```

**Commands:** `/plugin`, `/plugin install`, `/plugin marketplace add`

## Context Files

- `CLAUDE.md` - Project instructions (discovered from cwd upward)
- `.claude/settings.json` - Project configuration

## References

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Settings Reference](https://docs.anthropic.com/en/docs/claude-code/settings)
- [Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Hooks Guide](https://docs.anthropic.com/en/docs/claude-code/hooks)
- [Subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Plugins](https://docs.anthropic.com/en/docs/claude-code/plugins)
