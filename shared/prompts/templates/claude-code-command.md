<!-- template format for claude-code custom slash command -->
<!-- Docs: https://docs.claude.com/en/docs/claude-code/slash-commands -->

<FRONTMATTER>
allowed-tools: <!-- Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git log:*), Bash(git diff:*); Read(./path|glob), Write(./path|glob), Edit(./path|glob), MultiEdit(./path|glob), NotebookEdit(./path|glob), NotebookRead(./path|glob); Grep, Glob, Task, TodoWrite, WebFetch, WebSearch, Write; MCP: mcp__server, mcp__server__tool (no wildcards) -->
argument-hint: <!-- e.g. [type] [scope] [message] -->
description: <!-- one-line summary for /help -->
model: <!-- e.g. claude-3-5-haiku-20241022 (inherits if omitted) -->
disable-model-invocation: <!-- true | false (default false) -->
</FRONTMATTER>

<ARGUMENTS>
$1..$9: <!-- expand to the first nine positional args -->
$ARGUMENTS: <!-- expands to all arguments joined by a single space -->
$$: <!-- preserved literally (use to emit a dollar sign) -->
quoted: <!-- wrap an argument in double quotes to include spaces -->
</ARGUMENTS>

<TOOLS>
list: <!-- Bash | Edit | Glob | Grep | MultiEdit | NotebookEdit | NotebookRead | Read | Task | TodoWrite | WebFetch | WebSearch | Write -->
mcprules: <!-- mcp__github | mcp__github__get_issue (no wildcards) -->
</TOOLS>

<SHELL_OUTPUT_INJECTION>
!`<bash>`: <!-- injects command output into context; requires Bash(...) in allowed-tools -->
</SHELL_OUTPUT_INJECTION>

<FILE_REFERENCES>
@path: <!-- include file or directory contents in context (e.g. @src, @README.md) -->
</FILE_REFERENCES>

# Purpose

State the objective in one sentence. Be direct and outcome-focused.

## Variables

- Define inputs and their sources (e.g., from $ARGUMENTS or environment).
- Example: TYPE, SCOPE, MESSAGE

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

List concise facts to confirm completion (IDs, paths, counts, statuses).
