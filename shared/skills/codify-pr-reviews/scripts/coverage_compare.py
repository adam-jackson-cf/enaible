#!/usr/bin/env python
"""Compare patterns against tooling inventory and system rule documents."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rule_utils import tokenize
from schema_utils import validate_patterns

TOOL_MATRIX = (
    {
        "tool": "semgrep",
        "categories": {"security", "api-design"},
        "keywords": {"sql", "xss", "csrf", "jwt", "token", "secret", "auth"},
        "action": "Add or update Semgrep rule",
    },
    {
        "tool": "ruff",
        "categories": {"code-style", "type-safety"},
        "keywords": {"unused", "import", "typing", "flake8", "lint"},
        "action": "Add/adjust Ruff rule",
    },
    {
        "tool": "eslint",
        "categories": {"frontend", "react-patterns", "accessibility", "code-style"},
        "keywords": {"react", "component", "jsx", "hook", "aria", "eslint"},
        "action": "Add ESLint rule or plugin",
    },
    {
        "tool": "prettier",
        "categories": {"code-style"},
        "keywords": {"format", "style"},
        "action": "Configure Prettier formatting",
    },
    {
        "tool": "custom-analyzer",
        "categories": {"performance", "database", "testing"},
        "keywords": {"n+1", "query", "migration", "test", "coverage"},
        "action": "Extend Enaible analyzer or write custom script",
    },
)


def best_rule_match(
    pattern_id: str | None, pattern_tokens: set[str], rules: list[dict[str, Any]]
) -> dict[str, Any] | None:
    if pattern_id:
        for rule in rules:
            if rule.get("ruleId") and rule.get("ruleId") == pattern_id:
                return rule
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


def keyword_hits(text: str, keywords: Iterable[str]) -> set[str]:
    lowered = text.lower()
    return {word for word in keywords if word in lowered}


def deterministic_options(pattern: dict[str, Any]) -> list[dict[str, str]]:
    description = pattern.get("description", "")
    category = (pattern.get("category") or "general").lower()
    options: list[dict[str, str]] = []
    for rule in TOOL_MATRIX:
        category_match = category in rule["categories"]
        keyword_match = keyword_hits(description, rule["keywords"])
        if category_match or keyword_match:
            reason_bits = []
            if category_match:
                reason_bits.append(f"category '{category}'")
            if keyword_match:
                reason_bits.append(f"keywords: {', '.join(sorted(keyword_match))}")
            options.append(
                {
                    "tool": rule["tool"],
                    "action": rule["action"],
                    "reason": "; ".join(reason_bits),
                }
            )
    return options


def tooling_status(
    tool_name: str, tool_inventory: dict[str, Any], pattern_tokens: set[str]
) -> dict[str, Any]:
    tool = tool_inventory.get("tools", {}).get(tool_name, {})
    files = tool.get("files", [])
    if not files:
        return {"tool": tool_name, "status": "not-configured", "evidence": []}

    candidates: list[str] = []
    if tool_name == "semgrep":
        candidates = tool.get("ruleIds", [])
    elif tool_name == "ruff":
        for config in tool.get("configs", []):
            for key in ("select", "extendSelect"):
                candidates.extend(config.get(key, []))
    elif tool_name == "eslint":
        for config in tool.get("configs", []):
            candidates.extend(config.get("rules", []))

    token_hits = [rule for rule in candidates if tokenize(rule) & pattern_tokens]
    if token_hits:
        return {
            "tool": tool_name,
            "status": "possible-match",
            "matchedRules": sorted(set(token_hits)),
            "evidence": files,
        }
    return {"tool": tool_name, "status": "configured-no-match", "evidence": files}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare patterns against tooling configs and doc rules."
    )
    parser.add_argument("--patterns-path", required=True)
    parser.add_argument("--tooling-inventory-path", required=True)
    parser.add_argument("--doc-rules-path", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()

    patterns_payload = json.loads(Path(args.patterns_path).read_text(encoding="utf-8"))
    validate_patterns(patterns_payload)
    patterns = patterns_payload.get("patterns", [])
    tooling_inventory = json.loads(
        Path(args.tooling_inventory_path).read_text(encoding="utf-8")
    )
    doc_rules_payload = json.loads(
        Path(args.doc_rules_path).read_text(encoding="utf-8")
    )
    doc_rules = doc_rules_payload.get("rules", [])
    results = []
    for pattern in patterns:
        pattern_id = pattern.get("id")
        description = pattern.get("description", "")
        tokens = tokenize(description)
        doc_match = best_rule_match(pattern_id, tokens, doc_rules)
        doc_coverage = "new-rule"
        if doc_match:
            if (
                doc_match.get("hasDirectives")
                and doc_match.get("hasBad")
                and doc_match.get("hasGood")
            ):
                doc_coverage = "already-covered"
            else:
                doc_coverage = "needs-strengthening"

        options = deterministic_options(pattern)
        tool_statuses = [
            tooling_status(option["tool"], tooling_inventory, tokens)
            for option in options
        ]

        enforcement_suggestion = "docs"
        if options:
            enforcement_suggestion = "tooling"
            if doc_coverage != "new-rule":
                enforcement_suggestion = "both"

        results.append(
            {
                "id": pattern_id,
                "title": pattern.get("title"),
                "description": description,
                "category": pattern.get("category"),
                "frequency": pattern.get("frequency"),
                "docCoverage": {
                    "status": doc_coverage,
                    "matchedRule": doc_match.get("title") if doc_match else None,
                    "matchedRuleId": doc_match.get("ruleId") if doc_match else None,
                    "source": doc_match.get("sourcePath") if doc_match else None,
                },
                "toolingCoverage": tool_statuses,
                "deterministicOptions": options,
                "enforcementSuggestion": enforcement_suggestion,
            }
        )

    summary = {
        "total": len(results),
        "docCovered": sum(
            1 for item in results if item["docCoverage"]["status"] == "already-covered"
        ),
        "needsStrengthening": sum(
            1
            for item in results
            if item["docCoverage"]["status"] == "needs-strengthening"
        ),
        "newRules": sum(
            1 for item in results if item["docCoverage"]["status"] == "new-rule"
        ),
        "toolingOptions": sum(1 for item in results if item["deterministicOptions"]),
    }

    output = {
        "comparedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "summary": summary,
        "patterns": results,
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote coverage comparison to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
