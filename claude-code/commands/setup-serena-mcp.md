# Purpose

Configure the Serena MCP server with the IDE-assistant context, update project guidance, and verify Claude Code connectivity.

## Variables

- `PROJECT_ROOT` ← output of `pwd`.
- `SERENA_CONFIG` ← `~/.serena/serena_config.yml`.
- `$ARGUMENTS` ← raw argument string (no additional flags supported).

## Instructions

- ALWAYS remove any existing `serena` MCP entry before re-adding to avoid duplicate registrations.
- Use the IDE-assistant context and current project path for optimal Claude Code integration.
- Document the MCP tools available in `AGENTS.md`; emphasize that Serena search tools are mandatory.
- Offer optional configuration to disable the Serena web dashboard auto-open.
- Verify connection status via `claude mcp list` and surface the result.

## Workflow

1. Check prerequisites
   - Run `uvx --version`; exit immediately if `uvx` is unavailable because it is required to launch the Serena MCP server.
   - Run `claude --version`; exit immediately if the Claude CLI cannot be reached because configuration steps will fail.
   - Capture current working directory as `PROJECT_ROOT`.
2. Register MCP server
   - Remove existing entry (ignore errors):
     ```bash
     claude mcp remove serena || true
     ```
   - Add Serena using IDE-assistant context:
     ```bash
     claude mcp add serena -- \
       uvx --from git+https://github.com/oraios/serena \
       serena start-mcp-server \
       --context ide-assistant \
       --project "$PROJECT_ROOT"
     ```
3. Update project documentation
   - Append the required instruction block to the project-level `AGENTS.md`, describing mandatory Serena tool usage (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `search_for_pattern`).
4. Optional dashboard configuration
   - If requested, edit `~/.serena/serena_config.yml` to set:
     ```yaml
     web_dashboard: false
     web_dashboard_open_on_launch: false
     ```
   - Mention manual dashboard URL: `http://localhost:24282/dashboard/index.html`.
5. Verify connectivity
   - Run `claude mcp list` and confirm Serena appears as `connected`.
6. Report completion
   - Summarize registered command, documentation update, optional config, and connection status.

## Output

```md
# RESULT

- Summary: Serena MCP configured for Claude Code.

## DETAILS

- Context: ide-assistant
- Project Path: <PROJECT_ROOT>
- Dashboard Auto-Open: <disabled|unchanged>
- AGENTS.md Updated: <yes/no>
- MCP Status: <connected|error> (from `claude mcp list`)

## NEXT STEPS

1. Restart Claude Code or IDE if connection isn’t detected.
2. Use Serena tools (`find_symbol`, `find_referencing_symbols`, etc.) for code searches.
3. Visit http://localhost:24282/dashboard/index.html when manual dashboard access is needed.
```

## Examples

```bash
# Configure Serena MCP for the current project
/setup-serena-mcp
```
