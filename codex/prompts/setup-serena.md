# Setup Serena (activate + validate)

Quickly activate the Serena MCP server for the current project and validate connectivity from this Codex session.

## What to do

1. Verify Serena is configured

- Use Bash to check that `~/.codex/config.toml` contains an `[mcp_servers.serena]` entry.
- If missing: report instructions to add it, then stop.

2. Check connection state

- Run `codex mcp list` and confirm `serena` appears (connected). If not connected, instruct to restart Codex and retry.

3. Activate Serena for this project

- Send the following instruction verbatim to initialize the project context:

  Activate the current dir as project using serena

4. Sanity check

- After activation, run `codex mcp list` again and report the `serena` status.
- If available, perform a lightweight Serena action (e.g., list project files or analyze a single file) and report success.

## Notes

- Codex looks for Serena logs and sessions under:
  - Sessions: `~/.codex/sessions/YYYY/MM/DD/*.jsonl`
  - Logs: `~/.codex/log/codex-tui.log`
- If `serena` isn’t listed, ensure Codex was restarted after adding the TOML entry.

$ARGUMENTS
