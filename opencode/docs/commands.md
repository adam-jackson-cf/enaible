# OpenCode Commands Documentation

**Source:** https://opencode.ai/docs/commands/
**Scraped:** 2025-09-10

---

## Overview

Custom commands in OpenCode allow you to create specialized prompts for repetitive tasks that can be executed in the Terminal User Interface (TUI).

## Creating Command Files

Commands can be created in two primary ways:

1. Markdown files in the `command/` directory
2. JSON configuration in `opencode.jsonc`

### Markdown Command Example

Create a file `.opencode/command/test.md`:

```markdown
---
description: Run tests with coverage
agent: build
model: anthropic/claude-3-5-sonnet-20241022
---

Run the full test suite with coverage report and show any failures.
Focus on the failing tests and suggest fixes.
```

### JSON Command Configuration

In `opencode.jsonc`:

```json
{
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    }
  }
}
```

## Prompt Configuration

### Arguments

Use `$ARGUMENTS` to pass dynamic arguments to commands:

```markdown
---
description: Create a new component
---

Create a new React component named $ARGUMENTS with TypeScript support.
Include proper typing and basic structure.
```

Example usage: `/component Button`

### Shell Output

Inject shell command output using _!`command`_:

```markdown
---
description: Analyze test coverage
---

Here are the current test results:!`npm test`
Based on these results, suggest improvements to increase coverage.
```

### File References

Include file contents using `@` followed by filename:

```markdown
---
description: Review component
---

Review the component in @src/components/Button.tsx.
Check for performance issues and suggest improvements.
```

## Command Options

### Template (Required)

Defines the prompt sent to the Language Model.

### Description

Provides a brief explanation of the command's purpose.

### Agent (Optional)

Specifies which agent executes the command. Defaults to "build".

### Model (Optional)

Overrides the default model for this specific command.

## Usage Examples

### Basic Command

```markdown
---
description: Generate documentation
---

Generate comprehensive documentation for the current project.
Include API references and usage examples.
```

### Command with Arguments

```markdown
---
description: Create feature branch
---

Create a new feature branch named $ARGUMENTS and switch to it.
Set up the initial commit structure.
```

### Complex Analysis Command

```markdown
---
description: Security audit
agent: security
---

Perform a comprehensive security audit of the codebase:!`npm audit`
Analyze the results and provide remediation steps.
```

## Best Practices

1. **Clear Descriptions**: Always include descriptive titles for your commands
2. **Specific Prompts**: Write detailed prompts to get better results
3. **Use Arguments**: Leverage `$ARGUMENTS` for flexible commands
4. **Agent Selection**: Choose appropriate agents for specialized tasks
5. **Shell Integration**: Use shell output injection for dynamic context

## File Structure

```
.opencode/
├── command/
│   ├── test.md
│   ├── component.md
│   └── audit.md
└── opencode.jsonc
```

Commands defined in markdown files take precedence over JSON configurations when both exist for the same command name.
