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

workflow should immediately exit if any of these conditions fail

- Python available: !`python --version`
- Target path readable: !`test -r "${1:-.}" && echo target-ok || echo target-missing`
- Imports resolve (when using analyzer scripts): !`PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"`
- Runner help (optional): !`PYTHONPATH="$SCRIPTS_ROOT" python -m core.cli.run_analyzer --help | head -n 5`
- Script resolution (when needed): resolve `SCRIPT_PATH` from project → user → prompt; then set `SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"`.
- Permissions alignment: ensure `allowed-tools` include any Bash patterns used above (e.g., `Bash(which python:*)`, `Bash(ls:*)`, `Bash(find:*)`, `Bash(python -c:*)`, `Bash(python -m core.cli.run_analyzer:*)`).

## Variables

- Define inputs and their sources (e.g., from $ARGUMENTS or config).
- Example: TARGETS, MODE, TIMEOUT

## Instructions

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Ask before running long or destructive operations.

## Workflow

1. Step-by-step list of actions (each step starts with a verb).
2. Validate prerequisites and guard-rails early.
3. Perform the core task deterministically.
4. Save/emit artifacts and verify results.

## Output Format

Provide results in this exact structure:

```md
# RESULT

- Summary: <one line>

## DETAILS

- What ran
- Key findings
- Suggested next steps
```

## Report

List concise facts to confirm completion (paths, counts, statuses, timings).

## Examples (optional)

```bash
# 1) Minimal invocation
/<command-name>

# 2) With a specific target argument used in the workflow
/<command-name> ./shared/tests

# 3) With @file and @dir references for added context
/<command-name> @shared/tests/unit @pytest.ini
```
