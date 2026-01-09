#!/usr/bin/env python
"""Lightweight schema validation helpers for research artifacts."""

from __future__ import annotations

from typing import Any


def _ensure(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _ensure_keys(payload: dict[str, Any], keys: list[str], label: str) -> None:
    for key in keys:
        _ensure(key in payload, f"{label} missing required key: {key}")


def validate_requirements(payload: dict[str, Any]) -> None:
    _ensure_keys(
        payload,
        [
            "runId",
            "startedAt",
            "artifactRoot",
            "objective",
            "scope",
            "outputFormat",
            "decisionContext",
            "onlineResearch",
            "questions",
        ],
        "requirements",
    )
    _ensure(
        payload["onlineResearch"] in {"allowed", "disallowed"},
        "onlineResearch must be allowed/disallowed",
    )
    _ensure(
        isinstance(payload["questions"], list) and payload["questions"],
        "requirements.questions must be a non-empty list",
    )
    for question in payload["questions"]:
        _ensure(
            isinstance(question, dict), "requirements.questions entries must be objects"
        )
        _ensure(
            "id" in question and "text" in question,
            "Each question must include id and text",
        )


def validate_domain_map(payload: dict[str, Any]) -> None:
    _ensure(
        "domains" in payload and isinstance(payload["domains"], dict),
        "domain map must include domains object",
    )
    for name, domain in payload["domains"].items():
        _ensure(isinstance(domain, dict), f"domain '{name}' must be an object")
        _ensure(
            "keywords" in domain and isinstance(domain["keywords"], list),
            f"domain '{name}' must include keywords list",
        )


def validate_domain_plan(payload: dict[str, Any]) -> None:
    _ensure_keys(payload, ["plannedAt", "questions"], "domain plan")
    _ensure(
        isinstance(payload["questions"], list) and payload["questions"],
        "domain plan questions must be a non-empty list",
    )
    for question in payload["questions"]:
        _ensure(
            "id" in question and "text" in question,
            "domain plan questions must include id and text",
        )
        _ensure(
            "primaryDomain" in question, "domain plan question missing primaryDomain"
        )


def validate_recency_policy(payload: dict[str, Any]) -> None:
    _ensure(
        "policies" in payload and isinstance(payload["policies"], dict),
        "recency policy must include policies object",
    )
    for name, policy in payload["policies"].items():
        _ensure(isinstance(policy, dict), f"recency policy '{name}' must be an object")


def validate_search_log(payload: dict[str, Any]) -> None:
    _ensure(
        "searches" in payload and isinstance(payload["searches"], list),
        "search-log must include searches list",
    )


def validate_sources(payload: dict[str, Any]) -> None:
    _ensure(
        "sources" in payload and isinstance(payload["sources"], list),
        "sources must include sources list",
    )
    for source in payload["sources"]:
        _ensure("id" in source, "source missing id")
        _ensure("questionId" in source, "source missing questionId")
        _ensure("url" in source, "source missing url")
        _ensure("title" in source, "source missing title")
        _ensure("sourceType" in source, "source missing sourceType")
        _ensure("origin" in source, "source missing origin")
        snapshot = source.get("snapshot")
        if snapshot is not None:
            _ensure(isinstance(snapshot, dict), "source snapshot must be an object")


def validate_evidence(payload: dict[str, Any]) -> None:
    _ensure("evidenceVersion" in payload, "evidence missing evidenceVersion")
    _ensure(
        isinstance(payload.get("evidenceVersion"), str),
        "evidenceVersion must be a string",
    )
    validate_search_log({"searches": payload.get("searches", [])})
    validate_sources({"sources": payload.get("sources", [])})


def validate_validation_report(payload: dict[str, Any]) -> None:
    _ensure_keys(payload, ["validatedAt", "status", "questions"], "validation report")
    _ensure(
        payload["status"] in {"pass", "fail"}, "validation.status must be pass or fail"
    )


def validate_analysis(payload: dict[str, Any]) -> None:
    _ensure_keys(
        payload,
        [
            "analysisAt",
            "executiveSummary",
            "findings",
            "insights",
            "recommendations",
            "limitations",
        ],
        "analysis",
    )
    _ensure(
        isinstance(payload["findings"], list) and payload["findings"],
        "analysis.findings must be a non-empty list",
    )
    _ensure(
        isinstance(payload["insights"], list) and payload["insights"],
        "analysis.insights must be a non-empty list",
    )
    _ensure(
        isinstance(payload["recommendations"], list) and payload["recommendations"],
        "analysis.recommendations must be a non-empty list",
    )
    for finding in payload["findings"]:
        _ensure(
            finding.get("confidence") in {"high", "medium", "low"},
            "finding.confidence must be high, medium, or low",
        )
        _ensure(
            finding.get("importance") in {"key", "supporting", "background"},
            "finding.importance must be key, supporting, or background",
        )
    for recommendation in payload["recommendations"]:
        _ensure(
            recommendation.get("priority") in {"high", "medium", "low"},
            "recommendation.priority must be high, medium, or low",
        )


def validate_citation_report(payload: dict[str, Any]) -> None:
    _ensure_keys(payload, ["checkedAt", "status", "items"], "citation report")
    _ensure(
        payload["status"] in {"pass", "fail"},
        "citation-report.status must be pass or fail",
    )
    _ensure(isinstance(payload["items"], list), "citation report items must be list")
