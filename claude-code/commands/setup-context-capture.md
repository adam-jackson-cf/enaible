---
allowed-tools: Write, Edit, Read, Bash(python:*), Bash(chmod:*), Bash(ls:*), Bash(cat:*)
argument-hint: [enable|disable|status]
description: Setup session context capture for improved continuity
---

# Setup Context Capture

Configure automatic session action tracking into JSON context bundles for improved session continuity and debugging.

Users can customize the capture behavior by editing the deployed `context_capture_config.json` file to add or remove exclusions, adjust truncation limits, or modify the bundle size threshold.

## Script Integration

**FIRST - Resolve SCRIPT_PATH:**

1. **Try project-level .claude folder**:

   ```bash
   Glob: ".claude/scripts/setup/context/*.py"
   ```

2. **Try user-level .claude folder**:

   ```bash
   Bash: ls "$HOME/.claude/scripts/setup/context/"
   ```

3. **Interactive fallback if not found**:
   - List searched locations: `.claude/scripts/setup/context/` and `$HOME/.claude/scripts/setup/context/`
   - Ask user: "Could not locate context setup scripts. Please provide full path to the scripts directory:"
   - Validate provided path contains expected scripts (context_bundle_capture.py, context_capture_config.json)
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname \"$SCRIPT_PATH\")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "import core.base; print('env OK')"
```

**THEN - Copy files to hooks directory:**

```bash
# Create hooks directory
mkdir -p "$CLAUDE_PROJECT_DIR/.claude/hooks"

# Copy capture script, redaction module, and config from deployed location
cp "$SCRIPTS_ROOT/setup/context/context_bundle_base.py" "$CLAUDE_PROJECT_DIR/.claude/hooks/"
cp "$SCRIPTS_ROOT/setup/context/context_bundle_capture_claude.py" "$CLAUDE_PROJECT_DIR/.claude/hooks/"
cp "$SCRIPTS_ROOT/setup/context/sensitive_data_redactor.py" "$CLAUDE_PROJECT_DIR/.claude/hooks/"
cp "$SCRIPTS_ROOT/setup/context/context_capture_config.json" "$CLAUDE_PROJECT_DIR/.claude/hooks/"

# Make scripts executable
chmod +x "$CLAUDE_PROJECT_DIR/.claude/hooks/context_bundle_capture_claude.py"
chmod +x "$CLAUDE_PROJECT_DIR/.claude/hooks/sensitive_data_redactor.py"
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
