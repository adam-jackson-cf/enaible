#!/usr/bin/env python
"""Extract content with Parallel AI."""

from __future__ import annotations

import argparse
import json
import sys

from parallel_api import api_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract content from a URL.")
    parser.add_argument("url", help="URL to extract content from")
    parser.add_argument(
        "-o",
        "--objective",
        help="What to focus on when extracting",
    )
    parser.add_argument(
        "-f",
        "--full-content",
        action="store_true",
        help="Return full page content",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format",
    )
    return parser


def print_extract_markdown(result: dict) -> None:
    print("# Extraction Results\n")
    print(f"**Extract ID:** {result.get('extract_id', 'N/A')}\n")

    results = result.get("results", [])
    if not results:
        print("No content extracted.")
        return

    for item in results:
        print(f"## {item.get('title', 'Untitled')}\n")
        print(f"**URL:** {item.get('url', 'N/A')}")
        if item.get("publish_date"):
            print(f"**Published:** {item['publish_date']}")
        print()

        if item.get("full_content"):
            print("### Content\n")
            print(item["full_content"])
        elif item.get("excerpts"):
            print("### Excerpts\n")
            for excerpt in item["excerpts"]:
                print(f"> {excerpt}\n")
        print("---\n")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    payload: dict = {
        "urls": [args.url],
        "excerpts": not args.full_content,
        "full_content": args.full_content,
    }
    if args.objective:
        payload["objective"] = args.objective

    try:
        result = api_request("POST", "/v1beta/extract", payload=payload)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "markdown":
        print_extract_markdown(result)
    else:
        print(json.dumps(result, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
