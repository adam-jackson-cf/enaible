"""Tests for the Enaible install command."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

os.environ.setdefault("ENAIBLE_SKIP_DEPENDENCY_CHECKS", "1")

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


def test_install_merges_rules_into_claude_md(tmp_path: Path) -> None:
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
    claude_md = tmp_path / "CLAUDE.md"
    assert claude_md.exists()
    content = claude_md.read_text(encoding="utf-8")
    assert "**CRITICAL** Must follow Design Principles" in content
    rules = tmp_path / ".claude" / "rules" / "global.claude.rules.md"
    assert not rules.exists()


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


def test_install_idempotent_claude_md(tmp_path: Path) -> None:
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
    claude_md = tmp_path / "CLAUDE.md"
    original = claude_md.read_text(encoding="utf-8")

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
    assert claude_md.read_text(encoding="utf-8") == original


def test_merge_creates_folder_backup_not_per_file(tmp_path: Path) -> None:
    """Verify MERGE mode creates a folder-level backup, not per-file .bak siblings."""
    target = tmp_path
    claude_dir = target / ".claude"
    commands_dir = claude_dir / "commands"
    commands_dir.mkdir(parents=True)

    # Create existing managed file that will be overwritten
    sentinel = "<!-- ENAIBLE_MANAGED_FILE -->"
    existing_file = commands_dir / "analyze-security.md"
    existing_file.write_text(f"{sentinel}\nold content", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(target),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    # Verify folder-level backup was created (not per-file .bak)
    backups = list(target.glob(".claude.bak*"))
    assert backups, "Expected a folder-level backup to be created"
    backup_root = backups[0]
    assert backup_root.is_dir(), "Backup should be a directory"
    assert (backup_root / "commands" / "analyze-security.md").exists(), (
        "Backup should contain original files"
    )

    # Verify NO per-file .bak siblings were created
    bak_files = list(claude_dir.rglob("*.bak"))
    assert not bak_files, f"Should not create per-file .bak files, found: {bak_files}"


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

    # A backup snapshot should have been created via copy (not move), path may be timestamped
    backups = list(target.glob(".codex.bak*"))
    assert backups, "Expected a backup copy of .codex to be created"
    # Backup should contain the original unmanaged files
    backup_root = backups[0]
    assert (backup_root / "auth.json").read_text(encoding="utf-8") == "keepme"
    assert (backup_root / "sessions" / "history.jsonl").read_text(
        encoding="utf-8"
    ) == "events"


def test_claude_code_merges_rules_into_project_root_claude_md(tmp_path: Path) -> None:
    """Verify claude-code install merges rules into project root CLAUDE.md."""
    target = tmp_path

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(target),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    # Rules should ALSO be merged into project root CLAUDE.md
    claude_md = target / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md should be created in project root"
    content = claude_md.read_text(encoding="utf-8")
    assert "AI-Assisted Workflows" in content, "CLAUDE.md should contain merged rules"


def test_claude_code_appends_to_existing_claude_md(tmp_path: Path) -> None:
    """Verify claude-code install appends rules to existing CLAUDE.md."""
    target = tmp_path

    # Create existing CLAUDE.md with user content
    existing_claude_md = target / "CLAUDE.md"
    existing_claude_md.write_text(
        "# My Project\n\nCustom instructions here.\n", encoding="utf-8"
    )

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(target),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    # CLAUDE.md should contain both original content and merged rules
    content = existing_claude_md.read_text(encoding="utf-8")
    assert "# My Project" in content, "Original content should be preserved"
    assert "Custom instructions here." in content, (
        "Original content should be preserved"
    )
    assert "AI-Assisted Workflows" in content, "Merged rules should be appended"
    assert "---" in content, (
        "Separator should be added between original and merged content"
    )


def test_claude_code_user_scope_places_claude_md_in_dot_claude(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """User-scope installs should merge CLAUDE.md inside ~/.claude."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--scope",
            "user",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    claude_dir = home / ".claude"
    claude_md = claude_dir / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md should be written inside ~/.claude"
    assert not (home / "CLAUDE.md").exists(), (
        "Installer must not place CLAUDE.md at the home directory root"
    )


def test_install_update_mode_skips_unmanaged_files(tmp_path: Path) -> None:
    """Verify UPDATE mode skips files that don't exist or aren't managed."""
    destination = tmp_path / ".claude" / "commands"
    destination.mkdir(parents=True)

    # Create unmanaged file
    unmanaged_file = destination / "custom-command.md"
    unmanaged_file.write_text("custom", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "update",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    # Unmanaged file should be skipped
    assert "Skipped" in result.stdout
    assert unmanaged_file.read_text(encoding="utf-8") == "custom"


def test_install_fresh_mode_clears_destination(tmp_path: Path) -> None:
    """Verify FRESH mode clears destination (except codex)."""
    destination = tmp_path / ".claude"
    destination.mkdir(parents=True)
    existing_file = destination / "old-file.md"
    existing_file.write_text("old", encoding="utf-8")

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "fresh",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    # Old file should be removed
    assert not existing_file.exists()
    # New managed files should exist
    assert (destination / "commands").exists()


def test_install_dry_run_no_backup_created(tmp_path: Path) -> None:
    """Verify dry run doesn't create backups."""
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
    backups = list(tmp_path.glob(".claude.bak*"))
    assert not backups, "Dry run should not create backups"


def test_install_no_backup_flag_skips_backup(tmp_path: Path) -> None:
    """Verify --no-backup flag skips backup creation."""
    destination = tmp_path / ".claude"
    destination.mkdir(parents=True)

    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-backup",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    backups = list(tmp_path.glob(".claude.bak*"))
    assert not backups, "Backup should be skipped with --no-backup"


def test_install_no_sync_shared_skips_workspace_sync(tmp_path: Path) -> None:
    """Verify --no-sync-shared skips workspace synchronization."""
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
            "--no-sync-shared",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout
    # Should complete without errors even if workspace sync is skipped
    assert (tmp_path / ".claude" / "commands").exists()


def test_install_merge_mode_preserves_unmanaged(tmp_path: Path) -> None:
    """Verify MERGE mode preserves unmanaged files."""
    destination = tmp_path / ".claude" / "commands"
    destination.mkdir(parents=True)
    unmanaged = destination / "custom.md"
    unmanaged.write_text("custom content", encoding="utf-8")

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
    # Unmanaged file should be preserved
    assert unmanaged.exists()
    assert unmanaged.read_text(encoding="utf-8") == "custom content"


def test_copilot_user_scope_uses_vscode_user_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify copilot user scope install uses VS Code user directory."""
    # Mock VS Code user directory to a test location
    vscode_user_dir = tmp_path / "vscode_user"
    vscode_user_dir.mkdir(parents=True)

    # Patch where it's imported in install.py
    with patch(
        "enaible.commands.install.get_vscode_user_dir", return_value=vscode_user_dir
    ):
        result = runner.invoke(
            app,
            [
                "install",
                "copilot",
                "--scope",
                "user",
                "--mode",
                "merge",
                "--no-sync",
                "--dry-run",
            ],
        )
        assert result.exit_code == 0, result.stderr or result.stdout
        # Verify the path resolution uses VS Code user directory
        assert str(vscode_user_dir) in result.stdout


def test_copilot_user_scope_instructions_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify copilot user scope install places instructions file in VS Code user directory."""
    # Mock VS Code user directory to a test location
    vscode_user_dir = tmp_path / "vscode_user"
    vscode_user_dir.mkdir(parents=True)

    # Patch where it's imported in install.py
    with patch(
        "enaible.commands.install.get_vscode_user_dir", return_value=vscode_user_dir
    ):
        result = runner.invoke(
            app,
            [
                "install",
                "copilot",
                "--scope",
                "user",
                "--mode",
                "merge",
                "--no-sync",
            ],
        )
        assert result.exit_code == 0, result.stderr or result.stdout

        instructions_path = vscode_user_dir / "instructions" / "copilot.instructions.md"
        assert instructions_path.exists(), (
            "copilot.instructions.md should be in VS Code instructions directory"
        )
        assert "COPILOT_GLOBAL_RULES_START" in instructions_path.read_text(
            encoding="utf-8"
        )


def test_copilot_project_scope_instructions_in_github_dir(tmp_path: Path) -> None:
    """Verify copilot project scope install places copilot-instructions.md in .github."""
    result = runner.invoke(
        app,
        [
            "install",
            "copilot",
            "--scope",
            "project",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    instructions_path = tmp_path / ".github" / "copilot-instructions.md"
    assert instructions_path.exists(), "copilot-instructions.md should be in .github"
    assert "COPILOT_GLOBAL_RULES_START" in instructions_path.read_text(encoding="utf-8")


def test_claude_code_status_program_is_executable(tmp_path: Path) -> None:
    """Verify claude-code install sets executable permissions on statusline-worktree."""
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

    status_file = tmp_path / ".claude" / "statusline-worktree"
    assert status_file.exists(), "statusline-worktree should be copied"
    assert status_file.is_file(), "statusline-worktree should be a file"

    # Check that file has executable permissions (0o755 = rwxr-xr-x)
    # On Unix systems, check if any execute bit is set
    import stat

    file_mode = status_file.stat().st_mode
    assert file_mode & stat.S_IEXEC != 0, (
        "statusline-worktree should have executable permissions"
    )


def test_claude_code_status_program_dry_run_records_chmod(tmp_path: Path) -> None:
    """Verify dry-run mode records chmod action but doesn't change permissions."""
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

    # Dry run should mention the status file
    assert "statusline-worktree" in result.stdout or "chmod" in result.stdout

    # File should not exist in dry-run mode
    status_file = tmp_path / ".claude" / "statusline-worktree"
    assert not status_file.exists(), "Dry run should not create files"


def test_claude_code_status_program_only_for_claude_code(tmp_path: Path) -> None:
    """Verify executable permissions are only set for claude-code, not other systems."""
    # Install codex (should not process statusline-worktree)
    result = runner.invoke(
        app,
        [
            "install",
            "codex",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--no-sync",
        ],
    )
    assert result.exit_code == 0, result.stderr or result.stdout

    # Codex should not have statusline-worktree
    status_file = tmp_path / ".codex" / "statusline-worktree"
    assert not status_file.exists(), "codex should not have statusline-worktree"
