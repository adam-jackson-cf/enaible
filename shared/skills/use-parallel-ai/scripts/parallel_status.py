#!/usr/bin/env python
"""Check status and results for Parallel AI runs."""

from __future__ import annotations

import argparse
import json
import sys

from parallel_api import FINDALL_BETA_HEADER, api_request


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check status or results.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    status_parser = subparsers.add_parser("status", help="Check run status")
    status_parser.add_argument("run_id", help="Task run_id or FindAll findall_id")
    status_parser.add_argument(
        "-t",
        "--type",
        choices=("task", "findall"),
        help="Run type (auto-detected if not specified)",
    )

    result_parser = subparsers.add_parser("result", help="Fetch run results")
    result_parser.add_argument("run_id", help="Task run_id or FindAll findall_id")
    result_parser.add_argument(
        "-t",
        "--type",
        choices=("task", "findall"),
        help="Run type (auto-detected if not specified)",
    )
    result_parser.add_argument("-o", "--output", help="Write results to file")
    result_parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format",
    )

    return parser


def detect_run_type(run_id: str, run_type: str | None) -> str | None:
    if run_type:
        return run_type
    if run_id.startswith("trun_"):
        return "task"
    if run_id.startswith("fa_") or run_id.startswith("findall_"):
        return "findall"
    return None


def print_task_result_markdown(result: dict) -> None:
    print("# Task Result\n")

    run_info = result.get("run", {})
    if run_info:
        print(f"**Status:** {run_info.get('status', 'N/A')}\n")

    output = result.get("output", {})
    if output:
        content = output.get("content", {})
        print("## Output\n")
        print(json.dumps(content, indent=2))

        basis = output.get("basis", [])
        if basis:
            print("\n## Basis & Citations\n")
            for item in basis:
                field = item.get("field", "unknown")
                confidence = item.get("confidence", "N/A")
                reasoning = item.get("reasoning", "")
                print(f"### {field} (confidence: {confidence})\n")
                if reasoning:
                    print(f"{reasoning}\n")
                citations = item.get("citations", [])
                if citations:
                    print("**Sources:**")
                    for cite in citations:
                        print(f"- [{cite.get('title', 'N/A')}]({cite.get('url', '')})")
                    print()


def print_findall_result_markdown(result: dict) -> None:
    print("# FindAll Results\n")

    candidates = result.get("candidates", [])
    if not candidates:
        print("No candidates found.")
        return

    print(f"**Total Candidates:** {len(candidates)}\n")

    for index, candidate in enumerate(candidates, 1):
        name = candidate.get("name", f"Candidate {index}")
        print(f"## {index}. {name}\n")

        for key, value in candidate.items():
            if key != "name":
                print(f"- **{key}:** {value}")
        print()


def run_status(run_id: str, run_type: str) -> int:
    try:
        if run_type == "task":
            result = api_request("GET", f"/v1/tasks/runs/{run_id}", beta_header=None)
        else:
            result = api_request(
                "GET",
                f"/v1beta/findall/runs/{run_id}",
                beta_header=FINDALL_BETA_HEADER,
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


def run_result(run_id: str, run_type: str, output: str | None, fmt: str) -> int:
    try:
        if run_type == "task":
            result = api_request(
                "GET",
                f"/v1/tasks/runs/{run_id}/result",
                beta_header=None,
            )
        else:
            result = api_request(
                "GET",
                f"/v1beta/findall/runs/{run_id}/result",
                beta_header=FINDALL_BETA_HEADER,
            )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_text = json.dumps(result, indent=2)

    if output:
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(output_text)
        print(f"Results written to {output}")
        return 0

    if fmt == "markdown" and run_type == "task":
        print_task_result_markdown(result)
    elif fmt == "markdown" and run_type == "findall":
        print_findall_result_markdown(result)
    else:
        print(output_text)

    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    run_type = detect_run_type(args.run_id, args.type)
    if run_type is None:
        print(
            "Error: Could not auto-detect run type. Use --type task or --type findall.",
            file=sys.stderr,
        )
        return 1

    if args.command == "status":
        return run_status(args.run_id, run_type)
    if args.command == "result":
        return run_result(args.run_id, run_type, args.output, args.format)

    print("Error: Unknown command", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
