#!/usr/bin/env python3
"""Lightweight helpers for external CLI tool detection and invocation."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass
class ToolCheck:
    name: str
    available: bool
    path: str | None
    version: str | None = None


def find_cli(candidates: Sequence[str]) -> ToolCheck:
    """Return first available CLI from candidates (e.g., ["semgrep", "npx semgrep"])."""
    for cand in candidates:
        # Support space-separated forms like "npx jscpd"
        if " " in cand:
            exe = cand.split()[0]
            if shutil.which(exe):
                return ToolCheck(name=cand, available=True, path=cand)
        else:
            path = shutil.which(cand)
            if path:
                return ToolCheck(name=cand, available=True, path=path)
    return ToolCheck(
        name=candidates[0] if candidates else "", available=False, path=None
    )


def run_cli(cmd: Sequence[str], timeout: int = 300) -> tuple[int, str, str]:
    """Run a CLI command and return (rc, stdout, stderr)."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout or "", p.stderr or ""
    except subprocess.TimeoutExpired as e:
        return 124, "", str(e)


def auto_install_python_package(package: str, env_flag: str) -> bool:
    """Auto-install a Python package when the opt-in env flag is set."""
    if os.environ.get(env_flag, "").lower() not in {"1", "true", "yes"}:
        return False
    py = shutil.which("python3") or shutil.which("python")
    if not py:
        return False
    try:
        r = subprocess.run(
            [py, "-m", "pip", "install", "--user", package],
            capture_output=True,
            text=True,
            timeout=600,
        )
        return r.returncode == 0
    except Exception:
        return False


def auto_install_npm_packages(packages: Sequence[str], env_flag: str) -> bool:
    """Auto-install npm packages globally when the opt-in env flag is set."""
    if os.environ.get(env_flag, "").lower() not in {"1", "true", "yes"}:
        return False
    npm = shutil.which("npm")
    if not npm:
        return False
    try:
        r = subprocess.run(
            [npm, "install", "-g", *packages],
            capture_output=True,
            text=True,
            timeout=600,
        )
        return r.returncode == 0
    except Exception:
        return False
