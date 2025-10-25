# Purpose

Configure the Serena MCP server with the IDE-assistant context, update project guidance, and verify Claude Code connectivity.

## Variables

### Derived (internal)

- @PROJECT_ROOT = <derived> — current working directory (pwd)
- @SERENA_CONFIG = <derived> — ~/.serena/serena_config.yml

## Instructions

- Verify CLI availability upfront: run `uvx --version` and `claude --version`; halt and surface errors if either command fails.
- ALWAYS remove any existing `serena` MCP entry before re-adding to avoid duplicate registrations.
- Use the IDE-assistant context and current project path for optimal Claude Code integration.
- Document the MCP tools available in `AGENTS.md`; emphasize that Serena search tools are mandatory.
- Offer optional configuration to disable the Serena web dashboard auto-open.
- Verify connection status via `claude mcp list` and surface the result.

## Workflow

1. **Establish Project Context**

   - Capture the current working directory as `PROJECT_ROOT=$(pwd)` and keep the IDE-assistant context ready for registration.
   - Reference @SERENA_CONFIG for optional dashboard tweaks later in the workflow.

2. **Register MCP Server**

   - Remove any existing Serena registration before re-adding:

     ```bash
     claude mcp remove serena || true
     ```

   - Add Serena with the IDE-assistant context bound to `PROJECT_ROOT`:

     ```bash
     claude mcp add serena -- \
       uvx --from git+https://github.com/oraios/serena \
       serena start-mcp-server \
       --context ide-assistant \
       --project "$PROJECT_ROOT"
     ```

3. **Update Project Documentation**

   - Append the mandatory Serena tooling block to `AGENTS.md`, covering `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, and `search_for_pattern`.

4. **Optional Dashboard Configuration**

   - When disabling auto-open is desired, edit `SERENA_CONFIG`:

     ```yaml
     web_dashboard: false
     web_dashboard_open_on_launch: false
     ```

   - Note the manual dashboard URL for reference: `http://localhost:24282/dashboard/index.html`.

5. **Verify Connectivity**

   - Confirm Serena appears as `connected`:

     ```bash
     claude mcp list
     ```

6. **Report Completion**
   - Summarize the registration command used, documentation updates, optional dashboard changes, and the connectivity status for the user.

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
