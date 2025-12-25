#!/usr/bin/env python
"""Discover entities with Parallel AI FindAll."""

from __future__ import annotations

import argparse
import sys

from parallel_api import FINDALL_BETA_HEADER, api_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Discover entities (async).")
    parser.add_argument("objective", help="Natural language discovery objective")
    parser.add_argument(
        "-e",
        "--entity",
        required=True,
        help="Entity type (e.g., company, person, product)",
    )
    parser.add_argument(
        "-c",
        "--condition",
        action="append",
        help="Match conditions (repeatable)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="Maximum matches (5-1000)",
    )
    parser.add_argument(
        "-g",
        "--generator",
        choices=("base", "core", "pro"),
        default="base",
        help="Generator tier",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not 5 <= args.limit <= 1000:
        print(f"Error: Limit must be between 5 and 1000, got {args.limit}.")
        return 1

    match_conditions = []
    if args.condition:
        for index, cond in enumerate(args.condition, 1):
            match_conditions.append({"name": f"condition_{index}", "description": cond})
    else:
        match_conditions.append(
            {"name": "primary_criteria", "description": args.objective}
        )

    payload = {
        "objective": args.objective,
        "entity_type": args.entity,
        "match_conditions": match_conditions,
        "generator": args.generator,
        "match_limit": args.limit,
    }

    try:
        result = api_request(
            "POST",
            "/v1beta/findall/runs",
            payload=payload,
            beta_header=FINDALL_BETA_HEADER,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    findall_id = result.get("findall_id", "unknown")
    status_info = result.get("status", {})
    status = (
        status_info.get("status", "unknown")
        if isinstance(status_info, dict)
        else "unknown"
    )

    print("FindAll task created successfully!")
    print(f"  FindAll ID: {findall_id}")
    print(f"  Status: {status}")
    print(f"  Generator: {args.generator}")
    print(f"  Limit: {args.limit}")
    print("\nCheck progress: parallel_status.py status <findall_id> --type findall")
    print("Get results:    parallel_status.py result <findall_id> --type findall")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
