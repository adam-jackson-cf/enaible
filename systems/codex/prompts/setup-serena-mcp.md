# Purpose

Activate and validate the Serena MCP server in Codex using the global configuration approach so every project can rely on the same Serena tooling.

## Variables

### Derived (internal)

- @PROJECT_ROOT = <derived> — current working directory (pwd)

## Instructions

- Ensure `uvx` is installed (`uvx --version`) before attempting any Serena actions.
- Maintain the Serena entry in `~/.codex/config.toml`; restart Codex after editing that file.
- Run all activation and onboarding phrases inside an interactive Codex session opened at @PROJECT_ROOT.
- Document the required Serena tools in `AGENTS.md` so the team understands the enforced search workflow.
- Use the validation commands to confirm `.serena/` assets exist and the project path is registered.

## Workflow

1. **Verify global config**

   - Confirm the Serena block exists in the Codex config:

     ```bash
     rg -n "^\[mcp_servers\.serena\]" ~/.codex/config.toml || echo "Serena block missing in ~/.codex/config.toml"
     ```

   - If missing, append:

     ```toml
     [mcp_servers.serena]
     command = "uvx"
     args = ["--from", "git+https://github.com/oraios/serena", "serena", "start-mcp-server", "--context", "codex"]
     ```

     Restart Codex after editing the file.

2. **Check server availability**

   - Make sure Codex sees Serena:

     ```bash
     codex mcp list
     # Expect: serena (enabled or connected)
     ```

3. **Activate Serena for @PROJECT_ROOT**

   - Inside Codex (with the workspace set to @PROJECT_ROOT) type exactly:

     Activate serena for current project

   - Serena should create `.serena/` in the repo and register the path in `~/.serena/serena_config.yml`.

4. **Perform Serena onboarding**

   - Still inside Codex, run:

     Perform Serena onboarding

   - This builds the symbol index and may populate `.serena/memories/`.

5. **Recommend project policy (AGENTS.md)**

   - Add the mandatory rule block:

     ```markdown
     - **CRITICAL** Must use serena mcp tools for codebase searches over other available tools, but fall back when Serena fails. Available tools:
       - find_symbol — global/local search by name/substring (optional type filters).
       - find_referencing_symbols — list symbols referencing a given symbol.
       - get_symbols_overview — enumerate top-level symbols in a file/dir.
       - search_for_pattern — regex search when symbol tools are insufficient.
     ```

6. **Optional dashboard & automation**

   - Disable auto-open for the Serena dashboard (recommended):

     ```yaml
     # ~/.serena/serena_config.yml
     web_dashboard: false
     web_dashboard_open_on_launch: false
     ```

   - Run Codex in tmux for long-lived indexing sessions:

     ```bash
     tmux new-session -d -s project-codex -c "@PROJECT_ROOT" 'codex'
     # inside that session: Activate serena for current project
     ```

   - Troubleshoot via `~/.codex/log/codex-tui.log` when activation fails.

## Validation

Run from @PROJECT_ROOT to verify setup:

```bash
test -d .serena && echo ".serena present" || echo ".serena missing"
rg -n --fixed-strings "@PROJECT_ROOT" ~/.serena/serena_config.yml || echo "project not yet in serena_config.yml"
```

## Troubleshooting

- Ensure `uvx` is on PATH; install `uv` if necessary and restart the shell.
- Restart Codex whenever `~/.codex/config.toml` changes to reload MPC entries.

## Output

```md
# RESULT

- Summary: Serena MCP configured for Codex.

## DETAILS

- Project Path: <@PROJECT_ROOT>
- AGENTS.md Updated: <yes/no>
- Dashboard Auto-Open: <disabled|unchanged>
- MCP Status: <enabled|error> (from `codex mcp list`)

## NEXT STEPS

1. Keep `.serena/` committed or documented per repo policy.
2. Use Serena tools (find_symbol, find_referencing_symbols, etc.) for code navigation.
3. Visit http://localhost:24282/dashboard/index.html if manual access is required.
```
