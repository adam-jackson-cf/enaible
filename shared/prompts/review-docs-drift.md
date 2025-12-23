# Purpose

Audit README.md and AGENTS.md files for documentation drift against local workspace changes and update them to reflect current behavior.

## Variables

### Optional (derived from $ARGUMENTS)

- (none)

### Derived (internal)

- @STAGED_FILES — staged file list from `git diff --name-only --cached`
- @UNSTAGED_FILES — unstaged file list from `git diff --name-only`
- @CHANGED_FILES — combined staged and unstaged file list
- @DIFF_STAT — combined diff stat from staged + unstaged changes
- @DOC_INVENTORY — list of README.md and AGENTS.md files in the repo
- @DOC_DIFF — combined staged + unstaged diffs limited to README.md and AGENTS.md

## Instructions

- Inspect every README.md and AGENTS.md file for drift against current staged and unstaged changes.
- Keep roles distinct: README.md is end-user guidance; AGENTS.md is developer or LLM rules.
- Update documentation directly; remove outdated instructions instead of soft-deprecating them.
- Maintain existing tone and structure; do not add new sections unless required to resolve drift.
- Exit immediately if there are no staged or unstaged changes.
- Use @DIFF_STAT and @DOC_DIFF as evidence for edits.
- Provide a short status note describing what changed or that no drift was found.

## Workflow

1. Check for local changes.
   - Collect @STAGED_FILES and @UNSTAGED_FILES using `git diff --name-only --cached` and `git diff --name-only`.
   - If both sets are empty, exit immediately with a status note that no changes were found.
2. Combine @STAGED_FILES and @UNSTAGED_FILES into @CHANGED_FILES.
3. Derive @DIFF_STAT and @DOC_DIFF from staged + unstaged diffs.
4. Use @DOC_INVENTORY to locate all README.md and AGENTS.md files.
5. Compare documentation content against @CHANGED_FILES using @DOC_DIFF and code context.
6. Update documentation with minimal edits that resolve drift.
7. Summarize changes and provide the status note.

## Output

```md
# RESULT

- Summary: <one line>

## DOCUMENTATION UPDATES

- <file path>: <what changed and why>

## STATUS NOTE

- <short note confirming updates or stating no drift was found>
```
