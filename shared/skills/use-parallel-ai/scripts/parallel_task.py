#!/usr/bin/env python
"""Create an async task with Parallel AI."""

from __future__ import annotations

import argparse
import sys

from parallel_api import api_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create an enrichment or research task (async)."
    )
    parser.add_argument("input", help="Input data to enrich or research")
    parser.add_argument(
        "-s",
        "--schema",
        help="Output schema description",
    )
    parser.add_argument(
        "-p",
        "--processor",
        choices=("base", "core"),
        default="base",
        help="Processor type",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload: dict = {
        "input": args.input,
        "processor": args.processor,
        "task_spec": {},
    }
    if args.schema:
        payload["task_spec"]["output_schema"] = args.schema

    try:
        result = api_request(
            "POST", "/v1/tasks/runs", payload=payload, beta_header=None
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    run_id = result.get("run_id", "unknown")
    status = result.get("status", "unknown")

    print("Task created successfully!")
    print(f"  Run ID: {run_id}")
    print(f"  Status: {status}")
    print("\nCheck progress: parallel_status.py status <run_id>")
    print("Get results:    parallel_status.py result <run_id>")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
