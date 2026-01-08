# Google Antigravity System Adapter

This adapter enables enaible shared prompts and skills to render for [Google Antigravity](https://antigravity.google), an agent-first development platform.

## Configuration Structure

| Scope     | Directory                |
| --------- | ------------------------ |
| Workspace | `.agent/`                |
| User      | `~/.gemini/antigravity/` |
| Global    | `~/.gemini/GEMINI.md`    |

## File Formats

### Rules

Rules are markdown files that provide persistent system-level instructions to guide agent behavior during code generation.

**Locations:**

- `~/.gemini/GEMINI.md` - Global rules
- `.agent/rules/*.md` - Workspace rules

```markdown
# Code Style Rules

- Follow PEP 8 style guide for Python
- Use TypeScript strict mode
- Keep cyclomatic complexity under 10
- Add JSDoc comments for public APIs
```

Rules are applied automatically without user intervention.

### Workflows

Workflows are saved prompts that can be triggered on demand with `/` commands.

**Locations:**

- `~/.gemini/antigravity/global_workflows/*.md` - Global workflows
- `.agent/workflows/*.md` - Workspace workflows

```markdown
---
description: Generate unit tests
---

# Generate Unit Tests

- Generate unit tests for each file and method
- Name test files with `test_` prefix
- Follow Arrange-Act-Assert pattern
- Mock external dependencies
```

**Usage:** Type `/workflow-name` in the agent interface

### Context Files (GEMINI.md)

Global context and instructions shared across projects.

**Location:** `~/.gemini/GEMINI.md`

## Development Modes

| Mode           | Behavior                                     |
| -------------- | -------------------------------------------- |
| Autopilot      | Agent acts autonomously                      |
| Review-driven  | Agent asks permission for actions            |
| Agent-assisted | User control with safe automations (default) |

## Interface Views

- **Editor View**: Traditional code editing with AI assistance
- **Manager View**: Oversee multiple agents working in parallel

## Supported Models

- Gemini 3 Pro
- Claude Sonnet 4.5
- GPT-4

## References

- [Google Antigravity](https://antigravity.google)
- [Getting Started Guide](https://codelabs.developers.google.com/getting-started-google-antigravity)
- [Customize Rules & Workflows](https://atamel.dev/posts/2025/11-25_customize_antigravity_rules_workflows/)
- [Google Developers Blog](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
