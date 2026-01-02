# GitHub Copilot System Adapter

This adapter enables enaible shared prompts and skills to render for [GitHub Copilot](https://docs.github.com/en/copilot).

## Configuration Structure

| Scope        | Directory                            |
| ------------ | ------------------------------------ |
| Repository   | `.github/`                           |
| Personal     | GitHub.com Settings > Copilot        |
| Organization | GitHub.com Org Settings (Enterprise) |

## File Formats

### Custom Instructions

Instructions guide Copilot's behavior without explicit invocation.

**Basic instructions**: `.github/copilot-instructions.md`

```markdown
# Project Instructions

This is a TypeScript project using React.

## Code Style

- Use functional components with TypeScript interfaces
- Prefer named exports over default exports
- Keep cyclomatic complexity under 10
```

**Contextual instructions**: `.github/instructions/*.instructions.md`

```markdown
---
applyTo: "**/*.ts, **/*.tsx"
description: TypeScript and React standards
---

## TypeScript Guidelines

- Enable strict mode
- Avoid `any` type
- Define explicit return types
```

**Agent instructions**: `AGENTS.md` at repository root

### Slash Commands (Prompts)

Prompts are reusable templates in `.github/prompts/*.prompt.md`:

```markdown
---
description: Review code for quality and best practices
mode: ask | edit | agent
model: claude-sonnet-4-5-20250929
tools: ["githubRepo", "search/codebase", "edit", "terminal"]
---

Review the selected code for:

- Code quality and readability
- Error handling and edge cases

Code to review:
${selection}
```

**Variables:**

- `${selection}` - Currently selected text
- `${file}` - Current file path
- `${input:varName}` - User-provided input
- `${input:varName:placeholder}` - Input with placeholder

**Modes:**

- `ask` - Conversational responses
- `edit` - Direct code modifications
- `agent` - Autonomous multi-step tasks

### Custom Agents

Agents are markdown files in `.github/agents/*.agent.md`:

```markdown
---
name: security-reviewer
description: Security and vulnerability analysis expert
tools: ["read", "search", "githubRepo"]
model: model-identifier
handoffs:
  - code-fixer
---

# Security Reviewer

You are a security expert specializing in identifying vulnerabilities.

## Review Process

1. Check for injection vulnerabilities
2. Review authentication/authorization
3. Identify data exposure risks
```

**Tools:** `read`, `search`, `edit`, `terminal`, `githubRepo`

### Skills

Skills are stored in `.github/skills/<skill-name>/SKILL.md`:

```markdown
---
name: skill-name
description: What this skill does. USE WHEN [trigger condition]
allowed-tools: @BASH, @READ
---

# Skill Name

## Workflow

Step 1: ...
Step 2: ...
```

**Directory structure:**

```
.github/skills/<skill-name>/
├── SKILL.md (required)
├── references/
├── scripts/
└── assets/
```

**Constraints:**

- `name`: lowercase, hyphens, max 64 characters
- `description`: include "USE WHEN..." trigger phrase
- `allowed-tools`: accepted but currently ignored by Copilot

## Instruction Precedence

1. **Personal** (highest) - GitHub.com settings
2. **Repository** - `.github/` files
3. **Organization** (lowest) - Enterprise only

## References

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions)
- [About Agent Skills](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills)
- [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/customization)
