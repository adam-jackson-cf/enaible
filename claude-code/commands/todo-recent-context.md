---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(ls:*), Read, Glob
argument-hint: [--uuid UUID] [--verbose]
description: Review recent context bundles and git history for quick orientation
---

# Recent Context Review

Analyze recent activity from context bundles and git history to understand current work and provide quick orientation for continuing development.

## Arguments

- `--uuid UUID` - Filter analysis to a specific session UUID
- `--verbose` - Expand truncated content from linked conversation files (when available)

## Behavior

This command performs a comprehensive review of recent activity by:

1. **Context Bundle Analysis**

   - Find and analyze context bundles from the last 2 days in `.claude/agents/context_bundles/`
   - Filter to specific UUID if `--uuid` provided (pattern: `*_UUID.json`)
   - Parse JSON files to extract operations, file access patterns, and user objectives
   - In `--verbose` mode: expand truncated content from linked conversation JSONL files
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
# Default: Find context bundle files from last 2 days
ls -la .claude/agents/context_bundles/ 2>/dev/null | grep -E "$(date +'%a_%d'|tr '[:lower:]' '[:upper:]')|$(date -d 'yesterday' +'%a_%d'|tr '[:lower:]' '[:upper:]')"

# With --uuid: Filter to specific session
ls -la .claude/agents/context_bundles/*_${UUID}.json 2>/dev/null
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

- Parse context bundle JSON files for operation patterns
- Handle optimized bundles with truncated content and conversation links
- In `--verbose` mode: fetch full content from linked JSONL conversation files
- Extract file access frequencies and modification types (accounting for deduplication)
- Identify command usage patterns and user objectives
- Correlate with git history for comprehensive view

## Output Format

```markdown
# Recent Activity Summary

## Context Bundles Analysis

**Sessions Found**: [count] sessions across [count] files
**Date Range**: [earliest timestamp] to [latest timestamp]
**Filter**: [All recent sessions | UUID: {uuid}]
**Mode**: [Concise summaries | Verbose with full content]

### File Operations Summary

- **Most Accessed**:
  - `[file_path]` (read, edit, write operations)
  - `[file_path]` (read operations only)
- **Recent Edits**: [list of files modified via Write/Edit operations]
- **Files Read**: [list of files accessed via Read operations]
- **Conversation Links**: [sessions with linked JSONL files for full detail]

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
```

$ARGUMENTS
