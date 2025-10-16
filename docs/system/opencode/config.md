# OpenCode.ai Configuration Documentation

**Source:** https://opencode.ai/docs/config/
**Scraped:** 2025-09-10 21:57:50

---

You can configure opencode using a JSON config file.

---

## Format

opencode supports both **JSON** and **JSONC** (JSON with Comments) formats.

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  // Theme configuration
  "theme": "opencode",
  "model": "anthropic/claude-sonnet-4-20250514",
  "autoupdate": true
}
```

---

## Locations

You can place your config in several different locations; they have the following order of precedence.

### Global

Place your global opencode config in `~/.config/opencode/opencode.json`. Use the global config for settings like themes, providers, or keybinds.

### Per project

You can also add an `opencode.json` in your project. It takes precedence over the global config. This is useful for providers or modes specific to the project.

When opencode starts, it looks for a config file in the current directory and traverses up to the nearest Git directory. This file is safe to check into Git and uses the same schema as the global one.

### Custom path

You can specify a custom config file path using the `OPENCODE_CONFIG` environment variable. This takes precedence over the global and project configs.

```sh
export OPENCODE_CONFIG=/path/to/my/custom-config.json
opencode run "Hello world"
```

---

## Schema

The config file schema is defined in [opencode.ai/config.json](https://opencode.ai/config.json). Your editor should be able to validate and autocomplete based on the schema.

---

## Models

Configure providers and models with the `provider`, `model`, and `small_model` options:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {},
  "model": "anthropic/claude-sonnet-4-20250514",
  "small_model": "anthropic/claude-3-5-haiku-20241022"
}
```

`small_model` is used for lightweight tasks (e.g., title generation). By default opencode tries a cheaper model if available; otherwise it falls back to your main model.

You can also configure local models. Learn more: https://opencode.ai/docs/models

---

## Themes

Set the theme via the `theme` option:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "theme": "opencode"
}
```

Learn more: https://opencode.ai/docs/themes

---

## Agents

Define specialized agents via the `agent` option:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "code-reviewer": {
      "description": "Reviews code for best practices and potential issues",
      "model": "anthropic/claude-sonnet-4-20250514",
      "prompt": "You are a code reviewer. Focus on security, performance, and maintainability.",
      "tools": {
        // Disable file modification tools for review-only agent
        "write": false,
        "edit": false
      }
    }
  }
}
```

You can also define agents using markdown files in `~/.config/opencode/agent/` or `.opencode/agent/`. Learn more: https://opencode.ai/docs/agents

---

## Sharing

Configure sharing through the `share` option:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "share": "manual"
}
```

Options:

- `"manual"` — Allow manual sharing via commands (default)
- `"auto"` — Automatically share new conversations
- `"disabled"` — Disable sharing entirely

Default is manual; use `/share` to explicitly share conversations. Learn more: https://opencode.ai/docs/share

---

## Commands

Configure custom commands with the `command` option:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "command": {
    "test": {
      "template": "Run the full test suite with coverage report and show any failures.\nFocus on the failing tests and suggest fixes.",
      "description": "Run tests with coverage",
      "agent": "build",
      "model": "anthropic/claude-3-5-sonnet-20241022"
    },
    "component": {
      "template": "Create a new React component named $ARGUMENTS with TypeScript support.\nInclude proper typing and basic structure.",
      "description": "Create a new component"
    }
  }
}
```

You can also define commands using markdown files in `~/.config/opencode/command/` or `.opencode/command/`. Learn more: https://opencode.ai/docs/commands

---

## Keybinds

Customize keybinds through the `keybinds` option:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "keybinds": {}
}
```

Learn more: https://opencode.ai/docs/keybinds

---

## Autoupdate

Control automatic updates with `autoupdate`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "autoupdate": false
}
```

---

## Formatters

Configure code formatters via the `formatter` option:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {
    "prettier": {
      "disabled": true
    },
    "custom-prettier": {
      "command": ["npx", "prettier", "--write", "$FILE"],
      "environment": {
        "NODE_ENV": "development"
      },
      "extensions": [".js", ".ts", ".jsx", ".tsx"]
    }
  }
}
```

Learn more: https://opencode.ai/docs/formatters

---

## Permissions

Control what AI agents can do through the `permission` option:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": "ask"
  }
}
```

- `edit` — whether file editing requires user approval (`"ask"` or `"allow"`)
- `bash` — whether bash commands require approval (`"ask"`, `"allow"`, or a pattern map)

Learn more: https://opencode.ai/docs/permissions

---

## MCP servers

Configure MCP servers with the `mcp` option:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {}
}
```

Learn more: https://opencode.ai/docs/mcp-servers

---

## Instructions

Provide instruction files to the model via `instructions`:

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

This accepts paths and glob patterns. Learn more about rules: https://opencode.ai/docs/rules

---

## Disabled providers

Disable automatically loaded providers using `disabled_providers`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "disabled_providers": ["openai", "gemini"]
}
```

When a provider is disabled:

- It won’t be loaded even if environment variables are set.
- It won’t be loaded even if keys are configured via `opencode auth login`.
- Its models won’t appear in model selection.

---

## Variables

Use variable substitution to reference environment variables and file contents.

### Env vars

Use `{env:VARIABLE_NAME}` to substitute environment variables:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "{env:OPENCODE_MODEL}",
  "provider": {
    "anthropic": {
      "models": {},
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

If the environment variable is not set, it will be replaced with an empty string.

### Files

Use `{file:path/to/file}` to substitute the contents of a file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["./custom-instructions.md"],
  "provider": {
    "openai": {
      "options": {
        "apiKey": "{file:~/.secrets/openai-key}"
      }
    }
  }
}
```

File paths can be:

- Relative to the config file directory
- Or absolute paths starting with `/` or `~`

Use cases:

- Keep sensitive data (API keys) in separate files.
- Include large instruction files without cluttering the config.
- Share common configuration snippets across multiple configs.

---
