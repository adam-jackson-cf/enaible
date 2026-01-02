#!/usr/bin/env python
"""Analyze comment groups and triage patterns against existing rules."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def extract_rules(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    rules: list[dict[str, Any]] = []
    current_title = None
    current_lines: list[str] = []

    for line in lines + ["## END"]:
        if line.startswith("## "):
            if current_title:
                body = "\n".join(current_lines)
                rules.append(
                    {
                        "title": current_title,
                        "content": body,
                        "hasDirectives": any(
                            line.strip().startswith("- ALWAYS")
                            or line.strip().startswith("- NEVER")
                            for line in current_lines
                        ),
                        "hasBad": "❌" in body or "BAD:" in body,
                        "hasGood": "✅" in body or "GOOD:" in body,
                    }
                )
            current_title = line.replace("## ", "").strip()
            current_lines = []
            continue
        current_lines.append(line)

    return rules


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


def best_rule_match(
    pattern_tokens: set[str], rules: list[dict[str, Any]]
) -> dict[str, Any] | None:
    best = None
    best_score = 0.0
    for rule in rules:
        title_tokens = tokenize(rule["title"])
        if not title_tokens:
            continue
        overlap = len(pattern_tokens & title_tokens)
        score = overlap / max(1, len(title_tokens))
        if score > best_score:
            best_score = score
            best = rule
    if best and best_score >= 0.5:
        return best
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze patterns from grouped comments."
    )
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--instruction-files", default="")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
    categories = defaults.get("categories", [])
    instruction_files = defaults.get("instructionFiles", {})
    if args.instruction_files:
        try:
            instruction_files = json.loads(args.instruction_files)
        except json.JSONDecodeError as e:
            raise SystemExit(
                f"Error: --instruction-files must be valid JSON.\n"
                f"Got: {args.instruction_files}\n"
                f"Parse error: {e}"
            ) from None

    rules: list[dict[str, Any]] = []
    for path_str in instruction_files.values():
        rules.extend(extract_rules(Path(path_str)))

    payload = json.loads(Path(args.input_path).read_text(encoding="utf-8"))
    patterns = []
    summary = {"alreadyCovered": 0, "needsStrengthening": 0, "newRules": 0}

    for group in payload.get("commentGroups", []):
        representative = group.get("representative", "")
        occurrences = group.get("occurrences", len(group.get("examples", [])))
        is_red_flag = bool(group.get("isRedFlag"))
        category = classify_category(representative, categories)
        severity = severity_for(category, is_red_flag)
        tokens = tokenize(representative)
        match = best_rule_match(tokens, rules)

        triage = "new-rule"
        suggested_action = "Create a new rule to cover this pattern."
        if match:
            if (
                match["hasDirectives"]
                and match["hasBad"]
                and match["hasGood"]
                and occurrences <= 5
            ):
                triage = "already-covered"
                suggested_action = "No action; existing rule appears sufficient."
            else:
                triage = "needs-strengthening"
                suggested_action = (
                    "Strengthen existing rule with clearer directives or examples."
                )

        if triage == "already-covered":
            summary["alreadyCovered"] += 1
        elif triage == "needs-strengthening":
            summary["needsStrengthening"] += 1
        else:
            summary["newRules"] += 1

        patterns.append(
            {
                "id": group.get("id"),
                "title": representative[:120],
                "description": representative,
                "frequency": occurrences,
                "severity": severity,
                "category": category,
                "isRedFlag": is_red_flag,
                "triage": triage,
                "suggestedAction": suggested_action,
                "matchedRule": match["title"] if match else None,
                "examples": group.get("examples", []),
            }
        )

    output = {
        "analyzedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "summary": {
            "totalPatterns": len(patterns),
            **summary,
        },
        "patterns": patterns,
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote patterns to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
