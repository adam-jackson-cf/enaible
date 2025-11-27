# setup-task-lists v0.1

## Purpose

Install and configure Beads (bd) for git-backed persistent task tracking with Claude Code hook integration.

## Variables

### Required

- (none)

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @HOOK_PATH = --hook-path — hook scripts directory (default .claude/hooks)
- @BD_READY_LIMIT = --limit — number of ready tasks to load at SessionStart (default 10)

### Derived (internal)

- @BD_BINARY_PATH = <path> — resolved bd binary location
- @HOOKS_CONFIG_PATH = <path> — hooks configuration file path (.claude/hooks.yaml or similar)
- @SYNC_SCRIPT_PATH = <path> — TodoWrite sync script path

## Instructions

- ALWAYS verify this is a git repository before proceeding.
- NEVER skip git integration prompts during `bd init` without user consent.
- ALWAYS add `.beads/` to `.gitignore` to prevent committing task database.
- Create hooks configuration that loads tasks at SessionStart and syncs completed TodoWrite items.
- Use the exact sync script pattern from the reference implementation.
- Respect STOP confirmations unless @AUTO is provided.

## Workflow

1. Validate prerequisites
   - Run `git rev-parse --is-inside-work-tree`; exit immediately if not a git repository.
   - Check if `bd` binary already installed: `command -v bd`
   - If found, capture version and skip installation step.
2. Install bd binary
   - **STOP (skip when @AUTO):** "Install Beads (bd) binary? (y/n)"
   - Attempt Homebrew installation (macOS/Linux): `brew install steveyegge/beads/bd`
   - If Homebrew unavailable or installation fails, provide manual download instructions:
     - Visit https://github.com/steveyegge/beads/releases
     - Download appropriate binary for platform
     - Move to `~/.local/bin` or `/usr/local/bin`
     - Make executable: `chmod +x <path>/bd`
   - Verify installation: `bd --version`
3. Initialize Beads in project
   - **STOP (skip when @AUTO):** "Run 'bd init' to create .beads/ directory? (y/n)"
   - Run `bd init` (will prompt for git hooks and merge drivers)
   - During init, user will be prompted to configure git integration (hooks, merge driver)
   - Capture initialization output for validation
4. Configure .gitignore
   - Check if `.gitignore` exists; create if missing
   - Search for `.beads/` entry: `grep -q '^\.beads/' .gitignore`
   - If not found, **STOP (skip when @AUTO):** "Add .beads/ to .gitignore? (y/n)"
   - Append `.beads/` to `.gitignore`
5. Create hooks directory
   - Ensure @HOOK_PATH directory exists: `mkdir -p @HOOK_PATH`
   - If hooks configuration file doesn't exist, create it
   - Detect existing hooks config location (.claude/hooks.yaml, .claude/hooks.yml, etc.)
6. Configure SessionStart hook
   - Add or update hooks configuration with SessionStart event:
     ```yaml
     # Load active Beads tasks at session start
     - name: load-bd-tasks
       events:
         - SessionStart
       hooks:
         - type: command
           command: |
             #!/bin/bash
             if command -v bd &> /dev/null; then
               echo "📋 Active Beads Tasks (bd ready):"
               echo ""
               bd ready --limit @BD_READY_LIMIT
               echo ""
               echo "---"
             fi
     ```
   - **STOP (skip when @AUTO):** "Add SessionStart hook to load bd tasks? (y/n)"
7. Create sync script

   - Write sync script to `@HOOK_PATH/sync-todos-to-bd.py`
   - Use the following content (exact implementation from reference):

     ```python
     #!/usr/bin/env python3
     """
     Sync completed TodoWrite items to Beads (bd).

     Extract bd IDs from completed todos and close them.

     Usage: sync-todos-to-bd.py <TOOL_USE_PAYLOAD>
     """
     import json
     import re
     import subprocess
     import sys


     def extract_bd_id(todo_content: str) -> str | None:
         """
         Extract a bd ID from todo content like "[bd-123] Task description".

         Args:
             todo_content: The todo item content string

         Returns
         -------
             bd ID string (e.g., 'bd-123') or None if not found
         """
         match = re.search(r"\[bd-(\d+)\]", todo_content)
         return f"bd-{match.group(1)}" if match else None


     def close_bd_issue(bd_id: str) -> bool:
         """
         Close a bd issue and return success status.

         Args:
             bd_id: The bd issue ID (e.g., 'bd-123')

         Returns
         -------
             True if closed successfully, False otherwise
         """
         try:
             result = subprocess.run(
                 ["bd", "close", bd_id, "--reason", "Completed via TodoWrite"],
                 capture_output=True,
                 text=True,
                 timeout=5,
             )
             return result.returncode == 0
         except Exception as e:
             print(f"Error closing {bd_id}: {e}", file=sys.stderr)
             return False


     def main():
         """Run the TodoWrite → Beads sync hook."""
         if len(sys.argv) < 2:
             # No payload provided, exit silently
             sys.exit(0)

         try:
             # Parse the TodoWrite payload
             payload = json.loads(sys.argv[1])
             todos = payload.get("parameters", {}).get("todos", [])

             closed_count = 0
             for todo in todos:
                 # Only process completed todos
                 if todo.get("status") == "completed":
                     bd_id = extract_bd_id(todo.get("content", ""))
                     if bd_id and close_bd_issue(bd_id):
                         print(f"✓ Closed {bd_id}")
                         closed_count += 1

             if closed_count > 0:
                 print(f"\n📝 Synced {closed_count} completed todo(s) to Beads")

         except json.JSONDecodeError as e:
             print(f"Error parsing payload JSON: {e}", file=sys.stderr)
             sys.exit(0)  # Don't block TodoWrite on errors
         except Exception as e:
             print(f"Error syncing todos: {e}", file=sys.stderr)
             sys.exit(0)  # Don't block TodoWrite on errors


     if __name__ == "__main__":
         main()
     ```

   - Make script executable: `chmod +x @HOOK_PATH/sync-todos-to-bd.py`

8. Configure PostToolUse hook
   - Add or update hooks configuration with PostToolUse event:
     ```yaml
     # Sync completed TodoWrite items to Beads
     - name: sync-completed-todos-to-bd
       events:
         - PostToolUse
       matchers:
         - TodoWrite
       hooks:
         - type: command
           command: |
             #!/bin/bash
             python3 @HOOK_PATH/sync-todos-to-bd.py "$TOOL_USE_PAYLOAD"
     ```
   - **STOP (skip when @AUTO):** "Add PostToolUse hook to sync completed todos? (y/n)"
9. Update CLAUDE.md

   - Add or update Beads documentation section:

     ```md
     ### Beads (bd) - Task Tracking

     **When to use Beads:**

     - Multi-session work that needs to persist beyond current session
     - Tracked deliverables the user wants visibility into
     - Tasks with dependencies or blockers
     - Work that should be discoverable in future sessions

     **When NOT to use Beads (just use TodoWrite):**

     - Single-session tasks
     - Implementation steps within a larger tracked bd task
     - Quick fixes or explorations

     **Workflow:**

     1. At session start: Check `bd ready` for pending tasks
     2. When planning multi-session work: `bd create "Task description"` to get ID
     3. In TodoWrite: Use `[bd-xxx] Step description` to link steps to bd task
     4. On completion: Completed TodoWrite items with bd IDs auto-close via hook

     **Commands:** `bd ready`, `bd show <id>`, `bd create "<title>"`, `bd close <id>`, `bd list --label <name>`
     ```

10. Validate setup
    - Verify bd binary accessible: `bd --version`
    - Check `.beads/` directory exists
    - Verify `.beads/` in `.gitignore`
    - Test hooks configuration syntax (if validation available)
    - Run `bd list` to confirm database initialized
    - Provide instructions to test: create a task with `bd create "Test task"`, then run `bd ready`

## Output

```md
# RESULT

- Summary: Beads (bd) installed and configured with Claude Code hooks integration

## DETAILS

- Binary: bd @BD_BINARY_PATH (version: <version>)
- Database: .beads/ (added to .gitignore)
- Hooks: @HOOKS_CONFIG_PATH
  - SessionStart: load-bd-tasks (limit: @BD_READY_LIMIT)
  - PostToolUse: sync-completed-todos-to-bd
- Sync Script: @SYNC_SCRIPT_PATH (executable)
- Documentation: CLAUDE.md updated

## VALIDATION

- bd binary: ✓ Installed and accessible
- .beads/ directory: ✓ Created
- .gitignore: ✓ Contains .beads/
- Hooks config: ✓ SessionStart and PostToolUse configured
- Sync script: ✓ Created and executable

## NEXT STEPS

1. Create a test task: `bd create "Test Beads integration"`
2. View ready tasks: `bd ready`
3. In Claude Code session, verify tasks appear at SessionStart
4. Create TodoWrite item with `[<issue-id>] Test Beads integration` format (use actual issue ID from step 1)
5. Complete the todo and verify bd auto-closes the task
```

$ARGUMENTS
