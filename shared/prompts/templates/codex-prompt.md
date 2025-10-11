<!-- template format for codex prompts -->
<!-- Docs: https://github.com/openai/codex/blob/main/docs/prompts.md -->

<!--
ARGUMENTS (expansion rules):
  $1..$9: expand to first nine positional args
  $ARGUMENTS: expands to all args joined by a single space
  $$: preserved literally (emit a dollar sign)
  quoted: wrap an argument in double quotes to include spaces
-->

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
  - $1 → AREA (e.g., core|api|ui)
  - $2 → FEATURE (short name)
  - $3 → OPTION (e.g., strict|fast)
  - $4..$9 → optional extras (document if used)
  - $ARGUMENTS → full raw argument string (space-joined)
- Rename AREA/FEATURE/OPTION to suit your prompt; do not print the variable names in the final output.

## Instructions

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Avoid verbosity; prefer concrete changes over descriptions.

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
  - What changed
  - Where it changed (files/paths)
  - How to verify (exact commands or steps)

## Example (do not copy verbatim)

```md
# RESULT

- Summary: Produced a concrete TODO plan for the import optimizer feature.

## DETAILS

- What changed: Added tasks for src/core/optimizer.ts and tests
- Where it changed: src/core/optimizer.ts, tests/core/optimizer.test.ts
- How to verify: run bunx tsc --noEmit and bun run test
```

## Response Rules

- Output only the deliverable in the contract shape above.
- Do not include this section, explanations, or any example text.
- Replace all placeholders with concrete values; do not print angle brackets.

## Examples (optional)

```bash
# 1) Minimal
/plan core "import optimizer"

# 2) Quoted args with spaces (affects $1/$2)
/plan "core api" "import optimizer"

# 3) Provide extra context via pasted code blocks or references
#    (Codex prompt files don’t support @file injection; include snippets inline.)
```
