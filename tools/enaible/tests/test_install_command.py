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


def test_codex_fresh_backup_preserves_existing_unmanaged(tmp_path: Path) -> None:
    target = tmp_path
    codex_dir = target / ".codex"
    (codex_dir / "sessions").mkdir(parents=True, exist_ok=True)
    (codex_dir / "auth.json").write_text("keepme", encoding="utf-8")
    (codex_dir / "sessions" / "history.jsonl").write_text("events", encoding="utf-8")

    # Run fresh install with backup enabled (default)
    result = runner.invoke(
        app,
        [
            "install",
            "codex",
            "--target",
            str(target),
            "--mode",
            "fresh",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    # Original unmanaged files must remain
    assert (codex_dir / "auth.json").read_text(encoding="utf-8") == "keepme"
    assert (codex_dir / "sessions" / "history.jsonl").read_text(
        encoding="utf-8"
    ) == "events"

    # Managed assets should exist after install
    assert (codex_dir / "prompts").exists()
    assert (codex_dir / "rules").exists()

    # A backup snapshot should have been created via copy (not move), path may be timestamped
    backups = list(target.glob(".codex.bak*"))
    assert backups, "Expected a backup copy of .codex to be created"
    # Backup should contain the original unmanaged files
    backup_root = backups[0]
    assert (backup_root / "auth.json").read_text(encoding="utf-8") == "keepme"
    assert (backup_root / "sessions" / "history.jsonl").read_text(
        encoding="utf-8"
    ) == "events"
