# Setup Serena MCP (Claude Code)

Configure and activate the Serena MCP server for Claude Code using the IDE-centric context recommended by the Serena README.

## Behavior

Claude should set up Serena with the `ide-assistant` context (best for IDE-style clients like Claude Code), verify connectivity, optionally disable the Serena web dashboard auto-open, and then activate Serena for the current project.

## Steps

1. Check prerequisites

- Ensure `uvx` is installed and on PATH: `uvx --version`.

2. Add or update the MCP server entry

- Remove any previous entry (ignore errors):
  ```bash
  claude mcp remove serena || true
  ```
- Add Serena with the IDE assistant context and current project path:
  ```bash
  claude mcp add serena -- \
    uvx --from git+https://github.com/oraios/serena \
    serena start-mcp-server \
    --context ide-assistant \
    --project "$(pwd)"
  ```

3. Optionally disable the web dashboard auto-open

- Edit `~/.serena/serena_config.yml` and set:
  ```yaml
  web_dashboard: false
  web_dashboard_open_on_launch: false
  ```
  You can still open the dashboard manually at http://localhost:24282/dashboard/index.html.

4. Verify connection

```bash
claude mcp list
# Expect: serena (connected)
```

5. Activate Serena for this project

- In your Claude Code session, say this exactly:

Activate the current dir as project using serena

6. Sanity check (optional)

- Ask Serena to perform a lightweight action (e.g., list project files or analyze a single file) and confirm success.

## Notes

- The `--` separator is required to pass arguments to the Serena process.
- `ide-assistant` is the recommended context for Claude Code; use `codex` only when integrating with the Codex CLI.
- Logs: check Claude’s logs and Serena’s own logs if needed.

## Example Usage

```bash
/setup-serena-mcp
```

$ARGUMENTS
