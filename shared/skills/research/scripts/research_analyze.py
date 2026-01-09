#!/usr/bin/env python
"""Assemble analysis.json from structured analysis input."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import validate_analysis


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build analysis.json from input.")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-path", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = load_json(Path(args.input_path))
    if "analysisAt" not in payload or not payload.get("analysisAt"):
        payload["analysisAt"] = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    validate_analysis(payload)
    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote analysis to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
