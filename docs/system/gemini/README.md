# Gemini CLI System Adapter

This adapter enables enaible shared prompts and skills to render for [Gemini CLI](https://github.com/google-gemini/gemini-cli).

## Configuration Structure

| Scope   | Directory    |
| ------- | ------------ |
| Project | `.gemini/`   |
| User    | `~/.gemini/` |

## File Formats

### Context Files (GEMINI.md)

Context files provide persistent instructions to Gemini CLI. They are discovered from cwd upward, with more specific files overriding general ones.

**Locations:**

- `~/.gemini/GEMINI.md` - Global context
- `.gemini/GEMINI.md` - Project context
- `GEMINI.md` - Repository root context

```markdown
# Project Context

This is a TypeScript monorepo using Bun.

## Code Style

- Use functional components
- Prefer named exports

## Build Commands

- Install: `bun install`
- Test: `bun test`
```

**Import other markdown:** Use `@file.md` syntax to import additional context files.

### Slash Commands

Commands are TOML files in `.gemini/commands/` (project) or `~/.gemini/commands/` (user):

```toml
description = "Brief description of the command"
prompt = '''
# Command Title

Your prompt instructions here.

Arguments: {{args}}
'''
```

**Usage:** Type `/command-name` in the CLI

### Settings

Configuration in `~/.gemini/settings.json`:

```json
{
  "theme": "dark",
  "sandbox_mode": "ask",
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@github/mcp-server"]
    }
  }
}
```

### MCP Servers

Configure MCP servers in settings.json or via CLI:

```bash
gemini mcp add <server>
gemini mcp list
gemini mcp remove <server>
```

**Usage:** `@servername command` (e.g., `@github List my PRs`)

## Built-in Tools

| Tool                  | Purpose                   |
| --------------------- | ------------------------- |
| Codebase Investigator | Analyze codebase          |
| Edit                  | Replace file content      |
| FindFiles             | Glob pattern file search  |
| GoogleSearch          | Web search with grounding |
| ReadFile              | Read file contents        |
| ReadFolder            | List directory contents   |
| Shell                 | Execute shell commands    |

**List tools:** `/tools` command

## CLI Usage

```bash
# Interactive mode
gemini

# Direct prompt
gemini "explain this code"
gemini -p "what is gcloud deploy command"

# JSON output for scripting
gemini --output-format json "analyze project"
gemini --output-format stream-json "complex task"

# Shell mode
gemini
> !ls -la    # Single command
> !          # Enter persistent shell mode
```

## References

- [Gemini CLI GitHub](https://github.com/google-gemini/gemini-cli)
- [Google Developers Docs](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
- [Gemini CLI Cheatsheet](https://www.philschmid.de/gemini-cli-cheatsheet)
