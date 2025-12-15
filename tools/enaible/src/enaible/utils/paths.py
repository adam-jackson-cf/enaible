"""Cross-platform path utilities for Enaible CLI."""

from __future__ import annotations

import os
import platform
from pathlib import Path


def get_vscode_user_dir() -> Path:
    """Get VS Code user directory path based on the current operating system.

    Returns:
        Path to VS Code user directory:
        - macOS: ~/Library/Application Support/Code/User/
        - Windows: %APPDATA%\\Code\\User\\
        - Linux: ~/.config/Code/User/

    Raises:
        RuntimeError: If the operating system is not supported.
    """
    system = platform.system().lower()

    if system == "darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Code" / "User"
    elif system == "windows":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not set on Windows")
        return Path(appdata) / "Code" / "User"
    elif system == "linux":
        return Path.home() / ".config" / "Code" / "User"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


