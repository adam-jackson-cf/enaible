---
description: Summarize recent context from git history and edited files
---

# Recent Context Review

Analyze recent activity from context bundles and git history to understand current work and provide quick orientation for continuing development.

## Arguments

- `--uuid UUID` - Filter analysis to a specific session UUID
- `--verbose` - Expand truncated content from linked conversation files (when available)
- `--search-term TERM` - Search for sessions containing semantically matching content

## Behavior

This command performs a comprehensive review of recent activity by:

**FIRST - Resolve SCRIPT_PATH:**

1. **Try project-level .opencode folder**:

   ```bash
   Glob: ".opencode/scripts/context/context_bundle_capture_opencode.py"
   ```

2. **Try user-level .opencode folder**:

   ```bash
   Bash: ls "$HOME/.config/opencode/scripts/context/context_bundle_capture_opencode.py"
   ```

3. **Try shared/ fallback**:

   ```bash
   Glob: "shared/context/context_bundle_capture_opencode.py"
   ```

4. **Interactive fallback if not found**:
   - List searched locations: `.opencode/scripts/context/`, `$HOME/.config/opencode/scripts/context/`, and `shared/context/`
   - Ask user: "Could not locate context bundle capture script. Please provide full path to the script:"
   - Validate provided path contains the script
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "import context.context_bundle_capture_opencode; print('env OK')"
```

1. **Context Bundle Analysis**

   - Extract context data using the resolved script path
   - Filter to specific UUID if `--uuid` provided
   - Search for semantic matches if `--search-term` provided
   - Parse returned operations for file access patterns and user objectives
   - In `--verbose` mode: expand truncated content
   - Summarize session activity and identify workflow patterns

2. **Git Status Review**

   - Review actively worked on files `git status`
   - Analyze changed files and modification patterns
   - Identify areas of active development and recent focus

3. **Git History Review**

   - Build a recent timeline: `git log --stat --date=iso --max-count 8`
   - For high-activity files (from context bundles or `git status`), trace evolution with `git log --follow --oneline -20 -- <file>`
   - When specific code chunks matter, run `git blame -w -C -C -C -- <file>` to surface origins while ignoring whitespace/moves
   - Mine commit intent: `git log --grep "\bfix\b" --since="30 days ago"` and other targeted keywords (refactor, perf, security)
   - Surface first/last occurrence of patterns via `git log -S"<pattern>" --oneline`
   - Record architectural turning points, renames, and rationale pulled from these commands

4. **Contributor & Pattern Mapping**

   - Identify key contributors with `git shortlog -sn --since="90 days ago"`
   - Cross-reference contributors with the files they touch most (use `git log --stat --author="<name>" --since="90 days ago"` when necessary)
   - Note recurring problem themes, follow-up fixes, and outstanding risks

5. **Generate Consolidated Summary**
   - Combine findings from context bundles, status, and history into a cohesive narrative
   - Highlight active development areas, contributors, and historical risk patterns
   - Provide clear orientation for resuming work or onboarding teammates

## Process

### 1. Context Bundle Discovery

```bash
# Extract context data using the resolved script
# Generate semantic variations when search term is provided
if [ -n "$SEARCH_TERM" ]; then
    # Generate semantic variations based on search term
    SEMANTIC_VARIATIONS=$(cat <<EOF
{
    "$(echo "$SEARCH_TERM" | cut -d' ' -f1)": [
        "$(echo "$SEARCH_TERM" | cut -d' ' -f1)s",
        "$(echo "$SEARCH_TERM" | cut -d' ' -f1)ing",
        "$(echo "$SEARCH_TERM" | cut -d' ' -f1)ed"
    ]
}
EOF
)
else
    SEMANTIC_VARIATIONS=""
fi

PYTHONPATH="$SCRIPTS_ROOT" python "$SCRIPT_PATH" --days 2 ${UUID:+--uuid "$UUID"} ${SEARCH_TERM:+--search-term "$SEARCH_TERM"} ${SEMANTIC_VARIATIONS:+--semantic-variations "$SEMANTIC_VARIATIONS"} --output-format json

# Cross-project aggregation
PYTHONPATH="$SCRIPTS_ROOT" python "$SCRIPT_PATH" --days 2 --include-all-projects --output-format json

# From the JSON, present a compact view when available:
# - Sessions: group `sessions[].user_messages` by session, newest first (limit 3 per session)
# - High-activity files: top `operations[].file_path` by frequency (read/write)
# - Commands: recent `operations[].command` (bash) with timestamps
```

### 2. Git Status Analysis

```bash
# Show any modified but yet to be commit files
git status --short
```

### 3. Git History Analysis

```bash
# Recent timeline overview
git log --stat --date=iso --max-count 8

# Contributor map
git shortlog -sn --since="90 days ago"

# Pattern searches (swap keyword/pattern as needed)
git log --grep="fix" --since="30 days ago"
git log -S"TODO" --oneline

# File-focused archaeology (run for top N files)
git log --follow --oneline -20 -- path/to/file
git blame -w -C -C -C -- path/to/file
```

### 4. Data Analysis and Summary

- Parse returned JSON data for operation patterns
- Handle data with semantic search results and UUID filtering
- In `--verbose` mode: expand truncated content from detailed operations
- Extract file access frequencies and modification types (accounting for deduplication)
- Identify command usage patterns and user objectives
- Correlate with git history for comprehensive view

**Semantic Variations Generation**:

When `--search-term` is provided, generate semantic variations dynamically:

```bash
# For single-word search terms
{
    "auth": ["auths", "authing", "authed"]
}

# For multi-word search terms, use first word
{
    "authentication": ["authentications", "authenticating", "authenticated"]
}
```

The LLM should enhance this with context-aware variations based on the search domain:

- Technical terms: related concepts, implementations, patterns
- Actions: verb forms, synonyms, related activities
- Domains: associated technologies, frameworks, tools

## Output Format

```markdown
# Recent Activity Summary

## Context Bundles Analysis

- **Sessions Found**: [count] sessions
- **Date Range**: [earliest timestamp] to [latest timestamp]
- **Filter**: [All recent sessions | UUID: {uuid} | Search: {term}]
- **Mode**: [Concise summaries | Verbose with full content]

### File Operations Summary

- **Most Accessed**:
  - `[file_path]` (read, edit, write operations)
  - `[file_path]` (read operations only)
- **Recent Edits**: [list of files modified via Write/Edit operations]
- **Files Read**: [list of files accessed via Read operations]
- **Search Results**: [sessions matching search criteria]

### Session Patterns

- **Common Workflows**: [identified patterns in operation sequences]
- **User Objectives**: [summary of goals extracted from prompts]

_Timeline of File Evolution_

1. `[date]` — `[hash]` `[commit message]` (Authored by [author])
   - **Scope**: [files / modules]
   - **Intent**: [feature, fix, refactor, etc.]
   - **Notes**: [renames, follow-up TODOs, regressions addressed]

[Repeat for meaningful hops]

_Key Contributors & Domains_

- **[Contributor]**: [primary areas touched, sample commits, expertise inference]
- **[Contributor]**: [primary areas touched, sample commits, expertise inference]

_Historical Issues & Fixes_

- **Pattern**: `[keyword or failure mode]`
  - **Introduced**: `[commit hash/date]`
  - **Fix / Mitigation**: `[commit hash/date]`
  - **Outstanding Risks**: [notes]

_Change Patterns_

- **File / Component**: [summary of change cadence, rewrite moments, churn indicators]
- **Pattern Searches**: [results from `git log --grep` or `-S` calls]

## Git Status (Uncommitted Work)

- **Files Changed**: [count] ([additions/deletions])
- **Hot Spots**: [directories/components with noteworthy deltas]

## Consolidated Analysis

- **Current Development Focus**: [link context bundles ↔ git history ↔ status]
- **Most Active Files**: [list with reasoning]
- **Recommended Next Checks**: [tests, follow-ups, stakeholders]
```

## Usage Examples

```bash
# Get recent activity summary (default: concise summaries for last 2 days)
/todo-recent-context

# Analyze specific session with concise summaries
/todo-recent-context --uuid a1b2c3d4-e5f6-7890-abcd-ef1234567890

# Get detailed analysis with full conversation content
/todo-recent-context --verbose

# Analyze specific session with full detail
/todo-recent-context --uuid a1b2c3d4-e5f6-7890-abcd-ef1234567890 --verbose

# Search for sessions with semantic matching
/todo-recent-context --search-term "authentication bug"

# Search within specific session
/todo-recent-context --uuid a1b2c3d4-e5f6-7890-abcd-ef1234567890 --search-term "refactor"

# Enhanced semantic search with LLM-generated variations
# When searching for "authentication", the LLM might generate:
{
    "authentication": ["auth", "login", "signin", "authorize", "security", "verify", "authenticate"],
    "bug": ["error", "issue", "problem", "fix", "debug", "repair", "resolve"],
    "performance": ["speed", "fast", "slow", "optimize", "efficiency", "latency"]
}
```

$ARGUMENTS
