---
allowed-tools: Bash(git:*), Bash(gh:*), Bash(ls:*), Read, Glob
description: Review recent context bundles and git history for quick orientation
---

# Recent Context Review

Analyze recent activity from context bundles and git history to understand current work and provide quick orientation for continuing development.

## Behavior

This command performs a comprehensive review of recent activity by:

1. **Context Bundle Analysis**

   - Find and analyze context bundles from the last 2 days in `.claude/agents/context_bundles/`
   - Parse JSON files to extract operations, file access patterns, and user objectives
   - Summarize session activity and identify workflow patterns

2. **Git History Review**

   - Retrieve last 5 commits with details using `git log`
   - Analyze commit messages, changed files, and modification patterns
   - Identify areas of active development and recent focus

3. **Generate Consolidated Summary**
   - Combine findings from both sources into a cohesive activity report
   - Highlight active development areas and common workflows
   - Provide context for resuming work or understanding team activity

## Process

### 1. Context Bundle Discovery

```bash
# Find context bundle files from last 2 days
ls -la .claude/agents/context_bundles/ 2>/dev/null | grep -E "$(date +'%a_%d'|tr '[:lower:]' '[:upper:]')|$(date -d 'yesterday' +'%a_%d'|tr '[:lower:]' '[:upper:]')"
```

### 2. Git History Analysis

```bash
# Get recent commit history with details
git log --oneline -5
git log --stat -5 --pretty=format:"%h - %s (%an, %ar)"
```

### 3. Data Analysis and Summary

- Parse context bundle JSON files for operation patterns
- Extract file access frequencies and modification types
- Identify command usage patterns and user objectives
- Correlate with git history for comprehensive view

## Output Format

```markdown
# Recent Activity Summary

## Context Bundles (Last 2 Days)

**Sessions Found**: [count] sessions across [count] files
**Date Range**: [earliest timestamp] to [latest timestamp]
**Total Operations**: [count] captured actions

### File Operations Summary

- **Most Accessed**:
  - `[file_path]` ([count] operations)
  - `[file_path]` ([count] operations)
- **Recent Edits**: [list of files modified via Write/Edit operations]
- **Files Read**: [list of files accessed via Read operations]

### Commands Executed

- **Build/Test Commands**: [frequently used build/test commands]
- **Git Operations**: [git commands with frequency]
- **Analysis Commands**: [analysis/debugging commands used]
- **Other**: [miscellaneous bash commands]

### Session Patterns

- **Common Workflows**: [identified patterns in operation sequences]
- **User Objectives**: [summary of goals extracted from prompts]
- **Tools Used**: [Task tool usage, agents invoked, etc.]

## Git History (Last 5 Commits)

### Commit Details

1. `[hash]` - [commit message] ([author], [relative_date])
   **Files Changed**: [count] ([additions/deletions])
   **Key Changes**: [summary of main changes]

2. `[hash]` - [commit message] ([author], [relative_date])
   **Files Changed**: [count] ([additions/deletions])
   **Key Changes**: [summary of main changes]

[Continue for remaining commits...]

### Development Focus Areas

- **[Directory/Component]**: [description of recent changes and activity]
- **[Directory/Component]**: [description of recent changes and activity]

### Commit Patterns

- **Frequency**: [commits per day/author analysis]
- **Types**: [feature additions, bug fixes, refactoring, documentation, etc.]
- **Scope**: [broad changes vs focused modifications]

## Consolidated Analysis

### Current Development Focus

[Analysis combining both context bundles and git history to identify main areas of work]

### Most Active Files

[Files that appear frequently in both context bundles and git commits]

1. `[file_path]` - [context: read/write operations + commit changes]
2. `[file_path]` - [context: read/write operations + commit changes]

### Observed Workflows

[Patterns identified from operation sequences and commit patterns]

- **Development Cycle**: [typical sequence of operations observed]
- **Testing Approach**: [how testing fits into the workflow]
- **Documentation**: [documentation update patterns]

### Recommendations for Continuation

[Actionable suggestions based on recent activity patterns]

- **Immediate Focus**: [areas that need attention based on recent work]
- **Pending Tasks**: [work that appears to be in progress]
- **Quality Gates**: [testing/validation that should be run]

## Notes

- Context bundles require the `/setup-context-capture enable` command to be run first
- Analysis covers only captured operations; some work may occur outside Claude sessions
- Git history provides the authoritative record of committed changes
```

## Usage Examples

```bash
# Get recent activity summary
/todo-recent-context

# Review recent work after returning from break
/todo-recent-context

# Understand team activity on shared project
/todo-recent-context
```

$ARGUMENTS
