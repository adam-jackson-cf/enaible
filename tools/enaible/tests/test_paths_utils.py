"""Tests for path utilities."""

from __future__ import annotations

import os
import platform
from pathlib import Path
from unittest.mock import patch

import pytest

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
import sys  # noqa: E402

if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from enaible.utils.paths import get_vscode_user_dir  # noqa: E402


def test_get_vscode_user_dir_macos(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test VS Code user directory path on macOS."""
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    expected = Path.home() / "Library" / "Application Support" / "Code" / "User"
    assert get_vscode_user_dir() == expected


def test_get_vscode_user_dir_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test VS Code user directory path on Windows."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    appdata = "C:\\Users\\TestUser\\AppData\\Roaming"
    with patch.dict(os.environ, {"APPDATA": appdata}):
        expected = Path(appdata) / "Code" / "User"
        assert get_vscode_user_dir() == expected


def test_get_vscode_user_dir_windows_missing_appdata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test VS Code user directory path on Windows when APPDATA is missing."""
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(RuntimeError, match="APPDATA environment variable"):
            get_vscode_user_dir()


def test_get_vscode_user_dir_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test VS Code user directory path on Linux."""
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    expected = Path.home() / ".config" / "Code" / "User"
    assert get_vscode_user_dir() == expected


def test_get_vscode_user_dir_unsupported_os(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test VS Code user directory path on unsupported OS."""
    monkeypatch.setattr(platform, "system", lambda: "FreeBSD")
    with pytest.raises(RuntimeError, match="Unsupported operating system"):
        get_vscode_user_dir()


