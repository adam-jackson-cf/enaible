#!/usr/bin/env python3
"""Timing utilities for the agentic readiness workflow."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator, Sequence

TIMING_ENV_VAR = "AGENTIC_READINESS_TIMING_LOG"
DEFAULT_LOG_PATH = Path("/tmp/agentic_readiness_test.log")


def _iso_timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _resolve_log_path() -> Path:
    path = os.environ.get(TIMING_ENV_VAR, str(DEFAULT_LOG_PATH))
    candidate = Path(path).expanduser()
    candidate.parent.mkdir(parents=True, exist_ok=True)
    return candidate


def _write_line(payload: dict[str, Any], mirror_stdout: bool = True) -> None:
    payload.setdefault("pid", os.getpid())
    line = json.dumps(payload, sort_keys=True)
    log_path = _resolve_log_path()
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    if mirror_stdout:
        print(line, flush=True)


@contextmanager
def log_phase(phase: str, metadata: dict[str, Any] | None = None) -> Iterator[None]:
    """Context manager that logs start/end timestamps for a phase."""

    start = time.perf_counter()
    payload = {
        "event": "start",
        "phase": phase,
        "timestamp": _iso_timestamp(),
    }
    if metadata:
        payload["metadata"] = metadata
    _write_line(payload)

    status = "success"
    error_message: str | None = None
    try:
        yield
    except Exception as exc:  # noqa: BLE001 - we re-raise after logging
        status = "error"
        error_message = repr(exc)
        raise
    finally:
        payload = {
            "event": "end",
            "phase": phase,
            "timestamp": _iso_timestamp(),
            "duration_seconds": round(time.perf_counter() - start, 3),
            "status": status,
        }
        if error_message:
            payload["error"] = error_message
        if metadata:
            payload["metadata"] = metadata
        _write_line(payload)


def log_summary(
    phase: str, duration_seconds: float, metadata: dict[str, Any] | None = None
) -> None:
    """Append a summary line for quick tailing dashboards."""

    payload = {
        "event": "summary",
        "phase": phase,
        "timestamp": _iso_timestamp(),
        "duration_seconds": round(duration_seconds, 3),
    }
    if metadata:
        payload["metadata"] = metadata
    _write_line(payload, mirror_stdout=False)


def _combine_metadata(
    metadata: dict[str, Any] | None,
    command: Sequence[str],
) -> dict[str, Any]:
    combined: dict[str, Any] = {"command": list(command), "cwd": os.getcwd()}
    if metadata:
        combined.update(metadata)
    return combined


def run_command_with_timing(
    phase: str, command: Sequence[str], metadata: dict[str, Any] | None = None
) -> int:
    """Execute a command while logging its start/end timestamps."""

    combined_metadata = _combine_metadata(metadata, command)
    payload = {
        "event": "start",
        "phase": phase,
        "timestamp": _iso_timestamp(),
        "metadata": combined_metadata,
    }
    _write_line(payload)

    start = time.perf_counter()
    exit_code = 0
    try:
        completed = subprocess.run(command, check=False)  # noqa: S603
        exit_code = completed.returncode
        return exit_code
    except KeyboardInterrupt:  # pragma: no cover - handled for completeness
        exit_code = 130
        raise
    except Exception:
        exit_code = 1
        raise
    finally:
        payload = {
            "event": "end",
            "phase": phase,
            "timestamp": _iso_timestamp(),
            "duration_seconds": round(time.perf_counter() - start, 3),
            "metadata": combined_metadata,
            "exit_code": exit_code,
        }
        _write_line(payload)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Run a command with agentic readiness timing instrumentation.")
    )
    parser.add_argument(
        "--phase",
        required=True,
        help="Logical name for the command (e.g., analyzer:jscpd)",
    )
    parser.add_argument(
        "--metadata",
        help="Optional JSON blob to attach to log entries",
    )
    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Command to execute (must follow '--').",
    )
    args = parser.parse_args(argv)
    if not args.command:
        parser.error("Command to execute must follow '--'.")
    return args


def _load_metadata(blob: str | None) -> dict[str, Any] | None:
    if not blob:
        return None
    try:
        parsed = json.loads(blob)
    except json.JSONDecodeError as exc:  # pragma: no cover - thin CLI
        raise SystemExit(f"Invalid metadata JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("Metadata JSON must be an object")
    return parsed


def main(argv: Sequence[str] | None = None) -> None:
    args = _parse_args(argv)
    command = args.command
    metadata = _load_metadata(args.metadata)
    exit_code = run_command_with_timing(args.phase, command, metadata)
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main(sys.argv[1:])
