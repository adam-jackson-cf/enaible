import os
import re
import shlex
import subprocess
from pathlib import Path

import pytest


def _which(cmd: str) -> bool:
    from shutil import which

    return which(cmd) is not None


def _run(cmd: str, cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        text=True,
        capture_output=True,
        env=os.environ.copy(),
        check=False,
    )


ALLOWED_MODES = ("claude", "codex", "opencode", "qwen", "gemini")
SLOW_MODES = {"claude", "qwen", "gemini"}


def _selected_modes():
    raw = os.getenv("TODO_BG_MODES", "codex").strip().lower()
    if raw == "all":
        return list(ALLOWED_MODES)
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    sel = [p for p in parts if p in ALLOWED_MODES]
    return sel or ["codex"]


def _param_modes():
    params = []
    for m in _selected_modes():
        marks = [pytest.mark.slow] if m in SLOW_MODES else []
        params.append(pytest.param(m, id=m, marks=marks))
    return params


@pytest.mark.parametrize("mode", _param_modes())
def test_todo_background_fixture_script_gate_modes(mode: str):
    repo_root = Path(__file__).resolve().parents[3]
    script = repo_root / "shared/tests/integration/fixtures/test-todo-background.sh"
    assert script.exists(), f"Missing fixture script: {script}"

    # Skip if required CLI for mode is not installed
    if mode == "codex" and not (_which("cdx-exec") or _which("codex")):
        pytest.skip("Codex CLI not installed; skipping")
    if mode == "claude" and not _which("claude"):
        pytest.skip("Claude CLI not installed; skipping")
    if mode == "opencode" and not _which("opencode"):
        pytest.skip("OpenCode CLI not installed; skipping")
    if mode == "qwen" and not _which("qwen"):
        pytest.skip("Qwen CLI not installed; skipping")
    if mode == "gemini" and not _which("gemini"):
        pytest.skip("Gemini CLI not installed; skipping")

    # Run the script for the selected mode and capture output
    cmd = f"{shlex.quote(str(script))} {shlex.quote(mode)}"
    result = _run(cmd, cwd=str(repo_root))
    assert (
        result.returncode == 0
    ), f"Script failed (exit {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Extract report path from output (supports success and auth-skip variants)
    m = re.search(r"Report file:\s*(.*)\n", result.stdout)
    if not m:
        m = re.search(r"See report:\s*(.*)\n", result.stdout)
    assert m, f"Could not find report path in output. STDOUT:\n{result.stdout}"
    report_path = Path(m.group(1).strip())
    assert report_path.exists(), f"Report file not created: {report_path}"
    assert report_path.stat().st_size > 0, "Report file is empty"
