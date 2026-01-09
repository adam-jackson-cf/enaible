#!/usr/bin/env python
"""Create deterministic domain mappings for research questions."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import (
    validate_domain_map,
    validate_domain_plan,
    validate_recency_policy,
    validate_requirements,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_overrides(raw: list[str]) -> dict[str, list[str]]:
    overrides: dict[str, list[str]] = {}
    for entry in raw:
        if "=" not in entry:
            raise SystemExit(
                "Overrides must be in the form question_id=domain[,domain]."
            )
        question_id, domains_raw = entry.split("=", 1)
        domains = [item.strip() for item in domains_raw.split(",") if item.strip()]
        if not domains:
            raise SystemExit("Overrides must specify at least one domain.")
        overrides[question_id.strip()] = domains
    return overrides


def compile_patterns(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.IGNORECASE) for pattern in patterns]


def score_question(
    text: str, domain: dict[str, Any]
) -> tuple[int, list[str], list[str]]:
    lowered = text.lower()
    keyword_hits = [
        word for word in domain.get("keywords", []) if word.lower() in lowered
    ]
    pattern_hits = []
    for pattern in domain.get("patterns", []):
        if re.search(pattern, text, re.IGNORECASE):
            pattern_hits.append(pattern)
    score = len(keyword_hits) + len(pattern_hits)
    return score, keyword_hits, pattern_hits


def select_domain(
    question_id: str,
    text: str,
    domains: dict[str, Any],
    overrides: dict[str, list[str]],
) -> dict[str, Any]:
    if question_id in overrides:
        selected = overrides[question_id]
        for name in selected:
            if name not in domains:
                raise SystemExit(
                    f"Override domain '{name}' is not defined in domain map."
                )
        return {
            "domains": selected,
            "rationale": {"override": True, "keywords": [], "patterns": []},
        }

    scored: list[tuple[str, int, list[str], list[str]]] = []
    for name, config in domains.items():
        score, keyword_hits, pattern_hits = score_question(text, config)
        if score:
            scored.append((name, score, keyword_hits, pattern_hits))

    if not scored:
        raise SystemExit(
            f"No domain match for question '{question_id}'. Provide --override to continue."
        )

    scored.sort(key=lambda item: item[1], reverse=True)
    top_score = scored[0][1]
    top_matches = [item for item in scored if item[1] == top_score]
    if len(top_matches) > 1:
        matched = ", ".join(item[0] for item in top_matches)
        raise SystemExit(
            f"Ambiguous domain match for question '{question_id}': {matched}. Use --override."
        )

    name, _, keyword_hits, pattern_hits = top_matches[0]
    return {
        "domains": [name],
        "rationale": {
            "override": False,
            "keywords": keyword_hits,
            "patterns": pattern_hits,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Map research questions to deterministic research domains."
    )
    parser.add_argument("--requirements-path", required=True)
    parser.add_argument("--domain-map-path")
    parser.add_argument("--recency-policy-path")
    parser.add_argument("--output-path")
    parser.add_argument("--override", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    requirements = load_json(Path(args.requirements_path))
    validate_requirements(requirements)
    domain_map_path = args.domain_map_path or str(
        Path(__file__).resolve().parents[1] / "assets" / "domain-map.json"
    )
    domain_map = load_json(Path(domain_map_path))
    validate_domain_map(domain_map)
    recency_path = args.recency_policy_path or str(
        Path(__file__).resolve().parents[1] / "assets" / "recency-policy.json"
    )
    recency_policy = load_json(Path(recency_path))
    validate_recency_policy(recency_policy)
    domains = domain_map.get("domains")
    if not domains:
        raise SystemExit("Domain map is missing 'domains'.")

    overrides = parse_overrides(args.override)

    questions = requirements.get("questions") or []
    if not questions:
        raise SystemExit("Requirements file must include questions.")

    planned_questions = []
    for question in questions:
        question_id = question.get("id")
        text = question.get("text")
        if not question_id or not text:
            raise SystemExit("Each question must include 'id' and 'text'.")
        selection = select_domain(question_id, text, domains, overrides)
        primary_domain = selection["domains"][0]
        recency = recency_policy.get("policies", {}).get(primary_domain)
        if not recency:
            raise SystemExit(f"Recency policy missing for domain '{primary_domain}'.")
        planned_questions.append(
            {
                "id": question_id,
                "text": text,
                "domains": selection["domains"],
                "primaryDomain": primary_domain,
                "recencyPolicy": recency,
                "expectedSourceTypes": domains[primary_domain].get("sourceTypes"),
                "rationale": selection["rationale"],
            }
        )

    summary = {}
    for entry in planned_questions:
        primary = entry["primaryDomain"]
        summary[primary] = summary.get(primary, 0) + 1

    output = {
        "plannedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "domainMapVersion": domain_map.get("version"),
        "questions": planned_questions,
        "summary": summary,
    }
    validate_domain_plan(output)

    output_path = args.output_path
    if not output_path:
        artifact_root = Path(requirements.get("artifactRoot"))
        output_path = artifact_root / "domain-plan.json"
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote domain plan to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
