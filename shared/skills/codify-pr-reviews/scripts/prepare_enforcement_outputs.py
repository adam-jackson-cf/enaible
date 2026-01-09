#!/usr/bin/env python
"""Prepare tooling change plan and doc pattern list from approved enforcement."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import validate_approved_enforcement, validate_coverage


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare enforcement outputs from approved decisions."
    )
    parser.add_argument("--approved-path", required=True)
    parser.add_argument("--coverage-path", required=True)
    parser.add_argument("--doc-patterns-path", required=True)
    parser.add_argument("--tooling-changes-path", required=True)
    args = parser.parse_args()

    approved = load_json(Path(args.approved_path))
    coverage = load_json(Path(args.coverage_path))
    validate_approved_enforcement(approved)
    validate_coverage(coverage)
    coverage_map = {item.get("id"): item for item in coverage.get("patterns", [])}

    doc_patterns: list[dict[str, Any]] = []
    tooling_tasks: list[str] = []
    tooling_json: list[dict[str, Any]] = []

    for item in approved.get("patterns", []):
        decision = item.get("decision", {})
        enforcement = decision.get("enforcementPath")
        if enforcement in {"docs", "both"} and decision.get("action") != "skip":
            doc_patterns.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "category": item.get("category"),
                    "frequency": item.get("frequency"),
                    "action": decision.get("action"),
                    "rationale": decision.get("rationale"),
                }
            )

        if enforcement in {"tooling", "both"}:
            tooling_action = decision.get("toolingAction")
            tooling_tasks.append(f"- {tooling_action}")
            tooling_json.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "action": tooling_action,
                    "enforcementPath": enforcement,
                    "rationale": decision.get("rationale"),
                }
            )
            coverage_entry = coverage_map.get(item.get("id"))
            if coverage_entry:
                for option in coverage_entry.get("deterministicOptions", []):
                    tooling_tasks.append(
                        f"  - Suggested tool: {option['tool']} ({option['action']})"
                    )

    doc_output = {
        "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "patterns": doc_patterns,
    }

    Path(args.doc_patterns_path).parent.mkdir(parents=True, exist_ok=True)
    Path(args.doc_patterns_path).write_text(
        json.dumps(doc_output, indent=2), encoding="utf-8"
    )

    tooling_report = [
        "# Tooling Changes",
        "",
        f"Source: `{Path(args.approved_path)}`",
        "",
    ]
    tooling_report.extend(tooling_tasks or ["- No tooling changes approved."])
    tooling_path = Path(args.tooling_changes_path)
    tooling_path.parent.mkdir(parents=True, exist_ok=True)
    tooling_path.write_text("\n".join(tooling_report).rstrip() + "\n", encoding="utf-8")
    tooling_json_path = tooling_path.with_suffix(".json")
    tooling_json_path.write_text(
        json.dumps(
            {
                "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "items": tooling_json,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
