# Keybinds

## Overview

opencode provides customizable keybinds that can be configured in the `opencode.json` configuration file. The configuration allows users to modify keyboard shortcuts for various application functions.

## Leader Key

The leader key is a central concept in opencode's keybind system. By default, `ctrl+x` serves as the leader key. Most actions require pressing the leader key first, followed by a specific shortcut.

Example:

- To start a new session: Press `ctrl+x`, then press `n`

## Configuration Example

```json
{
  "$schema": "https://opencode.ai/config.json",
  "keybinds": {
    "leader": "ctrl+x",
    "app_help": "<leader>h",
    "app_exit": "ctrl+c,<leader>q",
    "editor_open": "<leader>e"
    // ... other keybinds
  }
}
```

## Disabling Keybinds

To disable a specific keybind, set its value to "none" in the configuration:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "keybinds": {
    "session_compact": "none"
  }
}
```

The configuration supports a wide range of actions, including:

- Application controls
- Session management
- Message navigation
- Model and agent selection
- Input handling

Users can customize these keybinds to suit their workflow and avoid conflicts with existing terminal shortcuts.

## Source

Extracted from https://opencode.ai/docs/keybinds/ on 2025-09-10
