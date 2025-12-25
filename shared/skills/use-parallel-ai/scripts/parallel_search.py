#!/usr/bin/env python
"""Search the web with Parallel AI."""

from __future__ import annotations

import argparse
import json
import sys

from parallel_api import api_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search the web with Parallel AI.")
    parser.add_argument("objective", help="Natural language search objective")
    parser.add_argument(
        "-q",
        "--query",
        action="append",
        help="Search query (repeatable)",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=10,
        help="Maximum results to return",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format",
    )
    return parser


def print_search_markdown(result: dict) -> None:
    print("# Search Results\n")
    print(f"**Search ID:** {result.get('search_id', 'N/A')}\n")

    results = result.get("results", [])
    if not results:
        print("No results found.")
        return

    for index, item in enumerate(results, 1):
        print(f"## {index}. {item.get('title', 'Untitled')}\n")
        print(f"**URL:** {item.get('url', 'N/A')}")
        if item.get("publish_date"):
            print(f"**Published:** {item['publish_date']}")
        print()
        excerpts = item.get("excerpts", [])
        if excerpts:
            print("### Excerpts\n")
            for excerpt in excerpts:
                print(f"> {excerpt}\n")
        print("---\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    queries = args.query if args.query else [args.objective]
    payload = {
        "objective": args.objective,
        "search_queries": queries,
        "max_results": args.max_results,
        "excerpts": {"max_chars_per_result": 10000},
    }

    try:
        result = api_request("POST", "/v1beta/search", payload=payload)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "markdown":
        print_search_markdown(result)
    else:
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
