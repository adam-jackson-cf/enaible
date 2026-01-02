# Cursor IDE System Adapter

This adapter enables enaible shared prompts and skills to render for [Cursor IDE](https://cursor.com).

## Configuration Structure

| Scope   | Directory        |
| ------- | ---------------- |
| Project | `.cursor/rules/` |

## File Formats

### Rules

Cursor uses `.mdc` files (Markdown with Context) for custom rules and instructions, stored in `.cursor/rules/`:

```markdown
<!-- generated: enaible -->

<rule_category>

# Title

Content goes here...
</rule_category>
```

### Rule Categories

Rules are wrapped in XML-style category tags:

| Category          | Purpose                            |
| ----------------- | ---------------------------------- |
| `<coding>`        | General coding practices/standards |
| `<security>`      | Security-focused rules             |
| `<quality>`       | Code quality and refactoring       |
| `<performance>`   | Performance optimization           |
| `<debugging>`     | Debugging and troubleshooting      |
| `<planning>`      | Planning and design rules          |
| `<documentation>` | Documentation standards            |
| `<development>`   | Development workflow rules         |
| `<configuration>` | Configuration management           |
| `<scaffolding>`   | Project scaffolding and setup      |
| `<analysis>`      | Code analysis guidelines           |

### Variable Handling

Unlike other AI coding systems, Cursor rules are **static instructions** and do not support runtime variables. All `@TOKEN` placeholders from source prompts are removed or replaced with literal values during rendering.

### Hooks

Cursor supports lifecycle hooks configured via JSON. Place a `hooks.json` file in one of the supported scopes (highest precedence first):

| Scope       | File path                        |
| ----------- | -------------------------------- |
| Enterprise  | Managed via Cursor dashboard     |
| Project     | `<project>/.cursor/hooks.json`   |
| User        | `~/.cursor/hooks.json`           |
| System-wide | `/etc/cursor/hooks.json` (Linux) |

Each file contains a `hooks` object mapping hook names to arrays of command definitions:

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [{ "command": "./scripts/check.sh" }],
    "afterFileEdit": [{ "command": "./scripts/format.sh" }]
  }
}
```

**Supported events:** `beforeShellExecution`, `afterShellExecution`, `beforeMCPExecution`, `afterMCPExecution`, `beforeReadFile`, `afterFileEdit`, `beforeTabFileRead`, `afterTabFileEdit`, `beforeSubmitPrompt`, `afterAgentResponse`, `afterAgentThought`, and `stop`. Agent hooks apply to Cmd+K and chat, while Tab hooks (`beforeTabFileRead`, `afterTabFileEdit`) target inline completions.

Hooks receive structured JSON payloads describing the triggering action and can return permission decisions (e.g., allow, deny, ask) or follow-up instructions depending on the event. Scripts referenced in `command` can be absolute paths or relative to the `hooks.json` file, enabling auditing, enforcement, or automation around Cursor tool use.

## Managed Files

Files with the `<!-- generated: enaible -->` sentinel are automatically managed by the enaible CLI. Modify source prompts in `shared/prompts/` and re-render instead of editing directly.

## Rendering

```bash
# Render all prompts for Cursor
uv run enaible prompts render --system cursor

# Render specific prompt
uv run enaible prompts render --prompt analyze-security --system cursor
```

## References

- [Cursor Documentation](https://docs.cursor.com)
- [Cursor Rules](https://docs.cursor.com/rules)
