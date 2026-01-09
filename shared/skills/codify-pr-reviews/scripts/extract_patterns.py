#!/usr/bin/env python
"""Extract normalized comment patterns from preprocessed groups."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def classify_category(text: str, categories: list[str]) -> str:
    keywords = {
        "security": ["sql", "xss", "csrf", "auth", "secret", "password", "token"],
        "error-handling": ["error", "exception", "try", "catch"],
        "type-safety": ["type", "any", "null", "undefined"],
        "performance": ["slow", "performance", "n+1", "cache"],
        "accessibility": ["aria", "a11y", "alt text"],
        "react-patterns": ["react", "useeffect", "hook", "key"],
        "api-design": ["endpoint", "request", "response", "api"],
        "database": ["database", "sql", "query", "migration"],
        "testing": ["test", "spec", "coverage"],
        "code-style": ["lint", "format", "naming", "style"],
    }
    lowered = text.lower()
    for category, words in keywords.items():
        if category in categories and any(word in lowered for word in words):
            return category
    return categories[0] if categories else "general"


def severity_for(category: str, is_red_flag: bool) -> str:
    if is_red_flag:
        return "critical"
    if category in {"security", "error-handling"}:
        return "high"
    if category in {"performance", "type-safety"}:
        return "medium"
    return "low"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract normalized patterns from preprocessed comments."
    )
    parser.add_argument("--preprocessed-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
    categories = defaults.get("categories", [])

    payload = json.loads(Path(args.preprocessed_path).read_text(encoding="utf-8"))
    groups = payload.get("commentGroups", [])
    patterns = []

    for group in groups:
        representative = group.get("representative", "").strip()
        category = classify_category(representative, categories)
        is_red_flag = bool(group.get("isRedFlag"))
        patterns.append(
            {
                "id": group.get("id"),
                "title": representative[:120],
                "description": representative,
                "frequency": group.get("occurrences"),
                "severity": severity_for(category, is_red_flag),
                "category": category,
                "isRedFlag": is_red_flag,
                "examples": group.get("examples", []),
            }
        )

    output = {
        "extractedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "totalPatterns": len(patterns),
        "patterns": patterns,
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote patterns to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
