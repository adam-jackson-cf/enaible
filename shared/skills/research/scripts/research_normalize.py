#!/usr/bin/env python
"""Normalize evidence sources (publisher names, URLs, deduplication)."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlsplit, urlunsplit

from schema_utils import validate_evidence


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_url(url: str) -> str:
    parts = urlsplit(url)
    scheme = parts.scheme.lower() or "https"
    netloc = parts.netloc.lower()
    path = parts.path or "/"
    query_items = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        if key.lower().startswith("utm_"):
            continue
        if key.lower() in {"ref", "source"}:
            continue
        query_items.append((key, value))
    query = "&".join(f"{key}={value}" if value else key for key, value in query_items)
    normalized = urlunsplit((scheme, netloc, path.rstrip("/"), query, ""))
    return normalized or url


def normalize_publisher(
    publisher: str | None, url: str, mapping: dict[str, str]
) -> str:
    if publisher:
        key = publisher.strip().lower()
        if key in mapping:
            return mapping[key]
        return publisher.strip()
    host = urlsplit(url).netloc
    key = host.lower()
    if key in mapping:
        return mapping[key]
    return host or "Unknown publisher"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize evidence sources.")
    parser.add_argument("--evidence-path", required=True)
    parser.add_argument("--publisher-map-path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    evidence_path = Path(args.evidence_path)
    evidence = load_json(evidence_path)
    validate_evidence(evidence)

    publisher_map_path = args.publisher_map_path or str(
        Path(__file__).resolve().parents[1] / "assets" / "publisher-map.json"
    )
    publisher_map = load_json(Path(publisher_map_path))
    mapping = {
        key.lower(): value
        for key, value in (publisher_map.get("publishers") or {}).items()
    }

    seen: dict[str, str] = {}
    duplicates: list[dict[str, Any]] = []
    normalized_sources: list[dict[str, Any]] = []

    for source in evidence.get("sources", []):
        url = source.get("url")
        if not url:
            raise SystemExit("Source is missing url.")
        canonical = normalize_url(url)
        source["canonicalUrl"] = canonical
        source["publisher"] = normalize_publisher(
            source.get("publisher"), canonical, mapping
        )
        if canonical in seen:
            kept_id = seen[canonical]
            duplicates.append(
                {
                    "canonicalUrl": canonical,
                    "keptId": kept_id,
                    "removedIds": [source.get("id")],
                }
            )
            continue
        seen[canonical] = source.get("id")
        normalized_sources.append(source)

    evidence["sources"] = normalized_sources
    evidence["normalization"] = {
        "normalizedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "duplicates": duplicates,
        "publisherMapVersion": publisher_map.get("version"),
    }
    evidence["updatedAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_evidence(evidence)

    evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Normalized evidence at {evidence_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
