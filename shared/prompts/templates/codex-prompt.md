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

## Variables

- Define inputs and their sources (e.g., from $ARGUMENTS or context).
- Example: FEATURE_NAME, FILE_PATH, STRICT

## Instructions

- Use short, imperative bullets.
- Call out IMPORTANT constraints explicitly.
- Avoid verbosity; prefer concrete changes over descriptions.

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

- What changed
- Where it changed
- How to verify
```

## Report

List concise facts to confirm completion (paths, counts, statuses).

## Examples (optional)

```bash
# 1) Minimal
/plan core "import optimizer"

# 2) Quoted args with spaces (affects $1/$2)
/plan "core api" "import optimizer"

# 3) Provide extra context via pasted code blocks or references
#    (Codex prompt files don’t support @file injection; include snippets inline.)
```

## Examples (optional)
