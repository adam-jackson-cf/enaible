"""Tests for the `enaible doctor` command."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from typer.testing import CliRunner

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from enaible import app  # noqa: E402

runner = CliRunner()


def test_doctor_json_output() -> None:
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["checks"]["workspace"] is True
    assert payload["checks"]["schema_exists"] is True
    assert payload["checks"]["analyzer_registry"] is True


def test_doctor_text_output(tmp_path: Path) -> None:
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Enaible Diagnostics" in result.stdout
    assert "Workspace: OK" in result.stdout
