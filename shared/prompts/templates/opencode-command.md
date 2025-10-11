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

# Purpose

State the objective in one sentence. Be direct and outcome-focused.

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
