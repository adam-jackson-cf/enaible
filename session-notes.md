# Session Notes — Ghostty default 3‑pane layout

Date: 2025-10-13

Changes applied to ensure Ghostty loads with a 3‑pane layout by default and to prevent the duplicate-splitting bug when launching Ghostty from within Ghostty.

## What changed

- Updated Ghostty config to avoid restoring prior window state (prevents re-splitting on next launch):
  - File: `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config`
  - Set `window-save-state = never` (was `always`).
- Kept `initial-command` but refined the layout script to target the newest Ghostty window explicitly and equalize splits at the end:
  - File: `/Users/adamjackson/.ghostty/claude-layout.sh`
  - Focuses the newest window (AXRaise/AXMain/AXFocused) before sending split keystrokes.
  - Performs: right split → run `lazygit` → focus left → create bottom-left split → focus top-left → equalize splits.
  - Guards with `GHOSTTY_LAYOUT_DONE` to avoid recursion.

Backups created:

- `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config.backup.20251013-143614`
- `/Users/adamjackson/.ghostty/claude-layout.sh.backup.20251013-143614`

## How it works

- Ghostty launches and runs `initial-command`, which calls the layout script once.
- The script selects the newest Ghostty window and issues the split sequence via Accessibility.
- `window-save-state = never` ensures startup is always the same 3‑pane layout instead of restoring prior sessions.

## Permissions

This uses `System Events` for UI scripting. If macOS prompts for Accessibility permissions, enable Ghostty (and/or your shell host) in:

System Settings → Privacy & Security → Accessibility.

## Rollback

- To restore previous behavior: set `window-save-state = always` in `/Users/adamjackson/Library/Application Support/com.mitchellh.ghostty/config` and, if desired, replace the layout script with the backup noted above.

## Optional follow-ups

- Add a shell alias to open a fresh 3‑pane window on demand:

  - Example alias in `~/.zshrc`:
    `alias g3='open -na Ghostty.app'`
  - Then hit `Cmd+N` to create a window and run `g3` for a separate instance if you want another default 3‑pane layout.

---

# Installer Notes — Codex CLI

Date: 2025-10-13

Fixed an installation path bug in the Codex installers where the Python framework was looked up at `systems/shared/` instead of the repository-level `shared/` directory.

What changed

- systems/codex/install.sh: in `copy_python_framework()`, changed the shared root resolution from `$(cd "$SCRIPT_DIR/.." && pwd)/shared` to `$(cd "$SCRIPT_DIR/../.." && pwd)/shared` (two levels up from `systems/codex/`).
- systems/codex/install.ps1: compute `$repoRoot` two levels up with `Split-Path (Split-Path $ScriptDir -Parent) -Parent` and set `$sharedRoot = Join-Path $repoRoot 'shared'`. Also improved the error message to print the full missing path.

Verification

- Ran `./systems/codex/install.sh --dry-run --verbose` and confirmed Phase [5/11] "Copy Python framework" now resolves correctly and proceeds. Dry-run succeeded end-to-end.

Impact

- Addresses the error: `Missing shared subtree: /.../systems/shared/core` observed during step [5/11] of the installer.
