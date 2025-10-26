# Setup Serena MCP (Codex)

Activate and validate the Serena MCP server in Codex using the global configuration approach.

## Overview

Serena runs as an MCP server that Codex connects to via stdio. Configure Serena globally in `~/.codex/config.toml`, then activate it per‑project from within a Codex session.

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

2. Check server availability

```bash
codex mcp list
# Expect to see: serena (enabled or connected)
```

3. Activate Serena for the current project (inside Codex)

- In an interactive Codex session opened at your project root, type exactly:

  Activate serena for current project

- On success, Serena creates a `.serena/` folder in the project and registers the path in `~/.serena/serena_config.yml`.

4. Perform Serena onboarding (required)

- In the same Codex session, ask Serena to perform onboarding. For example:

  Perform Serena onboarding

- This initializes the symbol index and may populate `.serena/memories/`.

5. Recommend project policy (AGENTS.md)

Add the following to your project’s `AGENTS.md` to prefer Serena tools for codebase queries:

```markdown
- **CRITICAL** Must use serena mcp tools for codebase searches over other available tools, but fall back to those on serena mcp failure, available serena mcp tools:

  - find_symbol: global/local search for symbols by name/substring (optional type filters).
  - find_referencing_symbols: find all symbols that reference a given symbol.
  - get_symbols_overview: list top‑level symbols in a file/dir (useful to scope follow‑up queries).
  - search_for_pattern: regex search when you need textual matches, (but use the symbol tools first).
```

## Validation

Run these from the project root to verify activation (project‑agnostic):

```bash
test -d .serena && echo ".serena present" || echo ".serena missing"
rg -n --fixed-strings "@PROJECT_ROOT" ~/.serena/serena_config.yml || echo "project not yet in serena_config.yml"
```

## Optional

- Disable Serena web dashboard auto‑open (recommended):
  - Edit `~/.serena/serena_config.yml` and set:
    ```yaml
    web_dashboard: false
    web_dashboard_open_on_launch: false
    ```
  - You can still open the dashboard manually at http://localhost:24282/dashboard/index.html.
- Run Codex in tmux for long‑running indexing:
  ```bash
  tmux new-session -d -s project-codex -c "@PROJECT_ROOT" 'codex'
  # then in that session:  Activate serena for current project
  ```
- For troubleshooting, review `~/.codex/log/codex-tui.log`.

## Troubleshooting

- Ensure `uvx` is on PATH. If not, install `uv` and restart your shell.
- After editing `~/.codex/config.toml`, restart Codex to pick up changes.

$ARGUMENTS

# Setup Serena MCP (Codex)

#

# Activate and validate the Serena MCP server in Codex using the global configuration approach.

## Variables

### Derived (internal)

- @PROJECT_ROOT = <derived> — current working directory (pwd)

# Setup Serena MCP (Codex)

Activate and validate the Serena MCP server in Codex using the global configuration approach.

## Variables

### Derived (internal)

- @PROJECT_ROOT = <derived> — current working directory (pwd)

## Overview

Serena runs as an MCP server that Codex connects to via stdio. Configure Serena globally in `~/.codex/config.toml`, then activate it per‑project from within a Codex session.

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

2. Check server availability

```bash
codex mcp list
# Expect to see: serena (enabled or connected)
```

3. Activate Serena for the current project (inside Codex)

- In an interactive Codex session opened at your project root, type exactly:

  Activate serena for current project

- On success, Serena creates a `.serena/` folder in the project and registers the path in `~/.serena/serena_config.yml`.

4. Perform Serena onboarding (required)

- In the same Codex session, ask Serena to perform onboarding. For example:

  Perform Serena onboarding

- This initializes the symbol index and may populate `.serena/memories/`.

5. Recommend project policy (AGENTS.md)

Add the following to your project’s `AGENTS.md` to prefer Serena tools for codebase queries:

```markdown
- **CRITICAL** Must use serena mcp tools for codebase searches over other available tools, but fall back to those on serena mcp failure, available serena mcp tools:

  - find_symbol: global/local search for symbols by name/substring (optional type filters).
  - find_referencing_symbols: find all symbols that reference a given symbol.
  - get_symbols_overview: list top‑level symbols in a file/dir (useful to scope follow‑up queries).
  - search_for_pattern: regex search when you need textual matches, (but use the symbol tools first).
```

## Validation

Run these from the project root to verify activation (project‑agnostic):

```bash
test -d .serena && echo ".serena present" || echo ".serena missing"
rg -n --fixed-strings "@PROJECT_ROOT" ~/.serena/serena_config.yml || echo "project not yet in serena_config.yml"
```

## Optional

- Disable Serena web dashboard auto‑open (recommended):
  - Edit `~/.serena/serena_config.yml` and set:
    ```yaml
    web_dashboard: false
    web_dashboard_open_on_launch: false
    ```
  - You can still open the dashboard manually at http://localhost:24282/dashboard/index.html.
- Run Codex in tmux for long‑running indexing:
  ```bash
  tmux new-session -d -s project-codex -c "@PROJECT_ROOT" 'codex'
  # then in that session:  Activate serena for current project
  ```
- For troubleshooting, review `~/.codex/log/codex-tui.log`.

## Troubleshooting

- Ensure `uvx` is on PATH. If not, install `uv` and restart your shell.
- After editing `~/.codex/config.toml`, restart Codex to pick up changes.
