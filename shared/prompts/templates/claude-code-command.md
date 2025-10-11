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
