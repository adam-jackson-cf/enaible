#!/usr/bin/env python
"""Log research searches and sources for auditability."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import validate_evidence

SOURCE_TYPES = {
    "industry-report",
    "financial",
    "government",
    "news",
    "company",
    "official-docs",
    "repository",
    "academic",
    "community",
    "survey",
    "support",
    "review",
    "other",
}


EVIDENCE_VERSION = "2026-01-09"


def load_evidence(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "evidenceVersion": EVIDENCE_VERSION,
            "createdAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "searches": [],
            "sources": [],
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    validate_evidence(payload)
    return payload


def mark_normalization_stale(payload: dict[str, Any]) -> None:
    if "normalization" in payload:
        payload.pop("normalization")


def write_log(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_id(prefix: str, count: int) -> str:
    return f"{prefix}-{count:03d}"


def resolve_path(artifact_root: str | None, override: str | None) -> Path:
    if override:
        return Path(override)
    if not artifact_root:
        raise SystemExit("Provide --artifact-root or explicit path.")
    return Path(artifact_root) / "evidence.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Log searches and sources.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search = subparsers.add_parser("search", help="Log a search query.")
    search.add_argument("--artifact-root")
    search.add_argument("--evidence-path")
    search.add_argument("--question-id", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--engine", required=True)
    search.add_argument("--filters")
    search.add_argument("--result-count", type=int)
    search.add_argument("--notes")

    source = subparsers.add_parser("source", help="Log a source record.")
    source.add_argument("--artifact-root")
    source.add_argument("--evidence-path")
    source.add_argument("--question-id", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--title", required=True)
    source.add_argument("--source-type", required=True)
    source.add_argument("--published-date")
    source.add_argument("--undated-reason")
    source.add_argument("--retrieved-at")
    source.add_argument("--origin", required=True, choices=["engagement", "prior"])
    source.add_argument("--search-id")
    source.add_argument("--citation-label")
    source.add_argument("--publisher")
    source.add_argument("--notes")

    batch = subparsers.add_parser("batch", help="Import sources from CSV or JSON.")
    batch.add_argument("--artifact-root")
    batch.add_argument("--evidence-path")
    batch.add_argument("--input-path", required=True)
    batch.add_argument("--format", choices=["csv", "json"])

    snapshot = subparsers.add_parser("snapshot", help="Attach a metadata snapshot.")
    snapshot.add_argument("--artifact-root")
    snapshot.add_argument("--evidence-path")
    snapshot.add_argument("--source-id", required=True)
    snapshot.add_argument("--snapshot-title")
    snapshot.add_argument("--snapshot-date")
    snapshot.add_argument("--snapshot-notes")
    snapshot.add_argument("--observed-at")

    return parser.parse_args()


def log_search(args: argparse.Namespace) -> int:
    evidence_path = resolve_path(args.artifact_root, args.evidence_path)
    payload = load_evidence(evidence_path)
    mark_normalization_stale(payload)
    entry_id = build_id("search", len(payload["searches"]) + 1)
    payload["searches"].append(
        {
            "id": entry_id,
            "questionId": args.question_id,
            "query": args.query,
            "engine": args.engine,
            "filters": args.filters,
            "resultCount": args.result_count,
            "notes": args.notes,
            "searchedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        }
    )
    payload["updatedAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_evidence(payload)
    write_log(evidence_path, payload)
    print(entry_id)
    return 0


def normalize_source_entry(entry: dict[str, Any]) -> dict[str, Any]:
    source_type = entry.get("sourceType")
    if source_type not in SOURCE_TYPES:
        raise SystemExit(
            f"source-type must be one of: {', '.join(sorted(SOURCE_TYPES))}"
        )
    if not entry.get("publishedDate") and not entry.get("undatedReason"):
        raise SystemExit("Provide publishedDate or undatedReason for sources.")
    if entry.get("origin") not in {"engagement", "prior"}:
        raise SystemExit("origin must be engagement or prior.")
    return entry


def log_source(args: argparse.Namespace) -> int:
    normalize_source_entry(
        {
            "sourceType": args.source_type,
            "publishedDate": args.published_date,
            "undatedReason": args.undated_reason,
            "origin": args.origin,
        }
    )

    evidence_path = resolve_path(args.artifact_root, args.evidence_path)
    payload = load_evidence(evidence_path)
    mark_normalization_stale(payload)
    entry_id = build_id("src", len(payload["sources"]) + 1)
    retrieved_at = args.retrieved_at or datetime.now(UTC).isoformat().replace(
        "+00:00", "Z"
    )
    payload["sources"].append(
        {
            "id": entry_id,
            "questionId": args.question_id,
            "url": args.url,
            "title": args.title,
            "publisher": args.publisher,
            "sourceType": args.source_type,
            "publishedDate": args.published_date,
            "undatedReason": args.undated_reason,
            "retrievedAt": retrieved_at,
            "origin": args.origin,
            "searchId": args.search_id,
            "citationLabel": args.citation_label,
            "notes": args.notes,
        }
    )
    payload["updatedAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_evidence(payload)
    write_log(evidence_path, payload)
    print(entry_id)
    return 0


def load_batch_entries(path: Path, fmt: str | None) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Batch file not found: {path}")
    format_hint = fmt or path.suffix.lstrip(".").lower()
    if format_hint == "json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise SystemExit("JSON batch must be a list of source entries.")
        return payload
    if format_hint == "csv":
        entries: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                entries.append({key: value or None for key, value in row.items()})
        return entries
    raise SystemExit("Batch format must be csv or json.")


def add_batch_sources(args: argparse.Namespace) -> int:
    evidence_path = resolve_path(args.artifact_root, args.evidence_path)
    payload = load_evidence(evidence_path)
    mark_normalization_stale(payload)
    entries = load_batch_entries(Path(args.input_path), args.format)
    for entry in entries:
        normalized = normalize_source_entry(
            {
                "sourceType": entry.get("sourceType"),
                "publishedDate": entry.get("publishedDate"),
                "undatedReason": entry.get("undatedReason"),
                "origin": entry.get("origin"),
            }
        )
        entry_id = build_id("src", len(payload["sources"]) + 1)
        payload["sources"].append(
            {
                "id": entry_id,
                "questionId": entry.get("questionId"),
                "url": entry.get("url"),
                "title": entry.get("title"),
                "publisher": entry.get("publisher"),
                "sourceType": normalized.get("sourceType"),
                "publishedDate": entry.get("publishedDate"),
                "undatedReason": entry.get("undatedReason"),
                "retrievedAt": entry.get("retrievedAt")
                or datetime.now(UTC).isoformat().replace("+00:00", "Z"),
                "origin": normalized.get("origin"),
                "searchId": entry.get("searchId"),
                "citationLabel": entry.get("citationLabel"),
                "notes": entry.get("notes"),
            }
        )
    payload["updatedAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_evidence(payload)
    write_log(evidence_path, payload)
    print(f"Imported {len(entries)} sources.")
    return 0


def attach_snapshot(args: argparse.Namespace) -> int:
    evidence_path = resolve_path(args.artifact_root, args.evidence_path)
    payload = load_evidence(evidence_path)
    mark_normalization_stale(payload)
    if not args.snapshot_title and not args.snapshot_date and not args.snapshot_notes:
        raise SystemExit("Provide at least one snapshot field.")
    observed_at = args.observed_at or datetime.now(UTC).isoformat().replace(
        "+00:00", "Z"
    )
    snapshot = {"observedAt": observed_at}
    if args.snapshot_title:
        snapshot["title"] = args.snapshot_title
    if args.snapshot_date:
        snapshot["publishedDate"] = args.snapshot_date
    if args.snapshot_notes:
        snapshot["notes"] = args.snapshot_notes
    updated = False
    for source in payload["sources"]:
        if source.get("id") == args.source_id:
            source["snapshot"] = snapshot
            updated = True
            break
    if not updated:
        raise SystemExit(f"Source id not found: {args.source_id}")
    payload["updatedAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_evidence(payload)
    write_log(evidence_path, payload)
    print(args.source_id)
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "search":
        return log_search(args)
    if args.command == "source":
        return log_source(args)
    if args.command == "batch":
        return add_batch_sources(args)
    if args.command == "snapshot":
        return attach_snapshot(args)
    raise SystemExit("Unknown command.")


if __name__ == "__main__":
    raise SystemExit(main())
