---
description: Fires off a full Claude Code instance in the background
argument-hint: [prompt] [model:claude:sonnet|claude:opus|qwen|gemini] [report-file]
allowed-tools: Bash, BashOutput, Read, Edit, MultiEdit, Write, Grep, Glob, WebFetch, WebSearch, TodoWrite, Task
---

# Background Claude Code

Run a Claude Code instance in the background to perform tasks autonomously while you continue working.

## Variables

USER_PROMPT: $1
MODEL: $2 (defaults to 'claude:sonnet' if not provided, format: 'claude:model' or just 'qwen'/'gemini' e.g. claude:opus, qwen, gemini)
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

# Parse CLI and model from argument
IFS=':' read -r CLI MODEL_NAME <<< "${2:-claude:sonnet}"

# Launch appropriate CLI instance based on selection
case "$CLI" in
  claude)
    claude --model "${MODEL_NAME:-sonnet}" \
      --output-format text \
      --dangerously-skip-permissions \
      --append-system-prompt "Report all progress and results to: $REPORT_FILE. Use Write tool to append updates." \
      --print "$1"
    ;;
  qwen)
    # For qwen, prepend report instructions to the prompt since no append-system-prompt support
    ENHANCED_PROMPT="$1

IMPORTANT: Report all progress and results to: $REPORT_FILE using the Write tool to append updates."
    qwen --yolo \
      --prompt "$ENHANCED_PROMPT"
    ;;
  gemini)
    # For gemini, prepend report instructions to the prompt since no append-system-prompt support
    ENHANCED_PROMPT="$1

IMPORTANT: Report all progress and results to: $REPORT_FILE using the Write tool to append updates."
    gemini --yolo \
      --prompt "$ENHANCED_PROMPT"
    ;;
  *)
    echo "Error: Unknown CLI '$CLI'. Use claude:sonnet, claude:opus, qwen, or gemini."
    exit 1
    ;;
esac
```

## Usage Examples

- `/todo-background "Analyze the codebase for performance issues"` - Uses default claude:sonnet model and auto-generated report file
- `/todo-background "Refactor the authentication module" claude:opus ./reports/auth-refactor.md` - Uses Claude Opus model with custom report location
- `/todo-background "Run security audit and create remediation plan" qwen` - Uses Qwen CLI with default report location
- `/todo-background "Generate API documentation" gemini ./reports/api-docs.md` - Uses Gemini CLI with custom report location

## Output

- **Background Process ID** - For monitoring the running task
- **Report File Location** - Where progress updates will be written
- **Task Summary** - Brief description of what was initiated
- **Monitoring Instructions** - How to check progress and results

$ARGUMENTS
