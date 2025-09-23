---
description: Install and manage Opencode context capture hooks backed by Python bundling scripts
---

# setup-context-capture

Configure Opencode to persist context bundles for every session by wiring runtime hooks to the existing Python capture stack.

## Overview

Running `opencode setup-context-capture enable` installs the context capture plugin hooks and copies the Python assets into `.opencode/hooks/`. Once enabled, every tool call, session start, and user prompt emits a structured JSON payload to `context_bundle_capture_opencode.py`, producing the same bundle format used in our Claude Code workflow. Bundles link back to full conversations via the session UUID so `/todo-recent-context` can reconstruct recent history.

## Requirements

- The `opencode/plugins/context-capture.ts` plugin must be present in the repository
- Python 3 available on the `PATH` (override with `OPENCODE_PYTHON` if needed)
- `.opencode/hooks/` writable inside the project
- Access to the shared context assets in `shared/setup/context/`

## Command Actions

### 1. Status (default)

```bash
opencode setup-context-capture status
```

- Prints the current enablement state
- Verifies the hook scripts exist under `.opencode/hooks/`
- Displays a reminder if the assets need to be reinstalled

### 2. Enable

```bash
opencode setup-context-capture enable
```

Performs the full installation:

1. Creates `.opencode/hooks/` if necessary
2. Copies the following files from `shared/setup/context/` into `.opencode/hooks/`:
   - `context_capture_base.py`
   - `context_bundle_capture_opencode.py`
   - `sensitive_data_redactor.py`
   - `context_capture_config.json`
3. Marks the Python files as executable (`chmod +x` equivalent)
4. Writes `.opencode/hooks/.context-capture-enabled` to activate the hook bridge

After enabling, the plugin subscribes to:

- `tool.execute.after` → `context_bundle_capture_opencode.py post-tool`
- `session.start` → `context_bundle_capture_opencode.py session-start`
- `user.prompt.submitted` → `context_bundle_capture_opencode.py user-prompt`

Each hook invocation pipes the runtime payload to the Python script via stdin, preserving exclusions, truncation, and redaction logic defined in `context_capture_config.json`.

### 3. Disable

```bash
opencode setup-context-capture disable
```

- Removes the `.context-capture-enabled` marker
- Leaves copied assets in place so re-enabling is instant
- Hooks remain registered but short-circuit until re-enabled

## Verification Checklist

1. Run `opencode setup-context-capture enable`
2. Trigger a few tool commands and prompts inside Opencode
3. Inspect `.opencode/agents/context_bundles/` for freshly written bundle files
4. Optional: run `opencode setup-context-capture status` to confirm the enabled state
5. Use `opencode todo-recent-context --verbose` to consume the generated bundles

## Troubleshooting

- **Missing scripts warning**: Rerun `opencode setup-context-capture enable` to reinstall assets
- **Different Python interpreter**: Set `OPENCODE_PYTHON=/path/to/python` before starting Opencode
- **No bundles written**: Confirm `.context-capture-enabled` exists and that the plugin is loaded (check Opencode startup logs)
- **Custom redaction**: Edit `.opencode/hooks/context_capture_config.json` to adjust exclusions or truncation limits

$ARGUMENTS
