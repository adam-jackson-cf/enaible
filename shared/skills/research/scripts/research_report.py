#!/usr/bin/env python
"""Assemble a research report from structured artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import (
    validate_analysis,
    validate_domain_plan,
    validate_evidence,
    validate_requirements,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def citation_label(source: dict[str, Any]) -> str:
    label = source.get("citationLabel") or source.get("title") or "Source"
    date = source.get("publishedDate") or "Undated"
    return f"[{label}, {date}]"


def citations_for(source_ids: list[str], sources: dict[str, dict[str, Any]]) -> str:
    labels = []
    for source_id in source_ids:
        source = sources.get(source_id)
        if not source:
            raise SystemExit(f"Missing source for citation: {source_id}")
        labels.append(citation_label(source))
    return " ".join(labels)


def source_publisher(source: dict[str, Any]) -> str:
    if source.get("publisher"):
        return source["publisher"]
    url = source.get("url") or ""
    parts = url.split("/")
    if len(parts) > 2 and parts[2]:
        return parts[2]
    return "Unknown publisher"


def build_objectives_section(requirements: dict[str, Any]) -> list[str]:
    lines = ["## 1. Research Objectives", ""]
    lines.append(f"**Objective**: {requirements.get('objective')}")
    lines.append(f"**Scope**: {requirements.get('scope')}")
    lines.append(f"**Decision Context**: {requirements.get('decisionContext')}")
    lines.append("")
    lines.append("**Questions**:")
    for question in requirements.get("questions", []):
        lines.append(f"- {question.get('text')}")
    lines.append("")
    return lines


def build_methodology_section(
    domain_plan: dict[str, Any], sources_count: int
) -> list[str]:
    lines = ["## 2. Methodology", "", "### Domain Coverage", ""]
    lines.append("| Domain | Questions |")
    lines.append("| --- | --- |")
    for domain, count in (domain_plan.get("summary") or {}).items():
        lines.append(f"| {domain} | {count} |")
    lines.append("")
    lines.append("### Source Collection")
    lines.append("")
    lines.append(f"Total sources logged: {sources_count}")
    lines.append("")
    return lines


def build_findings_section(
    findings: list[dict[str, Any]], sources: dict[str, dict[str, Any]]
) -> tuple[list[str], set[str]]:
    lines = ["## 3. Key Findings", ""]
    used_sources: set[str] = set()
    for finding in findings:
        source_ids = finding.get("sourceIds") or []
        used_sources.update(source_ids)
        citations = citations_for(source_ids, sources)
        lines.append(f"### {finding.get('title')}")
        lines.append("")
        lines.append(f"{finding.get('statement')} {citations}")
        lines.append("")
        lines.append(f"**Confidence**: {finding.get('confidence')}")
        lines.append("")
    return lines, used_sources


def build_synthesis_section(
    insights: list[dict[str, Any]], sources: dict[str, dict[str, Any]]
) -> tuple[list[str], set[str]]:
    lines = ["## 4. Synthesis and Insights", ""]
    used_sources: set[str] = set()
    for insight in insights:
        statement = insight.get("statement")
        source_ids = insight.get("sourceIds") or []
        used_sources.update(source_ids)
        citations = citations_for(source_ids, sources)
        lines.append(f"- {statement} {citations}")
    lines.append("")
    return lines, used_sources


def build_recommendations_section(
    recommendations: list[dict[str, Any]], sources: dict[str, dict[str, Any]]
) -> tuple[list[str], set[str]]:
    lines = ["## 5. Recommendations", ""]
    used_sources: set[str] = set()
    for idx, recommendation in enumerate(recommendations, start=1):
        source_ids = recommendation.get("sourceIds") or []
        used_sources.update(source_ids)
        citations = citations_for(source_ids, sources)
        lines.append(f"{idx}. **{recommendation.get('action')}**")
        lines.append("")
        lines.append(f"   Rationale: {recommendation.get('rationale')} {citations}")
        lines.append("")
        lines.append(f"   Priority: {recommendation.get('priority')}")
        lines.append("")
    return lines, used_sources


def build_limitations_section(limitations: list[str]) -> list[str]:
    lines = ["## 6. Limitations and Future Research", ""]
    for limitation in limitations:
        lines.append(f"- {limitation}")
    lines.append("")
    return lines


def build_references_section(
    used_sources: set[str], sources: dict[str, dict[str, Any]]
) -> list[str]:
    lines = ["## 7. References", ""]
    reference_list = []
    for idx, source_id in enumerate(sorted(used_sources), start=1):
        source = sources[source_id]
        title = source.get("title") or "Untitled"
        publisher = source_publisher(source)
        date_value = source.get("publishedDate") or "Undated"
        reference_list.append(
            f"[{idx}] {title}. {publisher}. ({date_value}). URL: {source.get('url')}"
        )
    lines.extend(reference_list)
    lines.append("")
    return lines


def build_appendix_section(search_log: dict[str, Any]) -> list[str]:
    lines = ["## 8. Appendices", "", "### Appendix A: Search Methodology", ""]
    for search in search_log.get("searches", []):
        lines.append(
            f"- [{search.get('questionId')}] {search.get('query')} ({search.get('engine')})"
        )
    lines.append("")
    return lines


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble research report markdown.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--requirements-path", required=True)
    parser.add_argument("--domain-plan-path", required=True)
    parser.add_argument("--analysis-path", required=True)
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--output-path", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requirements = load_json(Path(args.requirements_path))
    domain_plan = load_json(Path(args.domain_plan_path))
    analysis = load_json(Path(args.analysis_path))
    evidence = load_json(Path(args.evidence_path))
    validate_requirements(requirements)
    validate_domain_plan(domain_plan)
    validate_analysis(analysis)
    validate_evidence(evidence)

    sources = {item.get("id"): item for item in evidence.get("sources", [])}
    findings = analysis.get("findings") or []
    recommendations = analysis.get("recommendations") or []
    insights = analysis.get("insights") or []

    lines: list[str] = []
    lines.append(f"# {args.title}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(analysis["executiveSummary"])
    lines.append("")

    lines.append("## Table of Contents")
    lines.append("")
    lines.extend(
        [
            "1. Research Objectives",
            "2. Methodology",
            "3. Key Findings",
            "4. Synthesis and Insights",
            "5. Recommendations",
            "6. Limitations and Future Research",
            "7. References",
            "8. Appendices",
        ]
    )
    lines.append("")

    lines.extend(build_objectives_section(requirements))
    lines.extend(build_methodology_section(domain_plan, len(sources)))

    findings_lines, findings_sources = build_findings_section(findings, sources)
    lines.extend(findings_lines)

    synthesis_lines, synthesis_sources = build_synthesis_section(insights, sources)
    lines.extend(synthesis_lines)

    recommendations_lines, recommendation_sources = build_recommendations_section(
        recommendations, sources
    )
    lines.extend(recommendations_lines)

    lines.extend(build_limitations_section(analysis.get("limitations", [])))

    used_sources = findings_sources | synthesis_sources | recommendation_sources
    lines.extend(build_references_section(used_sources, sources))
    lines.extend(build_appendix_section(evidence))

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    summary_path = out_path.with_suffix(".json")
    summary_path.write_text(
        json.dumps(
            {
                "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "reportPath": str(out_path),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote report to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
