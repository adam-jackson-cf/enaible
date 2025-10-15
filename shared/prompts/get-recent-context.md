# Purpose

Summarize recent project activity by correlating context bundle captures with git status and history for rapid situational awareness.

## Variables

- `$UUID_FILTER` ← use `$ARGUMENTS` value passed to `--uuid` (optional).
- `$VERBOSE_MODE` ← use `$ARGUMENTS` boolean flag set when `--verbose` (optional).
- `$SEARCH_TERM` ← use `$ARGUMENTS` value passed to `--search-term` (optional).

## Instructions

- ALWAYS resolve the context bundle script before performing any analysis.
- Respect flag semantics: filter by UUID, expand content in verbose mode, and apply semantic search when requested.
- Store raw JSON outputs from the script for traceability.
- Combine context bundle insights with git status and history to produce a cohesive narrative.
- Highlight active files, commands, and workflows; surface follow-up questions where context is thin.

## Workflow

1. Confirm prerequisites
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not inside a git repository because git history is required.
   - Run `ls .claude/scripts/context/context_bundle_capture_claude.py || ls "$HOME/.claude/scripts/context/context_bundle_capture_claude.py"`; if both fail, request an explicit script path and exit if unavailable.
2. Parse flags
   - Capture `UUID_FILTER`, `VERBOSE_MODE`, and `SEARCH_TERM`.
3. Resolve script location
   - Search project-level `.claude/scripts/context/`.
   - Fallback to `$HOME/.claude/scripts/context/`.
   - Prompt for a path if unresolved; verify the script exists.
4. Prepare environment
   - Derive `SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"`.
   - Run the import readiness command: `PYTHONPATH="$SCRIPTS_ROOT" python -c "import context.context_bundle_capture_claude; print('env OK')"`; abort on failure.
5. Extract context bundles
   - Build semantic variations JSON when `SEARCH_TERM` provided.
   - Execute:
     ```bash
     PYTHONPATH="$SCRIPTS_ROOT" python "$SCRIPT_PATH" --days 2 \
       ${UUID_FILTER:+--uuid "$UUID_FILTER"} \
       ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} \
       ${SEMANTIC_VARIATIONS:+--semantic-variations "$SEMANTIC_VARIATIONS"} \
       --output-format json
     ```
   - Store the JSON response for analysis.
6. Analyze git activity
   - `git status --short` → capture uncommitted changes and focus areas.
   - `git log --stat -3 --pretty=format:"%h - %s (%an, %ar)"` → summarize last three commits.
7. Synthesize findings
   - Identify most accessed files, command usage patterns, and objectives from context bundles.
   - Correlate bundle activity with git status and recent commits.
   - In `VERBOSE_MODE`, expand truncated bundle content for richer detail.
8. Produce report
   - Follow the structured output format with sections for Context Bundles, Git History, Git Status, Development Focus, and Consolidated Analysis.
   - Highlight next steps or open questions suggested by the recent activity.

## Output

```md
# Recent Activity Summary

## Context Bundles

- Sessions: <count> (Filter: <all|uuid|search>)
- Date Range: <start> → <end>
- Mode: <concise|verbose>

### File Operations

- Most Accessed: <file> (read/write counts)
- Recent Edits: <files>
- Search Matches: <terms/results>

## Git History (Last 3 Commits)

1. <hash> - <message> (<author>, <relative date>)
   - Files: <count> (+<adds> / -<dels>)
   - Notes: <key change summary>

## Git Status

- Modified: <files>
- Untracked: <files>
- Focus Areas: <directories/components>

## Consolidated Analysis

- Current Focus: <narrative>
- Risks / Blockers: <items>
- Suggested Next Steps: <bullets>
```

## Examples

```bash
# Review recent context and git activity
/get-recent-context

# Focus on a specific session and expand content
/get-recent-context --uuid a1b2c3d4-e5f6-7890-abcd-ef1234567890 --verbose

# Search for sessions mentioning authentication
/get-recent-context --search-term "authentication bug"
```
