# OpenCode Formatters Documentation

**Source:** https://opencode.ai/docs/formatters/
**Extracted:** 2025-09-10

---

## Overview

OpenCode automatically formats files after writing or editing using language-specific formatters, ensuring code follows project styles and conventions.

## How It Works

When OpenCode writes or edits a file, it:

1. **Checks file extension** against enabled formatters
2. **Runs appropriate formatter** command
3. **Applies formatting changes** automatically

## Built-in Formatters

OpenCode includes built-in support for multiple language formatters:

| Formatter          | File Extensions                                                        | Requirements                            |
| ------------------ | ---------------------------------------------------------------------- | --------------------------------------- |
| **gofmt**          | `.go`                                                                  | `gofmt` command available               |
| **mix**            | `.ex`, `.exs`, `.eex`, `.heex`, `.leex`, `.neex`, `.sface`             | `mix` command available                 |
| **prettier**       | `.js`, `.jsx`, `.ts`, `.tsx`, `.html`, `.css`, `.md`, `.json`, `.yaml` | `prettier` dependency in `package.json` |
| **biome**          | `.js`, `.jsx`, `.ts`, `.tsx`, `.html`, `.css`, `.md`, `.json`, `.yaml` | `biome.json(c)` config file             |
| **zig**            | `.zig`, `.zon`                                                         | `zig` command available                 |
| **clang-format**   | `.c`, `.cpp`, `.h`, `.hpp`, `.ino`                                     | `.clang-format` config file             |
| **ktlint**         | `.kt`, `.kts`                                                          | `ktlint` command available              |
| **ruff**           | `.py`, `.pyi`                                                          | `ruff` command available with config    |
| **rubocop**        | `.rb`, `.rake`, `.gemspec`, `.ru`                                      | `rubocop` command available             |
| **standardrb**     | `.rb`, `.rake`, `.gemspec`, `.ru`                                      | `standardrb` command available          |
| **htmlbeautifier** | `.erb`, `.html.erb`                                                    | `htmlbeautifier` command available      |

## Configuration

Configure formatters through the `formatter` section in your `opencode.json` file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "formatter": {}
}
```

### Configuration Properties

Each formatter can be configured with the following properties:

| Property      | Type      | Description                             |
| ------------- | --------- | --------------------------------------- |
| `disabled`    | `boolean` | Disable the formatter                   |
| `command`     | `string`  | Custom command to run for formatting    |
| `environment` | `object`  | Environment variables for the formatter |
| `extensions`  | `array`   | File extensions to handle               |

### Disabling Formatters

To disable a specific formatter:

```json
{
  "formatter": {
    "prettier": {
      "disabled": true
    }
  }
}
```

### Custom Commands

Override the default formatting command:

```json
{
  "formatter": {
    "prettier": {
      "command": "npx prettier --write"
    }
  }
}
```

### Environment Variables

Set environment variables for formatters:

```json
{
  "formatter": {
    "ruff": {
      "environment": {
        "RUFF_CONFIG": "/path/to/custom/ruff.toml"
      }
    }
  }
}
```

### Custom Extensions

Modify which file extensions a formatter handles:

```json
{
  "formatter": {
    "prettier": {
      "extensions": [".js", ".ts", ".jsx", ".tsx", ".json"]
    }
  }
}
```

## Language-Specific Examples

### JavaScript/TypeScript (Prettier)

```json
{
  "formatter": {
    "prettier": {
      "command": "npx prettier --write --config .prettierrc"
    }
  }
}
```

### Python (Ruff)

```json
{
  "formatter": {
    "ruff": {
      "command": "ruff format",
      "environment": {
        "RUFF_CONFIG": "pyproject.toml"
      }
    }
  }
}
```

### Go (gofmt)

```json
{
  "formatter": {
    "gofmt": {
      "command": "gofmt -w"
    }
  }
}
```

### Ruby (RuboCop)

```json
{
  "formatter": {
    "rubocop": {
      "command": "bundle exec rubocop --autocorrect"
    }
  }
}
```

## Troubleshooting

### Formatter Not Working

1. **Check if the formatter command is available** in your PATH
2. **Verify configuration files** exist (e.g., `.prettierrc`, `biome.json`)
3. **Check file extensions** match the formatter's configuration
4. **Review OpenCode logs** for formatter errors

### Common Issues

**Prettier not formatting:**

- Ensure `prettier` is installed as a dependency
- Check for a valid `.prettierrc` or `prettier.config.js`

**Ruff not working:**

- Verify `ruff` is installed and available
- Check for `pyproject.toml` or `.ruff.toml` configuration

**Biome not detected:**

- Ensure `biome.json` or `biome.jsonc` exists in project root
- Check Biome is installed via npm/yarn

### Performance Considerations

- Formatters run synchronously after file changes
- Large files may experience formatting delays
- Consider disabling formatters for very large files if needed

## Best Practices

1. **Use project-specific configurations** for consistent formatting
2. **Disable formatters selectively** if they conflict with existing workflows
3. **Test formatter configurations** before committing to ensure they work correctly
4. **Keep formatter tools updated** for best compatibility and features
5. **Use environment variables** for flexible configuration across different environments

---

_For more information, visit the [OpenCode Documentation](https://opencode.ai/docs/)_
