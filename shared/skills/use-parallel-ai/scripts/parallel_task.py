"""Task command for Parallel AI."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer

_REPO_ROOT = Path(__file__).resolve().parents[4]
_PARALLEL_SRC = _REPO_ROOT / "tools" / "parallel" / "src"
if _PARALLEL_SRC.exists() and str(_PARALLEL_SRC) not in sys.path:
    sys.path.insert(0, str(_PARALLEL_SRC))

from parallel.app import app  # noqa: E402
from parallel.client import api_request  # noqa: E402


@app.command()
def task(
    input_data: Annotated[
        str, typer.Argument(help="Input data to enrich or research query")
    ],
    schema: Annotated[
        str | None,
        typer.Option("--schema", "-s", help="Output schema description"),
    ] = None,
    processor: Annotated[
        str,
        typer.Option("--processor", "-p", help="Processor type: base or core"),
    ] = "base",
) -> None:
    """Create an enrichment or research task (async).

    Returns a run_id immediately. Use 'parallel status <run_id>' to check progress
    and 'parallel result <run_id>' to fetch completed results.

    Examples
    --------
        parallel task "United Nations" --schema "founding date in MM-YYYY format"
        parallel task "OpenAI" --schema "funding rounds, valuation, key investors" --processor core
    """
    if processor not in ("base", "core"):
        print(f"Error: Invalid processor '{processor}'. Use 'base' or 'core'.")
        raise typer.Exit(1)

    payload: dict = {
        "input": input_data,
        "processor": processor,
        "task_spec": {},
    }
    if schema:
        payload["task_spec"]["output_schema"] = schema

    try:
        result = api_request("POST", "/v1/tasks/runs", json=payload, use_beta=False)

        run_id = result.get("run_id", "unknown")
        status = result.get("status", "unknown")

        print("Task created successfully!")
        print(f"  Run ID: {run_id}")
        print(f"  Status: {status}")
        print(f"\nCheck progress: parallel status {run_id}")
        print(f"Get results:    parallel result {run_id}")

    except Exception as e:
        print(f"Error: {e}", file=typer.get_text_stream("stderr"))
        raise typer.Exit(1) from None
