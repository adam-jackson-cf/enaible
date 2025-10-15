"""Analyzer command group for the Enaible CLI."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any

import typer

from ..app import app
from ..models.results import AnalyzerRunResponse
from ..runtime.context import WorkspaceContext, load_workspace

if TYPE_CHECKING:  # pragma: no cover
    pass


_analyzers_app = typer.Typer(help="Run and inspect registered analyzers.")
app.add_typer(_analyzers_app, name="analyzers")


_registry_bootstrapped = False


def _ensure_registry_loaded(context: WorkspaceContext) -> None:
    global _registry_bootstrapped
    if _registry_bootstrapped:
        return

    # Import bootstrap module which registers analyzers via side effects.
    __import__("core.base.registry_bootstrap")
    _registry_bootstrapped = True


def _resolve_analyzer_registry() -> Any:
    from core.base import AnalyzerRegistry

    return AnalyzerRegistry


def _create_config(
    *,
    target: Path,
    min_severity: str,
    summary_mode: bool,
    max_files: int | None,
    output_format: str,
) -> Any:
    from core.base import create_analyzer_config

    config = create_analyzer_config(
        target_path=str(target),
        min_severity=min_severity,
        summary_mode=summary_mode,
        output_format=output_format,
    )

    if max_files is not None:
        config.max_files = max_files
    return config


def _emit_json(payload: dict[str, Any], out: Path | None) -> None:
    rendered = json.dumps(payload, indent=2)
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered)
    else:
        typer.echo(rendered)


@_analyzers_app.command("run")
def analyzers_run(
    tool: str = typer.Argument(
        ..., help="Analyzer registry key (e.g. quality:lizard)."
    ),
    target: Path = typer.Option(Path("."), "--target", "-t", help="Path to analyze."),
    json_output: bool = typer.Option(
        True,
        "--json/--no-json",
        help="Emit normalized JSON payload (default).",
    ),
    out: Path
    | None = typer.Option(
        None,
        "--out",
        "-o",
        help="Optional file to write result JSON to.",
    ),
    min_severity: str = typer.Option(
        "low",
        "--min-severity",
        help="Minimum severity to include in findings.",
    ),
    max_files: int
    | None = typer.Option(
        None,
        "--max-files",
        help="Limit the number of files processed.",
    ),
    summary_mode: bool = typer.Option(
        False,
        "--summary",
        help="Return a severity summary only (omits full findings).",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable verbose analyzer logs."
    ),
    no_external: bool = typer.Option(
        False,
        "--no-external",
        help="Disable analyzer features requiring external dependencies (sets ENAIBLE_DISABLE_EXTERNAL=1).",
    ),
) -> None:
    """Run a registered analyzer and emit normalized results."""
    context = load_workspace()
    _ensure_registry_loaded(context)

    registry = _resolve_analyzer_registry()

    if no_external:
        os.environ.setdefault("ENAIBLE_DISABLE_EXTERNAL", "1")

    config = _create_config(
        target=target,
        min_severity=min_severity,
        summary_mode=summary_mode,
        max_files=max_files,
        output_format="json" if json_output else "console",
    )

    try:
        analyzer = registry.create(tool, config=config)
    except KeyError as exc:
        raise typer.BadParameter(str(exc)) from exc

    if hasattr(analyzer, "verbose"):
        analyzer.verbose = bool(verbose)

    started = time.time()
    result = analyzer.analyze(str(target))
    finished = time.time()

    response = AnalyzerRunResponse.from_analysis_result(
        tool=tool,
        result=result,
        started_at=started,
        finished_at=finished,
        summary_mode=summary_mode,
        min_severity=min_severity,
    )

    payload = response.to_dict()

    if json_output:
        _emit_json(payload, out)
    else:
        # Analyzer handles console output internally; only write JSON when requested.
        if out is not None:
            _emit_json(payload, out)

    raise typer.Exit(code=response.exit_code)


@_analyzers_app.command("list")
def analyzers_list(
    json_output: bool = typer.Option(
        True, "--json/--no-json", help="Emit JSON output."
    ),
) -> None:
    """List all registered analyzers."""
    context = load_workspace()
    _ensure_registry_loaded(context)
    registry = _resolve_analyzer_registry()

    analyzers = []
    for name, analyzer_cls in sorted(registry._registry.items()):  # type: ignore[attr-defined]
        analyzers.append(
            {
                "tool": name,
                "doc": (analyzer_cls.__doc__ or "").strip(),
                "module": f"{analyzer_cls.__module__}.{analyzer_cls.__name__}",
            }
        )

    if json_output:
        _emit_json({"analyzers": analyzers}, None)
    else:
        for entry in analyzers:
            typer.echo(f"{entry['tool']}: {entry['module']}")
