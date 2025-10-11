# Setup Serena MCP (Codex)

Activate and validate the Serena MCP server in Codex using the global configuration approach.

## Overview

Serena runs as an MCP server that Codex connects to via stdio. We configure Serena globally in `~/.codex/config.toml`, then activate it per-project with a one-line instruction inside Codex.

## Prerequisites

- `uvx` available (from the `uv` Python toolchain). Check with `uvx --version`.
- Global Codex config contains a Serena entry:

```toml
[mcp_servers.serena]
command = "uvx"
args = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex"]
```

If this block is missing, add it to `~/.codex/config.toml`, then restart Codex.

## Steps

1. Verify global config

```bash
rg -n "^\[mcp_servers\.serena\]" ~/.codex/config.toml || echo "Serena block missing in ~/.codex/config.toml"
```

2. Check connection

```bash
codex mcp list
# Expect to see: serena (connected or available)
```

3. Activate for current project

Add the following the project level `./AGENTS.md`

```markdown
- **CRITICAL** Must use serena mcp tools for codebase searches over other available tools, but fall back to those on serena mcp failure, available serena mcp tools:

  - find_symbol: global/local search for symbols by name/substring (optional type filters).
  - find_referencing_symbols: find all symbols that reference a given symbol.
  - get_symbols_overview: list top‑level symbols in a file/dir (useful to scope follow‑up queries).
  - search_for_pattern: regex search when you need textual matches, (but use the symbol tools first).
```

Now update the user with the following - "You will need to reload your codex session, on reload tell codex to activate serena by saying this in the session - Activate serena for current project - this will create a .serena folder and initiate its index."

## Optional

- Disable Serena web dashboard auto-open (recommended):
  - Edit `~/.serena/serena_config.yml` and set:
    ```yaml
    web_dashboard: false
    web_dashboard_open_on_launch: false
    ```
  - You can still open the dashboard manually at http://localhost:24282/dashboard/index.html.
- For troubleshooting, review `~/.codex/log/codex-tui.log`.

## Troubleshooting

- Ensure `uvx` is on PATH. If not, install `uv` and restart your shell.
- After editing `~/.codex/config.toml`, you must restart Codex to pick up changes.

## Tips

- ensure you activate serena once verified installed - this should produce a .serena folder and initial index in the current project

$ARGUMENTS
