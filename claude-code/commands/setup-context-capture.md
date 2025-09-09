---
allowed-tools: Write, Edit, Read, Bash(python:*), Bash(chmod:*), Bash(ls:*), Bash(cat:*)
argument-hint: [enable|disable|status]
description: Setup session context capture for improved continuity
---

# Setup Context Capture

Configure automatic session action tracking into JSON context bundles for improved session continuity and debugging.

## Behavior

Based on argument provided:

- **enable**: Create capture script and configure hooks
- **disable**: Remove hooks from settings (keep script)
- **status**: Show current configuration and recent captures

## Implementation

The command will create a Python script at `$CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_capture.py` and configure Claude Code hooks to automatically capture key session events into daily JSON files stored in `.claude/agents/context_bundles/`.

### Context Bundle Format

Files are named using the format: `DAY_DD_UUID.json` (e.g., `SAT_14_a1b2c3d4.json`)

Each file contains an array of captured actions:

```json
[
  {
    "operation": "read",
    "timestamp": "2024-12-14T10:30:45.123Z",
    "file_path": "/path/to/file.py",
    "tool_input": {
      /* full tool parameters */
    }
  },
  {
    "operation": "bash",
    "timestamp": "2024-12-14T10:31:02.456Z",
    "command": "git status",
    "description": "Check git status"
  },
  {
    "operation": "prompt",
    "timestamp": "2024-12-14T10:31:15.789Z",
    "prompt": "User's input text..."
  }
]
```

### Captured Events

- **Tool Operations**: Read, Write, Edit, MultiEdit, Bash, Task, Grep, Glob
- **User Prompts**: Full prompt submissions
- **Session Lifecycle**: Session start markers

### Script Creation

When enabled, creates the following capture script:

```python
#!/usr/bin/env python3
"""Context bundle capture for Claude Code session tracking."""
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import uuid

# Session UUID persisted in temp file
SESSION_UUID_FILE = Path.home() / ".claude" / ".current_session_uuid"

def get_session_uuid():
    """Get or create session UUID."""
    if SESSION_UUID_FILE.exists():
        return SESSION_UUID_FILE.read_text().strip()
    new_uuid = str(uuid.uuid4())[:8]
    SESSION_UUID_FILE.parent.mkdir(exist_ok=True)
    SESSION_UUID_FILE.write_text(new_uuid)
    return new_uuid

def capture_action(event_type):
    """Capture action based on event type."""
    try:
        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Create context bundle directory
        project_dir = os.environ.get('CLAUDE_PROJECT_DIR', '.')
        bundle_dir = Path(project_dir) / '.claude' / 'agents' / 'context_bundles'
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename: DAY_DD_UUID.json
        now = datetime.now()
        day_name = now.strftime('%a').upper()[:3]  # MON, TUE, etc.
        day_num = now.strftime('%d')
        session_id = get_session_uuid()
        filename = f"{day_name}_{day_num}_{session_id}.json"
        bundle_file = bundle_dir / filename

        # Load existing or create new
        if bundle_file.exists():
            with open(bundle_file, 'r') as f:
                entries = json.load(f)
        else:
            entries = []

        # Create entry based on event type
        entry = {
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }

        # Add context based on event
        if event_type == "post-tool":
            tool_name = data.get('tool_name', '').lower()
            entry["operation"] = tool_name

            # Capture key tool inputs
            if 'tool_input' in data:
                tool_input = data['tool_input']

                # File operations
                if 'file_path' in tool_input:
                    entry["file_path"] = tool_input['file_path']

                # Bash commands
                if tool_name == 'bash' and 'command' in tool_input:
                    entry["command"] = tool_input['command']
                    if 'description' in tool_input:
                        entry["description"] = tool_input['description']

                # Store full input for reference
                entry["tool_input"] = tool_input

        elif event_type == "user-prompt":
            entry["operation"] = "prompt"
            entry["prompt"] = data.get('prompt', '')[:500]  # Limit length

        elif event_type == "session-start":
            entry["operation"] = "session_start"
            # Reset UUID for new session
            SESSION_UUID_FILE.unlink(missing_ok=True)
            get_session_uuid()  # Generate new one

        # Only add if we have meaningful data
        if len(entry) > 1:  # More than just timestamp
            entries.append(entry)
            with open(bundle_file, 'w') as f:
                json.dump(entries, f, indent=2)

    except Exception as e:
        # Silent fail - don't interrupt Claude's flow
        pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        capture_action(sys.argv[1])
```

### Hook Configuration

When enabled, adds the following hooks to `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Read|Write|Edit|MultiEdit|Bash|Task|Grep|Glob",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_capture.py\" post-tool"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_capture.py\" user-prompt"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_capture.py\" session-start"
          }
        ]
      }
    ]
  }
}
```

$ARGUMENTS
