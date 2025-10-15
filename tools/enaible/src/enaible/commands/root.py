"""Root command definitions for Enaible CLI."""

from __future__ import annotations

import json
import platform
from importlib import metadata

import typer

from ..app import app
from ..runtime.context import load_workspace

root_app = typer.Typer(help="Top-level commands placeholder.")


@app.command("version")
def version() -> None:
    """Display CLI version information."""
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
    )
) -> None:
    """Run basic environment diagnostics."""
    report: dict[str, object] = {
        "python": platform.python_version(),
        "typer_version": metadata.version("typer"),
        "checks": {},
        "errors": [],
    }
    exit_code = 0

    try:
        context = load_workspace()
    except typer.BadParameter as exc:  # pragma: no cover - defensive
        report["errors"].append(str(exc))
        report["checks"]["workspace"] = False
        exit_code = 1
        context = None  # type: ignore[assignment]
    else:
        report["checks"]["workspace"] = True
        report["repo_root"] = str(context.repo_root)
        report["shared_root"] = str(context.shared_root)

    if context is not None:
        schema_path = context.repo_root / ".enaible" / "schema.json"
        schema_exists = schema_path.exists()
        report["checks"]["schema_exists"] = schema_exists
        if not schema_exists:
            report["errors"].append(
                "Missing .enaible/schema.json – regenerate artifacts schema."
            )
            exit_code = 1

        registry_stub = context.shared_root / "core" / "base" / "analyzer_registry.py"
        registry_exists = registry_stub.exists()
        report["checks"]["analyzer_registry"] = registry_exists
        if not registry_exists:
            report["errors"].append(
                "Analyzer registry module not found under shared/core/base."
            )
            exit_code = 1

    if json_output:
        typer.echo(json.dumps(report, indent=2, sort_keys=True))
    else:
        checks = report.get("checks", {})
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
            for err in report["errors"]:
                typer.echo(f"  - {err}")

    raise typer.Exit(code=exit_code)
