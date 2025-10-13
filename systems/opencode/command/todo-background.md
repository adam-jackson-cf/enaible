---
description: Build background context for a todo by scanning code and recent activity
---

# Background Opencode

Run a Opencode instance in the background to perform tasks autonomously while you continue working.

## Variables

USER_PROMPT: $1
MODEL: $2 (defaults to `github-copilot/gpt-5-mini` if not provided)
REPORT_FILE: $3 (defaults to './agents/background/background-report-DAY-NAME_HH_MM_SS.md' if not provided)

## Instructions

- Capture timestamp in a variable FIRST to ensure consistency across file creation and references
- Create the initial report file with header BEFORE launching the background agent
- Fire off a new AI CLI instance (Claude Code, Qwen, or Gemini) using the Bash tool with run_in_background=true
- IMPORTANT: Pass the `USER_PROMPT` exactly as provided with no modifications
- Parse the MODEL parameter to determine CLI (claude/qwen/gemini) and model name
- Configure the appropriate CLI with all necessary flags for automated operation
- For Claude Code: Use --print flag, --output-format text, --dangerously-skip-permissions, and --append-system-prompt
- For Qwen/Gemini: Use --prompt flag and --yolo for automated operation (no append-system-prompt support)
- Use all provided CLI flags AS IS. Do not alter them.

## Process

1. **Capture timestamp** - Store current timestamp for consistent file naming
2. **Create report file** - Initialize the report file with header and timestamp
3. **Launch background instance** - Start Claude Code with all required flags
4. **Configure monitoring** - Set up progress tracking and output capture
5. **Confirm launch** - Report successful background task initiation

## Command Structure

```bash
# Capture timestamp for consistency
TIMESTAMP=$(date +"%A_%H_%M_%S")
DEFAULT_REPORT="./agents/background/background-report-${TIMESTAMP}.md"
REPORT_FILE=${3:-$DEFAULT_REPORT}

# Create initial report file
mkdir -p "$(dirname "$REPORT_FILE")"
echo "# Background Task Report - $(date)" > "$REPORT_FILE"
echo "## Task: $1" >> "$REPORT_FILE"
echo "## Started: $(date)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# Launch opencode instance (headless)
opencode run \
  --model "${2:-github-copilot/gpt-5-mini}" \
  --print-logs \
  --log-level "INFO" \
  "$1"
```

## Usage Examples

- `/todo-background "Analyze the codebase for performance issues"` - Uses default `zai-coding-plan/glm-4.5` model and auto-generated report file
- `/todo-background "Refactor the authentication module" anthropic/claude-opus-4-20250514 ./reports/auth-refactor.md` - Uses Claude Opus model with custom report location

## Output

- **Background Process ID** - For monitoring the running task
- **Report File Location** - Where progress updates will be written
- **Task Summary** - Brief description of what was initiated
- **Monitoring Instructions** - How to check progress and results

$ARGUMENTS
