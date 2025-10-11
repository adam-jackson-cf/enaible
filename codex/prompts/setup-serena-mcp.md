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

Say this exactly in the current Codex session:

Activate the current dir as project using serena

4. Re-check status

```bash
codex mcp list
```

If `serena` still isn’t active, restart Codex and repeat step 3.

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
