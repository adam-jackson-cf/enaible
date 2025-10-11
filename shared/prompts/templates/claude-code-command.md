<!-- template format for claude-code custom slash command -->
<!-- Docs: https://docs.claude.com/en/docs/claude-code/slash-commands -->

<!--
FRONTMATTER (define these in real YAML frontmatter when instantiating):
  allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git log:*), Bash(git diff:*); Read(./path|glob); Write(./path|glob); Edit(./path|glob); MultiEdit(./path|glob); NotebookEdit(./path|glob); NotebookRead(./path|glob); Grep; Glob; Task; TodoWrite; WebFetch; WebSearch; Write; MCP tools by exact name: mcp__server, mcp__server__tool (no wildcards)
  argument-hint: [type] [scope] [message]
  description: One-line summary for /help
  model: claude-3-5-haiku-20241022 (inherits if omitted)
  disable-model-invocation: true | false (default false)

ARGUMENTS (expansion rules):
  $1..$9: expand to first nine positional args
  $ARGUMENTS: expands to all args joined by a single space
  $$: preserved literally (emit a dollar sign)
  quoted: wrap an argument in double quotes to include spaces

TOOLS (referenceable in allowed-tools):
  list: Bash | Edit | Glob | Grep | MultiEdit | NotebookEdit | NotebookRead | Read | Task | TodoWrite | WebFetch | WebSearch | Write
  mcp rules: mcp__github | mcp__github__get_issue (no wildcards)

SHELL OUTPUT INJECTION:
  !`<bash>` injects command output into context (requires a matching Bash(...) rule in allowed-tools)

FILE REFERENCES:
  @path includes file or directory contents in context (e.g., @src, @README.md)
-->

---

allowed-tools:
argument-hint: [type] [scope] [message]
description: One-line summary for /help
model: claude-3-5-haiku-20241022 (inherits if omitted)

---

# Purpose

State the objective in one sentence. Be direct and outcome-focused.

## Environment checks (optional)

These are examples of env checks, some prompts will have no env checks, only create env checks where the prompt requires it - but do include a sentence oulining immediate exit if you include an env check section. Env checks are items required for a prompt workflow beyond its standard practice or available tools, which may not be supplied by a user request or argument.

- Python available: !`python --version`
- Imports resolve (when using analyzer scripts): !`PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`
- Runner help (optional): !`PYTHONPATH="$SCRIPTS_ROOT" python -m core.cli.run_analyzer --help | head -n 5`
- Script resolution: resolve `SCRIPT_PATH` from project → user → prompt; then set `SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"`

## Variables

- Bind positional arguments to explicit names for clarity:
  - $1 → TYPE (e.g., feat/fix/chore)
  - $2 → SCOPE (e.g., api, ui)
  - $3 → MESSAGE (short subject)
  - $4..$9 → optional extras (document if used)
  - $ARGUMENTS → full raw argument string (space-joined)
- Rename TYPE/SCOPE/MESSAGE to suit your command; do not print the variable names in the final output.

## Instructions

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Avoid verbosity; prefer concrete actions over descriptions.

## Workflow

1. Step-by-step list of actions (each step starts with a verb).
2. Validate prerequisites and guard-rails early.
3. Perform the core task deterministically.
4. Save/emit artifacts and verify results.

## Output

This section should be an output structure detailing what this workflow should return and how, in a suitable format:

e.g.

```md
# RESULT

- Summary: <one line>

## DETAILS

- What changed
- Where it changed
- How to verify
```

Or

```json
{
  "CycleName": {
    "version": 3,
    "objective": {
      "task_objective": "Deliver authentication hardening for user-facing API",
      "purpose": "Reduce takeover risk for privileged accounts while keeping login latency flat.",
      "affected_users": ["admin-operators", "support-analysts"],
      "requirements": [
        "Require MFA for admin roles",
        "Provide backup codes during enrollment",
        "Log MFA events for audit export"
      ],
      "constraints": ["no-db-schema-changes", "release-window:2025-Q4"],
      "assumptions": ["backwards-compatible client SDKs"],
      "open_questions": [],
      "clarifications": [
        {
          "question": "Do support analysts require MFA on first login?",
          "answer": "Yes, enforce MFA immediately after first login."
        }
      ]
    }
  }
}
```

## Examples (optional)

```bash
# 1) Minimal invocation with positional arguments
/<command-name> feat api "add pagination"

# 2) With explicit target path as $1 (used by Environment checks)
/<command-name> ./services/api
```
