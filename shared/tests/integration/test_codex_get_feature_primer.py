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
@pytest.mark.timeout(600)
def test_codex_get_feature_primer_fixture(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[3]
    report_out = repo_root / "shared/tests/integration/fixtures/scout/report.md"
    # Cleanup: ensure previous runs don't leave stale reports behind.
    report_out.unlink(missing_ok=True)

    script = repo_root / "shared/tests/integration/fixtures/run-get-feature-primer.sh"
    assert script.exists(), f"Missing fixture script: {script}"

    if not (_which("cdx-exec") or _which("codex")):
        pytest.skip("Codex CLI not installed; skipping")

    cmd = shlex.quote(str(script))
    result = _run(cmd, cwd=str(repo_root))
    assert (
        result.returncode == 0
    ), f"Inspect fixture failed (exit {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    assert report_out.exists(), "Inspect report output not created"
    assert report_out.stat().st_size > 0, "Inspect report output is empty"
