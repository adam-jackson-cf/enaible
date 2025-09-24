---
allowed-tools: Write, Edit, Read, Bash(python:*), Bash(chmod:*), Bash(ls:*), Bash(cat:*)
description: >
Setup OpenCode context capture hooks for session history bundling, captures - tool executions, user prompts, session starts
- Stores JSON bundles in `.opencode/agents/context_bundles/`
- Configure in `.opencode/hooks/context_capture_config.json` (exclusions, truncation, redaction, retention)
---

# Setup Context Capture

Configure OpenCode to persist context bundles for every session by installing the context capture plugin and Python scripts.

## Script Integration

**FIRST - Resolve SCRIPT_PATH:**

1. **Try project-level .opencode folder**:

   ```bash
   Glob: ".opencode/scripts/setup/context/*.py"
   ```

2. **Try user-level .opencode folder**:

   ```bash
   Bash: ls "$HOME/.config/opencode/scripts/setup/context/"
   ```

3. **Interactive fallback if not found**:
   - List searched locations: `.opencode/scripts/setup/context/` and `$HOME/.config/opencode/scripts/setup/context/`
   - Ask user: "Could not locate context setup scripts. Please provide full path to the scripts directory:"
   - Validate provided path contains expected scripts (context_bundle_capture_opencode.py, context_capture_base.py, etc.)
   - Set SCRIPT_PATH to user-provided location

**Pre-flight environment check (fail fast if imports not resolved):**

```bash
SCRIPTS_ROOT="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
PYTHONPATH="$SCRIPTS_ROOT" python -c "from shared.setup.context.context_capture_base import ContextCaptureRunner; print('env OK')"
```

**THEN - Copy files to hooks and plugin directories:**

```bash
# Create directories
mkdir -p "$OPENCODE_PROJECT_DIR/.opencode/hooks"
mkdir -p "$OPENCODE_PROJECT_DIR/.opencode/plugin"

# Copy capture script, base module, redactor, and config from deployed location
cp "$SCRIPTS_ROOT/setup/context/context_capture_base.py" "$OPENCODE_PROJECT_DIR/.opencode/hooks/"
cp "$SCRIPTS_ROOT/setup/context/context_bundle_capture_opencode.py" "$OPENCODE_PROJECT_DIR/.opencode/hooks/"
cp "$SCRIPTS_ROOT/setup/context/sensitive_data_redactor.py" "$OPENCODE_PROJECT_DIR/.opencode/hooks/"
cp "$SCRIPTS_ROOT/setup/context/context_capture_config.json" "$OPENCODE_PROJECT_DIR/.opencode/hooks/"

# Copy plugin file
cp "$SCRIPTS_ROOT/opencode/plugins/context-capture.ts" "$OPENCODE_PROJECT_DIR/.opencode/plugin/"

# Make scripts executable
chmod +x "$OPENCODE_PROJECT_DIR/.opencode/hooks/context_bundle_capture_opencode.py"
chmod +x "$OPENCODE_PROJECT_DIR/.opencode/hooks/sensitive_data_redactor.py"
```

$ARGUMENTS
