<!-- template format for opencode markdown command -->
<!-- Docs: https://opencode.ai/docs/commands/ -->

<FRONTMATTER>
description: <!-- one-line summary shown in slash picker -->
agent: <!-- build | plan | <custom-agent-name> (defined in opencode.json or .opencode/agent/) -->
model: <!-- optional model override for this command (e.g. anthropic/claude-3-5-sonnet-20241022) -->
subtask: <!-- true | false (run as a subtask) -->
</FRONTMATTER>

<ARGUMENTS>
$1..$9: <!-- expand to the first nine positional args -->
$ARGUMENTS: <!-- expands to all arguments joined by a single space -->
$$: <!-- preserved literally (use to emit a dollar sign) -->
quoted: <!-- wrap an argument in double quotes to include spaces -->
</ARGUMENTS>

<TOOLS>
list: <!-- bash | edit | write | read | grep | glob | list | patch | todowrite | todoread | webfetch -->
permission: <!-- allow | ask | deny (bash supports prefix/glob maps: {"*":"allow","git push":"ask","terraform *":"deny"}) -->
</TOOLS>

<FILE_REFERENCES>
@path: <!-- include file or directory contents in context (e.g. @shared/tests, @pytest.ini) -->
</FILE_REFERENCES>

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

## Output

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
