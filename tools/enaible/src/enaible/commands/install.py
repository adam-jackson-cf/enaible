"""System installer command for Enaible CLI."""

from __future__ import annotations

import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import typer

from ..app import app
from ..prompts.adapters import SYSTEM_CONTEXTS, SystemRenderContext
from ..runtime.context import load_workspace

MANAGED_SENTINEL = "<!-- generated: enaible -->"


class InstallMode(str, Enum):
    MERGE = "merge"
    UPDATE = "update"
    SYNC = "sync"
    FRESH = "fresh"


@dataclass(slots=True)
class InstallSummary:
    actions: list[tuple[str, str]]
    skipped: list[str]

    def record(self, action: str, path: Path) -> None:
        self.actions.append((action, path.as_posix()))

    def record_skip(self, path: Path) -> None:
        self.skipped.append(path.as_posix())


@app.command("install")
def install(  # noqa: PLR0912
    system: str = typer.Argument(
        ..., help="System adapter to install (claude-code|opencode|codex)."
    ),
    target: Path = typer.Option(
        Path("."), "--target", "-t", help="Destination root for installation."
    ),
    mode: InstallMode = typer.Option(
        InstallMode.MERGE, "--mode", "-m", case_sensitive=False
    ),
    scope: str = typer.Option(
        "project",
        "--scope",
        "-s",
        help="Installation scope (project|user). Defaults to project-level directories.",
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Preview actions without writing files."
    ),
    backup: bool = typer.Option(
        False,
        "--backup/--no-backup",
        help="Create .bak backups for files that will be overwritten.",
    ),
) -> None:
    """Install rendered system assets into project or user configuration directories."""
    context = load_workspace()
    system_ctx = _get_system_context(system)
    source_root = context.repo_root / "systems" / system
    if not source_root.exists():
        raise typer.BadParameter(f"Source assets missing for system '{system}'.")

    destination_root = _resolve_destination(system_ctx, target, scope)
    summary = InstallSummary(actions=[], skipped=[])

    if mode is InstallMode.FRESH and not dry_run and destination_root.exists():
        shutil.rmtree(destination_root)
        summary.record("remove", destination_root)

    files = _iter_source_files(source_root)

    for source_file in files:
        relative = source_file.relative_to(source_root)
        destination_file = destination_root / relative

        managed = _has_managed_sentinel(source_file)
        dest_exists = destination_file.exists()
        dest_managed = (
            _has_managed_sentinel(destination_file) if dest_exists else managed
        )

        if mode is InstallMode.UPDATE and (not dest_exists or not dest_managed):
            summary.record_skip(relative)
            continue

        if (
            mode in {InstallMode.MERGE, InstallMode.SYNC}
            and dest_exists
            and not dest_managed
        ):
            summary.record_skip(relative)
            continue

        if dry_run:
            summary.record("write", destination_file)
            continue

        destination_file.parent.mkdir(parents=True, exist_ok=True)

        if backup and dest_exists:
            backup_path = destination_file.with_suffix(destination_file.suffix + ".bak")
            shutil.copy2(destination_file, backup_path)
            summary.record("backup", backup_path)

        shutil.copy2(source_file, destination_file)
        summary.record("write", destination_file)

    _emit_summary(system, destination_root, mode, summary, dry_run)


def _iter_source_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_file():
            yield path


def _resolve_destination(
    system_ctx: SystemRenderContext, target: Path, scope: str
) -> Path:
    if scope.lower() == "user":
        return Path(system_ctx.user_scope_dir).expanduser()
    if scope.lower() != "project":  # pragma: no cover - input validation
        raise typer.BadParameter("Scope must be either 'project' or 'user'.")
    return (target / system_ctx.project_scope_dir).resolve()


def _has_managed_sentinel(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8") as handle:
            for _ in range(5):
                line = handle.readline()
                if not line:
                    break
                if MANAGED_SENTINEL in line:
                    return True
    except UnicodeDecodeError:  # pragma: no cover - binary safety
        return False
    return False


def _emit_summary(
    system: str,
    destination_root: Path,
    mode: InstallMode,
    summary: InstallSummary,
    dry_run: bool,
) -> None:
    action_label = "Planned" if dry_run else "Completed"
    typer.echo(
        f"{action_label} Enaible install for {system} ({mode.value}) → {destination_root}"
    )
    if summary.actions:
        for action, rel_path in summary.actions:
            typer.echo(f"  {action:8} {rel_path}")
    else:
        typer.echo("  No changes required.")

    if summary.skipped:
        typer.echo("  Skipped (unmanaged or missing targets):")
        for rel_path in summary.skipped:
            typer.echo(f"    - {rel_path}")


def _get_system_context(system: str) -> SystemRenderContext:
    try:
        return SYSTEM_CONTEXTS[system]
    except KeyError as exc:  # pragma: no cover - input validation
        available = ", ".join(sorted(SYSTEM_CONTEXTS.keys()))
        raise typer.BadParameter(
            f"Unknown system '{system}'. Available adapters: {available}."
        ) from exc
