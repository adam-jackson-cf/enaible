#!/usr/bin/env python
"""Validate citations against logged sources."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import (
    validate_analysis,
    validate_citation_report,
    validate_evidence,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate citation coverage.")
    parser.add_argument("--analysis-path", required=True)
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--min-sources-key", type=int, default=3)
    parser.add_argument("--min-sources-supporting", type=int, default=2)
    parser.add_argument("--min-sources-background", type=int, default=1)
    parser.add_argument("--min-sources-insight", type=int, default=2)
    parser.add_argument("--min-sources-recommendation", type=int, default=2)
    return parser.parse_args()


def required_sources(importance: str, args: argparse.Namespace) -> int:
    if importance == "key":
        return args.min_sources_key
    if importance == "supporting":
        return args.min_sources_supporting
    if importance == "background":
        return args.min_sources_background
    raise SystemExit(
        "importance must be one of: key, supporting, background for each finding."
    )


def build_report_entries(
    entity_type: str,
    entities: list[dict[str, Any]],
    sources: dict[str, dict[str, Any]],
    min_sources: int,
    importance_mode: bool = False,
    args: argparse.Namespace | None = None,
    allow_missing_id: bool = False,
    id_prefix: str | None = None,
) -> tuple[list[dict[str, Any]], bool]:
    report_entries: list[dict[str, Any]] = []
    has_failures = False
    for idx, entity in enumerate(entities, start=1):
        entity_id = entity.get("id")
        source_ids = entity.get("sourceIds") or []
        if not entity_id:
            if allow_missing_id:
                prefix = id_prefix or entity_type
                entity_id = f"{prefix}-{idx:03d}"
            else:
                raise SystemExit(f"Each {entity_type} must include 'id'.")
        required = min_sources
        if importance_mode:
            importance = entity.get("importance")
            if not importance:
                raise SystemExit("Each finding must include 'importance'.")
            required = required_sources(importance, args)
        missing_sources = [
            source_id for source_id in source_ids if source_id not in sources
        ]
        issues = []
        if missing_sources:
            issues.append(f"Missing sources: {', '.join(missing_sources)}")
        if len(source_ids) < required:
            issues.append(
                f"Only {len(source_ids)} sources; minimum for {entity_type} is {required}."
            )
        if issues:
            has_failures = True
        report_entries.append(
            {
                "entityType": entity_type,
                "entityId": entity_id,
                "issues": issues,
            }
        )
    return report_entries, has_failures


def main() -> int:
    args = parse_args()
    analysis_payload = load_json(Path(args.analysis_path))
    evidence_payload = load_json(Path(args.evidence_path))
    validate_analysis(analysis_payload)
    validate_evidence(evidence_payload)
    sources = {item.get("id"): item for item in evidence_payload.get("sources", [])}

    findings = analysis_payload.get("findings") or []
    insights = analysis_payload.get("insights") or []
    recommendations = analysis_payload.get("recommendations") or []

    report = []
    has_failures = False

    findings_report, findings_failed = build_report_entries(
        "finding", findings, sources, args.min_sources_key, True, args
    )
    report.extend(findings_report)
    has_failures = has_failures or findings_failed

    insights_report, insights_failed = build_report_entries(
        "insight",
        insights,
        sources,
        args.min_sources_insight,
        allow_missing_id=True,
        id_prefix="insight",
    )
    report.extend(insights_report)
    has_failures = has_failures or insights_failed

    recommendations_report, rec_failed = build_report_entries(
        "recommendation", recommendations, sources, args.min_sources_recommendation
    )
    report.extend(recommendations_report)
    has_failures = has_failures or rec_failed

    output = {
        "checkedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "status": "fail" if has_failures else "pass",
        "items": report,
    }
    validate_citation_report(output)

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    if has_failures:
        raise SystemExit("Citation validation failed. See report.")
    print(f"Citation validation passed. Wrote report to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
