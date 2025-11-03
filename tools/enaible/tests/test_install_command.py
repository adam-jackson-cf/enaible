"""Tests for the Enaible install command."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from enaible import app  # noqa: E402
from enaible.runtime.context import WorkspaceContext  # noqa: E402

runner = CliRunner()
REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(autouse=True)
def _patch_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    context = WorkspaceContext(
        repo_root=REPO_ROOT,
        shared_root=REPO_ROOT / "shared",
        artifacts_root=REPO_ROOT / ".enaible",
    )
    monkeypatch.setattr("enaible.commands.install.load_workspace", lambda: context)


def test_install_merge_project_scope(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    destination = tmp_path / ".claude" / "commands" / "analyze-security.md"
    assert destination.exists()


def test_install_copies_agents_and_rules(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    agent = tmp_path / ".claude" / "agents" / "user-researcher.md"
    rules = tmp_path / ".claude" / "rules" / "global.claude.rules.md"
    assert agent.exists()
    assert rules.exists()
    assert agent.read_text(encoding="utf-8").startswith("---")
    assert "Tooling preferences" in rules.read_text(encoding="utf-8")


def test_install_dry_run_leaves_destination_clean(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--dry-run",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    destination = tmp_path / ".claude"
    assert not destination.exists()
    assert "Planned" in result.stdout


def test_install_skips_unmanaged_files(tmp_path: Path) -> None:
    destination = tmp_path / ".claude" / "commands"
    destination.mkdir(parents=True)
    target_file = destination / "analyze-security.md"
    target_file.write_text("custom content", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    assert target_file.read_text(encoding="utf-8") == "custom content"
    assert "Skipped" in result.stdout


def test_install_overwrites_managed_rules(tmp_path: Path) -> None:
    # First install to seed files
    base_result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert base_result.exit_code == 0, base_result.stderr or base_result.stdout
    rules_path = tmp_path / ".claude" / "rules" / "global.claude.rules.md"
    original = rules_path.read_text(encoding="utf-8")
    # Mutate destination to simulate stale content
    rules_path.write_text("outdated", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    assert rules_path.read_text(encoding="utf-8") == original
