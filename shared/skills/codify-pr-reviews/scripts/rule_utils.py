#!/usr/bin/env python
"""Shared helpers for rule extraction and tokenization."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

RULE_ID_RE = re.compile(r"^\s*Rule[- ]ID:\s*(.+)", re.IGNORECASE)


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def extract_rule_id(lines: list[str]) -> str | None:
    for line in lines:
        match = RULE_ID_RE.match(line)
        if match:
            return match.group(1).strip()
    return None


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
                        "ruleId": extract_rule_id(current_lines),
                        "hasDirectives": any(
                            text.strip().startswith("- ALWAYS")
                            or text.strip().startswith("- NEVER")
                            for text in current_lines
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
