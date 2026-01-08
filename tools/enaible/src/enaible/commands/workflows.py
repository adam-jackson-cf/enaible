"""Workflow command group for the Enaible CLI."""

from __future__ import annotations

from pathlib import Path

import typer

from ..app import app

_workflows_app = typer.Typer(help="Run managed workflows.")
app.add_typer(_workflows_app, name="workflows")


@_workflows_app.command("run")
def workflows_run(
    workflow: str = typer.Argument(
        ..., help="Workflow name (e.g., analyze-agentic-readiness)."
    ),
    target: Path = typer.Option(Path("."), "--target", "-t", help="Path to analyze."),
    artifact_root: Path | None = typer.Option(
        None,
        "--artifact-root",
        help="Custom artifact directory. If not provided, uses timestamped default.",
    ),
    auto: bool = typer.Option(
        False, "--auto", help="Skip confirmation prompts (auto-approve checkpoints)."
    ),
    days: int = typer.Option(
        180, "--days", help="History window for concentration and docs freshness."
    ),
    min_severity: str = typer.Option(
        "low",
        "--min-severity",
        help="Minimum severity to include in findings.",
        show_default=True,
    ),
    exclude_glob: list[str] = typer.Option(
        [],
        "--exclude",
        "-x",
        help="Additional glob patterns to exclude (repeatable).",
    ),
) -> None:
    """Run a managed workflow by name."""
    # Resolve paths before passing to workflow to handle relative paths correctly
    resolved_target = target.resolve()
    resolved_artifact_root = artifact_root.resolve() if artifact_root else None

    if workflow == "analyze-agentic-readiness":
        from ..workflows.agentic_readiness import run_workflow

        exit_code = run_workflow(
            target=resolved_target,
            artifact_root=resolved_artifact_root,
            days=days,
            min_severity=min_severity,
            excludes=exclude_glob if exclude_glob else None,
        )
        raise typer.Exit(code=exit_code)

    raise typer.BadParameter(
        f"Unknown workflow: {workflow}. Available workflows: analyze-agentic-readiness"
    )


@_workflows_app.command("list")
def workflows_list() -> None:
    """List available workflows."""
    workflows = [
        {
            "name": "analyze-agentic-readiness",
            "description": "Assess agentic readiness and maintenance scores.",
        },
    ]
    for wf in workflows:
        typer.echo(f"{wf['name']}: {wf['description']}")
