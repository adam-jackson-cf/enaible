---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(ls:*), Read, Glob
argument-hint: [--uuid UUID] [--verbose] [--search-term TERM]
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

1. **Try project-level .claude folder**:

   ```bash
   Glob: ".claude/scripts/analyzers/context/context_bundle_capture_claude.py"
   ```

2. **Try user-level .claude folder**:

   ```bash
   Bash: ls "$HOME/.claude/scripts/analyzers/context/context_bundle_capture_claude.py"
   ```

3. **Interactive fallback if not found**:
   - List searched locations: `.claude/scripts/analyzers/context/` and `$HOME/.claude/scripts/analyzers/context/`
   - Ask user: "Could not locate context bundle capture script. Please provide full path to the script:"
   - Validate provided path contains the script
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "import context.context_bundle_capture_claude; print('env OK')"
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

   - Retrieve last 5 commits with details using `git log`
   - Analyze commit messages, changed files, and modification patterns
   - Identify areas of active development and recent focus

4. **Generate Consolidated Summary**
   - Combine findings from both sources into a cohesive activity report
   - Highlight active development areas and common workflows
   - Provide context for resuming work or understanding team activity

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
```

### 2. Git History Analysis

```bash
# Get recent commit history with details
git log --oneline -3
git log --stat -3 --pretty=format:"%h - %s (%an, %ar)"
```

### 3. Git Status Analysis

```bash
# Show any modified but yet to be commit files
git status --oneline -3
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

**Sessions Found**: [count] sessions
**Date Range**: [earliest timestamp] to [latest timestamp]
**Filter**: [All recent sessions | UUID: {uuid} | Search: {term}]
**Mode**: [Concise summaries | Verbose with full content]

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

## Git History (Last 3 Commits)

### Commit Details

1. `[hash]` - [commit message] ([author], [relative_date])
   **Files Changed**: [count] ([additions/deletions])
   **Key Changes**: [summary of main changes]

2. `[hash]` - [commit message] ([author], [relative_date])
   **Files Changed**: [count] ([additions/deletions])
   **Key Changes**: [summary of main changes]

[Continue for remaining commits...]

## Git Status (uncommited files)

### Status Details

**Files Changed**: [count] ([additions/deletions])
**Key Changes**: [summary of main changes]

### Development Focus Areas

- **[Directory/Component]**: [description of recent changes and activity]
- **[Directory/Component]**: [description of recent changes and activity]

## Consolidated Analysis

### Current Development Focus

[Analysis combining both context bundles, git status and git history to identify main areas of work]

### Most Active Files

[Files that appear frequently in both context bundles, git status and git commits]

1. `[file_path]` - [context: read/write operations + commit changes]
2. `[file_path]` - [context: read/write operations + commit changes]
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
