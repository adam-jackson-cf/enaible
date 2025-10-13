# LSP Servers Documentation

**Source:** https://opencode.ai/docs/lsp/
**Extracted:** 2025-09-10

## Overview

opencode integrates with Language Server Protocol (LSP) to help LLMs interact with codebases. The integration provides:

- **Diagnostics feedback** - Real-time error and warning detection
- **Go-to-definition navigation** - Jump to symbol definitions
- **Find-references functionality** - Locate all references to symbols

## Built-in LSP Servers

opencode includes built-in LSP servers for multiple languages, automatically enabled when file extensions and requirements are met:

| LSP Server    | Extensions                 | Requirements              |
| ------------- | -------------------------- | ------------------------- |
| typescript    | .ts, .tsx, .js, .jsx, etc. | `typescript` dependency   |
| eslint        | .ts, .tsx, .js, .vue       | `eslint` dependency       |
| gopls         | .go                        | `go` command              |
| ruby-lsp      | .rb, .rake                 | `ruby` and `gem` commands |
| pyright       | .py, .pyi                  | `pyright` installed       |
| rust-analyzer | .rs                        | Rust toolchain            |
| clangd        | .c, .cpp, .h, .hpp         | clang tools               |
| jdtls         | .java                      | Java SDK                  |
| omnisharp     | .cs                        | .NET SDK                  |
| And more...   |                            |                           |

## How It Works

When opencode opens a file, it:

1. **Checks file extension** against enabled LSP servers
2. **Verifies requirements** are met for the language
3. **Starts appropriate LSP server** if not already running
4. **Establishes communication** for real-time feedback

## Configuration

Configure LSP servers in your `opencode.json` configuration file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "lsp": {}
}
```

### Configuration Options

Each LSP server can be configured with the following properties:

- **`disabled`** - Boolean to enable/disable the server
- **`command`** - Command array to start the LSP server
- **`extensions`** - File extensions the server should handle
- **`env`** - Environment variables to pass to the server
- **`initialization`** - Server-specific initialization options

### Disabling LSP Servers

To disable a specific LSP server:

```json
{
  "lsp": {
    "typescript": {
      "disabled": true
    }
  }
}
```

### Adding Custom LSP Servers

To add support for a custom language server:

```json
{
  "lsp": {
    "custom-lsp": {
      "command": ["custom-lsp-server", "--stdio"],
      "extensions": [".custom", ".mylang"]
    }
  }
}
```

### Advanced Configuration Example

```json
{
  "lsp": {
    "pyright": {
      "env": {
        "PYTHONPATH": "/custom/python/path"
      },
      "initialization": {
        "settings": {
          "python": {
            "analysis": {
              "typeCheckingMode": "strict"
            }
          }
        }
      }
    }
  }
}
```

## Environment Variables

### Disabling LSP Downloads

LSP server downloads can be disabled by setting the environment variable:

```bash
export OPENCODE_DISABLE_LSP_DOWNLOAD=true
```

This prevents opencode from automatically downloading and installing LSP servers.

## Troubleshooting

### Common Issues

1. **LSP server not starting**

   - Verify the language tools are installed
   - Check file extensions match server configuration
   - Review opencode logs for error messages

2. **Performance issues**

   - Consider disabling unused LSP servers
   - Limit LSP servers to specific project types
   - Use environment variables to control downloads

3. **Custom LSP integration**
   - Ensure the LSP server supports `--stdio` mode
   - Verify command path is accessible
   - Test server independently before integration

### Debug Mode

Enable debug logging to troubleshoot LSP issues:

```bash
OPENCODE_DEBUG=lsp opencode
```

## Supported Languages

opencode provides built-in support for 13+ programming languages through their respective LSP servers:

- **TypeScript/JavaScript** - Full type checking and IntelliSense
- **Python** - Type hints, imports, and syntax checking
- **Go** - Complete language support with gopls
- **Rust** - Advanced analysis with rust-analyzer
- **Ruby** - Syntax and semantic analysis
- **Java** - Enterprise-grade language support
- **C#** - .NET ecosystem integration
- **C/C++** - Native development support
- **And more...**

Each language server provides deep integration with the respective toolchain and ecosystem, enabling opencode to understand project structure, dependencies, and provide accurate code assistance.
