#!/usr/bin/env python
"""Inventory existing system rule documents for coverage comparison."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rule_utils import extract_rules


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory system rule documents for coverage checks."
    )
    parser.add_argument("--instruction-files", default="")
    parser.add_argument("--output-path", required=True)
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
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
    for key, path_str in instruction_files.items():
        path = Path(path_str)
        for rule in extract_rules(path):
            rules.append({**rule, "source": key, "sourcePath": str(path)})

    output = {
        "collectedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "ruleCount": len(rules),
        "rules": rules,
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Wrote doc rules inventory to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
