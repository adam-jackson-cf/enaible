"""Root command definitions for Enaible CLI."""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from enum import Enum
from pathlib import Path

import typer

from ..app import app
from ..runtime.context import find_shared_root, load_workspace


class ContextPlatform(str, Enum):
    """Supported context capture platforms."""

    CLAUDE = "claude"
    CODEX = "codex"


class OutputFormat(str, Enum):
    """Output formats supported by context capture scripts."""

    JSON = "json"
    TEXT = "text"


def _env_with_shared(shared_root: Path) -> dict[str, str]:
    """Return environment mapping that ensures shared/ is importable."""
    env = os.environ.copy()
    pythonpath = env.get("PYTHONPATH", "")
    if pythonpath:
        env["PYTHONPATH"] = f"{shared_root}{os.pathsep}{pythonpath}"
    else:
        env["PYTHONPATH"] = str(shared_root)
    return env


@app.command("context_capture")
def context_capture(
    platform: ContextPlatform = typer.Option(
        ...,
        "--platform",
        "-p",
        help="Target platform to capture context for.",
    ),
    days: int = typer.Option(2, help="Number of days to look back."),
    uuid: str | None = typer.Option(None, help="Filter to a specific session UUID."),
    search_term: str | None = typer.Option(
        None, help="Search for sessions containing this term."
    ),
    semantic_variations: str | None = typer.Option(
        None,
        help="JSON string describing semantic variations for search_term.",
    ),
    project_root: Path | None = typer.Option(
        None,
        help="Absolute path to project root for scoping. Defaults to current directory.",
    ),
    include_all_projects: bool = typer.Option(
        False, help="Include sessions across all projects instead of scoping to one."
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.JSON, "--output-format", case_sensitive=False
    ),
) -> None:
    """Capture session context for Claude or Codex."""
    workspace = load_workspace()
    script_map = {
        ContextPlatform.CLAUDE: workspace.repo_root
        / "shared"
        / "context"
        / "context_bundle_capture_claude.py",
        ContextPlatform.CODEX: workspace.repo_root
        / "shared"
        / "context"
        / "context_bundle_capture_codex.py",
    }

    script_path = script_map[platform]
    if not script_path.exists():
        typer.echo(f"Context capture script not found at {script_path}", err=True)
        raise typer.Exit(code=1)

    args: list[str] = ["--days", str(days), "--output-format", output_format.value]
    if uuid:
        args.extend(["--uuid", uuid])
    if search_term:
        args.extend(["--search-term", search_term])
    if semantic_variations:
        args.extend(["--semantic-variations", semantic_variations])
    if project_root:
        args.extend(["--project-root", str(project_root)])
    if include_all_projects:
        args.append("--include-all-projects")

    env = _env_with_shared(workspace.shared_root)
    proc = subprocess.run([sys.executable, str(script_path), *args], env=env)
    raise typer.Exit(code=proc.returncode)


@app.command("version")
def version() -> None:
    """Display CLI version information."""
    from importlib import metadata

    try:
        cli_version = metadata.version("enaible")
    except metadata.PackageNotFoundError:
        typer.echo("enaible (editable install not detected)", err=True)
        raise typer.Exit(code=1) from None
    else:
        typer.echo(f"enaible {cli_version}")


@app.command("doctor")
def doctor(
    json_output: bool = typer.Option(
        False,
        "--json/--no-json",
        help="Emit diagnostics as JSON instead of human-readable text.",
    ),
) -> None:
    """Run basic environment diagnostics."""
    from importlib import metadata

    report: dict[str, object] = {
        "python": platform.python_version(),
        "typer_version": metadata.version("typer"),
        "enaible_version": metadata.version("enaible"),
        "checks": {},
        "errors": [],
    }
    checks: dict[str, bool] = report["checks"]  # type: ignore[assignment]
    errors: list[str] = report["errors"]  # type: ignore[assignment]

    exit_code = _check_shared_workspace(checks, errors, report)
    context = _check_workspace_context(checks, errors, report)
    _check_schema(checks, context)

    _output_report(report, checks, json_output)
    raise typer.Exit(code=exit_code)


def _check_shared_workspace(
    checks: dict[str, bool], errors: list[str], report: dict[str, object]
) -> int:
    """Check shared workspace and analyzer registry."""
    shared_root = find_shared_root()
    if shared_root is None:
        checks["shared_workspace"] = False
        checks["analyzer_registry"] = False
        errors.append(
            "Shared workspace not found. Re-run `enaible install ... --sync-shared`."
        )
        return 1

    checks["shared_workspace"] = True
    report["shared_root"] = str(shared_root)
    registry_stub = shared_root / "core" / "base" / "analyzer_registry.py"
    registry_exists = registry_stub.exists()
    checks["analyzer_registry"] = registry_exists
    if not registry_exists:
        errors.append("Analyzer registry module not found under shared/core/base.")
        return 1
    return 0


def _check_workspace_context(
    checks: dict[str, bool], errors: list[str], report: dict[str, object]
) -> object | None:
    """Load and check workspace context."""
    try:
        context = load_workspace()
    except typer.BadParameter as exc:  # pragma: no cover - defensive
        checks["workspace"] = False
        errors.append(str(exc))
        return None
    checks["workspace"] = True
    report["repo_root"] = str(context.repo_root)
    return context


def _check_schema(checks: dict[str, bool], context: object | None) -> None:
    """Check schema exists if context is available."""
    if context is None:
        return
    schema_path = context.repo_root / ".enaible" / "schema.json"  # type: ignore[union-attr]
    checks["schema_exists"] = schema_path.exists()


def _output_report(
    report: dict[str, object], checks: dict[str, bool], json_output: bool
) -> None:
    """Output the diagnostic report in the requested format."""
    if json_output:
        typer.echo(json.dumps(report, indent=2, sort_keys=True))
        return
    typer.echo("Enaible Diagnostics")
    if "repo_root" in report:
        typer.echo(f"  Repo root: {report['repo_root']}")
    typer.echo(f"  Python: {report['python']}")
    typer.echo(f"  Typer: {report['typer_version']}")
    for name, passed in checks.items():
        status = "OK" if passed else "FAIL"
        typer.echo(f"  {name.replace('_', ' ').title()}: {status}")
    if report.get("errors"):
        typer.echo("Errors:")
        for err in report["errors"]:  # type: ignore[union-attr]
            typer.echo(f"  - {err}")
