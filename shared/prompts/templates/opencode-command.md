<!-- template format for opencode markdown command -->
<!-- Docs: https://opencode.ai/docs/commands/ -->

<!--
FRONTMATTER (define these in real YAML frontmatter when instantiating):
  description: One-line summary shown in slash picker
  agent: build | plan | <custom-agent-name> (defined in opencode.json or .opencode/agent/)
  model: anthropic/claude-3-5-sonnet-20241022 (optional override)
  subtask: true | false (run as a subtask)

ARGUMENTS (expansion rules):
  $1..$9: expand to first nine positional args
  $ARGUMENTS: expands to all args joined by a single space
  $$: preserved literally (emit a dollar sign)
  quoted: wrap an argument in double quotes to include spaces

TOOLS (controlled by agent/permissions):
  list: bash | edit | write | read | grep | glob | list | patch | todowrite | todoread | webfetch
  permission values: allow | ask | deny
  bash map example: {"*":"allow","git push":"ask","terraform *":"deny"}

FILE REFERENCES:
  @path includes file or directory contents in context (e.g., @shared/tests, @pytest.ini)
-->

---

description: <!-- one-line summary shown in slash picker -->
agent: <!-- build | plan | <custom-agent-name> -->
model: <!-- optional model override (e.g., anthropic/claude-3-5-sonnet-20241022) -->
subtask: <!-- true | false -->

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
  - $1 → TARGET (e.g., path or identifier)
  - $2 → MODE (e.g., plan|build|analyze)
  - $3 → OPTION (e.g., fast|strict)
  - $4..$9 → optional extras (document if used)
  - $ARGUMENTS → full raw argument string (space-joined)
- Rename TARGET/MODE/OPTION to suit your command; do not print the variable names in the final output.

## Instructions

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Ask before running long or destructive operations.

## Workflow

1. Step-by-step list of actions (each step starts with a verb).
2. Validate prerequisites and guard-rails early.
3. Perform the core task deterministically.
4. Save/emit artifacts and verify results.

## Output Contract

Use this structure for the final deliverable. Do not include the contract text, comments, or any example blocks in your response.

- Top-level sections: `# RESULT`, `## DETAILS`
- RESULT contains a single “Summary:” line (concise, one sentence)
- DETAILS contains bullets describing:
  - What ran or changed
  - Where it ran/changed (files/paths)
  - How to verify (exact commands or steps)

## Example (do not copy verbatim)

```md
# RESULT

- Summary: Ran unit tests with coverage and summarized failures.

## DETAILS

- What ran: PYTHONPATH=shared pytest --maxfail=1 --cov=shared --cov-report=term-missing
- Where it ran: repo root; focused modules under shared/
- How to verify: repeat the command; exit code 0, coverage > 85%
```

## Response Rules

- Output only the deliverable in the contract shape above.
- Do not include this section, explanations, or any example text.
- Replace all placeholders with concrete values; do not print angle brackets.

## Examples (optional)

```bash
# 1) Minimal invocation
/<command-name>

# 2) With a specific target argument used in the workflow
/<command-name> ./shared/tests

# 3) With @file and @dir references for added context
/<command-name> @shared/tests/unit @pytest.ini
```
