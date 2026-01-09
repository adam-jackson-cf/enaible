#!/usr/bin/env python
"""Minimal schema validation helpers for codify-pr-reviews artifacts."""

from __future__ import annotations

from typing import Any


def _error(message: str) -> None:
    raise SystemExit(message)


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        _error(message)


def _ensure_type(value: Any, expected: type, message: str) -> None:
    if not isinstance(value, expected):
        _error(message)


def validate_patterns(payload: dict[str, Any]) -> None:
    _ensure_type(payload, dict, "patterns.json must be a JSON object.")
    patterns = payload.get("patterns")
    _ensure(isinstance(patterns, list), "patterns.json must include a patterns list.")
    for pattern in patterns:
        _ensure(isinstance(pattern, dict), "patterns must be objects.")
        for key in ("id", "title", "description", "category"):
            _ensure(
                isinstance(pattern.get(key), str), f"patterns[{key}] must be string."
            )
        _ensure(
            isinstance(pattern.get("frequency"), int),
            "patterns.frequency must be integer.",
        )


def validate_coverage(payload: dict[str, Any]) -> None:
    _ensure_type(payload, dict, "coverage.json must be a JSON object.")
    patterns = payload.get("patterns")
    _ensure(isinstance(patterns, list), "coverage.json must include a patterns list.")
    for pattern in patterns:
        _ensure(isinstance(pattern, dict), "coverage patterns must be objects.")
        _ensure(
            isinstance(pattern.get("id"), str), "coverage.pattern.id must be string."
        )
        doc = pattern.get("docCoverage")
        _ensure(isinstance(doc, dict), "coverage.docCoverage must be object.")
        _ensure(
            isinstance(doc.get("status"), str),
            "coverage.docCoverage.status must be string.",
        )
        _ensure(
            isinstance(pattern.get("toolingCoverage"), list),
            "coverage.toolingCoverage must be list.",
        )
        _ensure(
            isinstance(pattern.get("enforcementSuggestion"), str),
            "coverage.enforcementSuggestion must be string.",
        )


def validate_approved_enforcement(payload: dict[str, Any]) -> None:
    _ensure_type(payload, dict, "approved-enforcement.json must be a JSON object.")
    patterns = payload.get("patterns")
    _ensure(
        isinstance(patterns, list),
        "approved-enforcement.json must include a patterns list.",
    )
    for pattern in patterns:
        _ensure(isinstance(pattern, dict), "approved patterns must be objects.")
        _ensure(isinstance(pattern.get("id"), str), "approved.id must be string.")
        decision = pattern.get("decision")
        _ensure(isinstance(decision, dict), "approved.decision must be object.")
        enforcement = decision.get("enforcementPath")
        _ensure(
            enforcement in {"tooling", "docs", "both", "skip"},
            "decision.enforcementPath must be tooling|docs|both|skip.",
        )
        action = decision.get("action")
        _ensure(
            action in {"create", "strengthen", "skip"},
            "decision.action must be create|strengthen|skip.",
        )
        if enforcement in {"tooling", "both"}:
            _ensure(
                isinstance(decision.get("toolingAction"), str),
                "decision.toolingAction required for tooling/both.",
            )
        if enforcement in {"docs", "both"}:
            _ensure(
                action in {"create", "strengthen"},
                "decision.action must be create/strengthen for docs/both.",
            )


def validate_doc_patterns(payload: dict[str, Any]) -> None:
    _ensure_type(payload, dict, "doc-patterns.json must be a JSON object.")
    patterns = payload.get("patterns")
    _ensure(isinstance(patterns, list), "doc-patterns.json must include patterns.")
    for pattern in patterns:
        _ensure(isinstance(pattern, dict), "doc-patterns entries must be objects.")
        _ensure(isinstance(pattern.get("id"), str), "doc-patterns.id must be string.")
        _ensure(
            isinstance(pattern.get("action"), str),
            "doc-patterns.action must be string.",
        )
