#!/usr/bin/env python
"""Validate source coverage, recency, and logging requirements."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from schema_utils import (
    validate_domain_plan,
    validate_evidence,
    validate_requirements,
    validate_validation_report,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(value: str) -> date:
    try:
        if "T" in value:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        return date.fromisoformat(value)
    except ValueError as exc:
        raise SystemExit(f"Invalid date format: {value}") from exc


def months_since(published: date, current: date) -> int:
    months = (current.year - published.year) * 12 + (current.month - published.month)
    if current.day < published.day:
        months -= 1
    return months


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate research artifacts.")
    parser.add_argument("--requirements-path", required=True)
    parser.add_argument("--domain-plan-path", required=True)
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--min-sources", type=int, default=3)
    parser.add_argument("--allow-undated", action="append", default=[])
    parser.add_argument("--allow-single-type", action="append", default=[])
    return parser.parse_args()


def validate_question(
    question: dict[str, Any],
    sources: list[dict[str, Any]],
    searches: list[dict[str, Any]],
    min_sources: int,
    allow_undated: set[str],
    allow_single_type: set[str],
    online_research: bool,
) -> tuple[list[str], list[str]]:
    issues = []
    warnings = []
    question_id = question["id"]

    issues.extend(check_searches(online_research, searches))
    issues.extend(
        check_source_counts(
            sources, min_sources, online_research, allow_single_type, question_id
        )
    )
    issues.extend(check_source_types(question, sources))
    warnings.extend(check_source_type_warnings(question, sources))
    issues.extend(check_recency(question, sources, allow_undated, question_id))
    warnings.extend(check_recency_warnings(question, sources))

    return issues, warnings


def check_searches(online_research: bool, searches: list[dict[str, Any]]) -> list[str]:
    if online_research and not searches:
        return ["No search log entries recorded for this question."]
    return []


def check_source_counts(
    sources: list[dict[str, Any]],
    min_sources: int,
    online_research: bool,
    allow_single_type: set[str],
    question_id: str,
) -> list[str]:
    issues: list[str] = []
    if len(sources) < min_sources:
        issues.append(f"Only {len(sources)} sources logged; minimum is {min_sources}.")
    if online_research and not any(
        source.get("origin") == "engagement" for source in sources
    ):
        issues.append("At least one source must be collected during this engagement.")
    source_types = {
        source.get("sourceType") for source in sources if source.get("sourceType")
    }
    if len(source_types) < 2 and question_id not in allow_single_type:
        issues.append(
            "Sources lack diversity; provide at least two source types or allow override."
        )
    return issues


def check_source_types(
    question: dict[str, Any], sources: list[dict[str, Any]]
) -> list[str]:
    expected_types = question.get("expectedSourceTypes") or []
    if expected_types and not any(
        source.get("sourceType") in expected_types for source in sources
    ):
        return [
            "No sources match expected source types for this domain. "
            "Add sources from the expected categories or update the domain plan."
        ]
    return []


def check_source_type_warnings(
    question: dict[str, Any], sources: list[dict[str, Any]]
) -> list[str]:
    expected_types = question.get("expectedSourceTypes") or []
    if not expected_types:
        return []
    unexpected_types = {
        source.get("sourceType")
        for source in sources
        if source.get("sourceType") and source.get("sourceType") not in expected_types
    }
    if unexpected_types:
        return [
            "Found sources outside expected types: "
            f"{', '.join(sorted(unexpected_types))}."
        ]
    return []


def check_recency(
    question: dict[str, Any],
    sources: list[dict[str, Any]],
    allow_undated: set[str],
    question_id: str,
) -> list[str]:
    issues: list[str] = []
    current_date = datetime.now(UTC).date()
    recency = question.get("recencyPolicy") or {}
    max_months = recency.get("maxMonths")
    for source in sources:
        published_date = source.get("publishedDate")
        if not published_date:
            if question_id not in allow_undated:
                issues.append("Source missing published date without approval.")
            continue
        published = parse_date(published_date)
        age_months = months_since(published, current_date)
        if max_months is not None and age_months > max_months:
            issues.append(
                f"Source {source.get('id')} exceeds max age ({age_months} months > {max_months})."
            )
    return issues


def check_recency_warnings(
    question: dict[str, Any], sources: list[dict[str, Any]]
) -> list[str]:
    warnings: list[str] = []
    current_date = datetime.now(UTC).date()
    recency = question.get("recencyPolicy") or {}
    preferred_months = recency.get("preferredMonths")
    for source in sources:
        published_date = source.get("publishedDate")
        if not published_date:
            continue
        published = parse_date(published_date)
        age_months = months_since(published, current_date)
        if preferred_months is not None and age_months > preferred_months:
            warnings.append(
                f"Source {source.get('id')} older than preferred ({age_months} months > {preferred_months})."
            )
    return warnings


def main() -> int:
    args = parse_args()
    requirements = load_json(Path(args.requirements_path))
    domain_plan = load_json(Path(args.domain_plan_path))
    evidence = load_json(Path(args.evidence_path))
    validate_requirements(requirements)
    validate_domain_plan(domain_plan)
    validate_evidence(evidence)

    questions = domain_plan.get("questions") or []
    if not questions:
        raise SystemExit("Domain plan must include questions.")

    online_research = requirements.get("onlineResearch") == "allowed"

    searches_by_question: dict[str, list[dict[str, Any]]] = {}
    for entry in evidence.get("searches", []):
        searches_by_question.setdefault(entry.get("questionId"), []).append(entry)

    sources_by_question: dict[str, list[dict[str, Any]]] = {}
    for entry in evidence.get("sources", []):
        sources_by_question.setdefault(entry.get("questionId"), []).append(entry)

    allow_undated = set(args.allow_undated)
    allow_single_type = set(args.allow_single_type)

    findings = []
    has_failures = False
    for question in questions:
        question_id = question.get("id")
        if not question_id:
            raise SystemExit("Each question in domain plan must include 'id'.")
        issues, warnings = validate_question(
            question,
            sources_by_question.get(question_id, []),
            searches_by_question.get(question_id, []),
            args.min_sources,
            allow_undated,
            allow_single_type,
            online_research,
        )
        if issues:
            has_failures = True
        findings.append(
            {
                "questionId": question_id,
                "issues": issues,
                "warnings": warnings,
            }
        )

    output = {
        "validatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "status": "fail" if has_failures else "pass",
        "questions": findings,
    }
    validate_validation_report(output)

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

    if has_failures:
        raise SystemExit("Validation failed. See validation report.")
    print(f"Validation passed. Wrote report to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
