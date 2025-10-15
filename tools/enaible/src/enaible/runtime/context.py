"""Workspace discovery utilities for the Enaible CLI."""

from __future__ import annotations

import os
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import typer

_SHARED_SENTINEL = Path("shared/core/base/analyzer_registry.py")


@dataclass(frozen=True)
class WorkspaceContext:
    """Resolved workspace paths required by the CLI."""

    repo_root: Path
    shared_root: Path
    artifacts_root: Path


def _env_path(*keys: str) -> Path | None:
    for key in keys:
        value = os.getenv(key)
        if value:
            candidate = Path(value).expanduser().resolve()
            if candidate.exists():
                return candidate
    return None


def _candidate_roots(start: Path) -> Iterable[Path]:
    yield start
    yield from start.parents

    package_relative = Path(__file__).resolve()
    yield from package_relative.parents


def _find_repo_root(start: Path | None = None) -> Path:
    env_repo = _env_path("ENAIBLE_REPO_ROOT")
    if env_repo is not None and (env_repo / _SHARED_SENTINEL).exists():
        return env_repo

    search_start = (start or Path.cwd()).resolve()
    for candidate in _candidate_roots(search_start):
        if (candidate / _SHARED_SENTINEL).exists():
            return candidate

    raise typer.BadParameter(
        "Unable to locate repository root; set ENAIBLE_REPO_ROOT or run inside a checkout."
    )


def _resolve_artifacts_root(repo_root: Path) -> Path:
    artifacts = _env_path("ENAIBLE_ARTIFACTS_DIR", "ENAIBLE_ARTIFACTS_ROOT")
    if artifacts is None:
        artifacts = repo_root / ".enaible"
    artifacts.mkdir(parents=True, exist_ok=True)
    return artifacts


def load_workspace(start: Path | None = None) -> WorkspaceContext:
    """Resolve workspace paths and ensure shared modules are importable."""
    repo_root = _find_repo_root(start)
    shared_root = repo_root / "shared"
    if not shared_root.exists():
        raise typer.BadParameter(
            f"Shared analyzers folder missing at {shared_root}; repository may be incomplete."
        )

    artifacts_root = _resolve_artifacts_root(repo_root)

    if str(shared_root) not in sys.path:
        sys.path.insert(0, str(shared_root))

    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    if str(shared_root) not in existing_pythonpath.split(os.pathsep):
        os.environ[
            "PYTHONPATH"
        ] = f"{str(shared_root)}{os.pathsep}{existing_pythonpath}".strip(os.pathsep)

    return WorkspaceContext(
        repo_root=repo_root,
        shared_root=shared_root,
        artifacts_root=artifacts_root,
    )
