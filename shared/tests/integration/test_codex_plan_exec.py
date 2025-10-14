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
        env=None,
        check=False,
    )


@pytest.mark.slow
def test_codex_create_execplan_fixture(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    script = repo_root / "shared/tests/integration/fixtures/run-plan-exec.sh"
    assert script.exists(), f"Missing fixture script: {script}"

    if not (_which("cdx-exec") or _which("codex")):
        pytest.skip("Codex CLI not installed; skipping")

    execplan_out = repo_root / "shared/tests/integration/fixtures/plan-exec/execplan.md"
    execplan_out.unlink(missing_ok=True)

    cmd = shlex.quote(str(script))
    result = _run(cmd, cwd=str(repo_root))
    assert (
        result.returncode == 0
    ), f"ExecPlan fixture failed (exit {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert execplan_out.exists(), "ExecPlan output not created"
    assert execplan_out.stat().st_size > 0, "ExecPlan output is empty"
