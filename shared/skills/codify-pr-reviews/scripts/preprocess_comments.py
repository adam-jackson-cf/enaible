#!/usr/bin/env python3
"""Deduplicate and group PR comments."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_red_flags(path: Path) -> list[str]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [flag.lower() for flag in data.get("redFlags", [])]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def flatten_comments(payload: dict[str, Any]) -> list[dict[str, Any]]:
    comments: list[dict[str, Any]] = []
    for pr in payload.get("pullRequests", []):
        for comment in pr.get("comments", []):
            comments.append(
                {
                    "pr": pr.get("number"),
                    "body": comment.get("body", ""),
                    "author": comment.get("author"),
                    "path": comment.get("path"),
                    "line": comment.get("line"),
                }
            )
    if comments:
        return comments
    return payload.get("comments", [])


def group_exact(comments: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for comment in comments:
        key = normalize(comment.get("body", ""))
        groups[key].append(comment)
    return list(groups.values())


def group_by_similarity(
    groups: list[list[dict[str, Any]]], threshold: float
) -> list[list[dict[str, Any]]]:
    clustered: list[list[dict[str, Any]]] = []
    rep_tokens: list[set[str]] = []

    for group in groups:
        rep = normalize(group[0].get("body", ""))
        tokens = tokenize(rep)
        placed = False
        for idx, existing in enumerate(clustered):
            if jaccard(tokens, rep_tokens[idx]) >= threshold:
                existing.extend(group)
                rep_tokens[idx] = tokenize(normalize(existing[0].get("body", "")))
                placed = True
                break
        if not placed:
            clustered.append(list(group))
            rep_tokens.append(tokens)

    return clustered


def main() -> int:
    parser = argparse.ArgumentParser(description="Group and deduplicate PR comments.")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--red-flags-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--min-occurrences", type=int, default=None)
    parser.add_argument("--semantic-threshold", type=float, default=None)
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
    min_occurrences = args.min_occurrences or defaults.get("defaultMinOccurrences", 3)
    semantic_threshold = args.semantic_threshold or defaults.get(
        "defaultSemanticThreshold", 0.85
    )

    payload = json.loads(Path(args.input_path).read_text(encoding="utf-8"))
    comments = flatten_comments(payload)
    red_flags = load_red_flags(Path(args.red_flags_path))

    exact_groups = group_exact(comments)
    fuzzy_threshold = min(0.95, semantic_threshold + 0.05)
    fuzzy_groups = group_by_similarity(exact_groups, fuzzy_threshold)
    semantic_groups = group_by_similarity(fuzzy_groups, semantic_threshold)

    comment_groups = []
    kept = 0
    for group in semantic_groups:
        representative = group[0].get("body", "").strip()
        occurrences = len(group)
        normalized = normalize(representative)
        is_red_flag = any(flag in normalized for flag in red_flags)
        if occurrences < min_occurrences and not is_red_flag:
            continue
        kept += occurrences
        comment_groups.append(
            {
                "id": re.sub(r"[^a-z0-9]+", "-", normalized).strip("-")[:40],
                "representative": representative,
                "occurrences": occurrences,
                "isRedFlag": is_red_flag,
                "examples": group[:5],
            }
        )

    output = {
        "processedAt": datetime.utcnow().isoformat() + "Z",
        "inputComments": len(comments),
        "outputGroups": len(comment_groups),
        "keptComments": kept,
        "filteredOut": len(comments) - kept,
        "commentGroups": comment_groups,
        "stats": {
            "exactGroups": len(exact_groups),
            "fuzzyGroups": len(fuzzy_groups),
            "semanticGroups": len(semantic_groups),
            "minOccurrences": min_occurrences,
            "semanticThreshold": semantic_threshold,
        },
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote grouped comments to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
