#!/usr/bin/env python
"""Inventory deterministic tooling configs and rule identifiers."""

from __future__ import annotations

import argparse
import json
import re
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def find_files(root: Path, patterns: list[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        files.extend(root.glob(pattern))
    return sorted({path for path in files if path.is_file()})


def parse_semgrep(paths: list[Path]) -> dict[str, Any]:
    rule_ids: list[str] = []
    for path in paths:
        for line in read_text(path).splitlines():
            match = re.match(r"\s*id:\s*([\w\-.]+)", line)
            if match:
                rule_ids.append(match.group(1))
    return {"files": [str(path) for path in paths], "ruleIds": sorted(set(rule_ids))}


def parse_ruff(paths: list[Path]) -> dict[str, Any]:
    parsed: list[dict[str, Any]] = []
    for path in paths:
        try:
            data = tomllib.loads(read_text(path))
        except tomllib.TOMLDecodeError:
            parsed.append({"file": str(path), "error": "toml-parse-failed"})
            continue
        tool = data.get("tool", {})
        ruff = tool.get("ruff", {})
        parsed.append(
            {
                "file": str(path),
                "select": ruff.get("select", []),
                "ignore": ruff.get("ignore", []),
                "extendSelect": ruff.get("extend-select", []),
                "extendIgnore": ruff.get("extend-ignore", []),
            }
        )
    return {"files": [str(path) for path in paths], "configs": parsed}


def parse_eslint(paths: list[Path], package_json: Path | None) -> dict[str, Any]:
    configs: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix != ".json":
            configs.append(
                {
                    "file": str(path),
                    "rules": [],
                    "note": "config-present-unparsed",
                }
            )
            continue
        try:
            payload = json.loads(read_text(path))
        except json.JSONDecodeError:
            configs.append({"file": str(path), "error": "json-parse-failed"})
            continue
        configs.append(
            {
                "file": str(path),
                "rules": sorted(payload.get("rules", {}).keys()),
            }
        )
    if package_json and package_json.exists():
        try:
            package = json.loads(read_text(package_json))
            eslint_config = package.get("eslintConfig")
            if eslint_config:
                configs.append(
                    {
                        "file": str(package_json),
                        "rules": sorted(eslint_config.get("rules", {}).keys()),
                    }
                )
        except json.JSONDecodeError:
            configs.append({"file": str(package_json), "error": "json-parse-failed"})
    return {"files": [str(path) for path in paths], "configs": configs}


def parse_prettier(paths: list[Path], package_json: Path | None) -> dict[str, Any]:
    configs = [str(path) for path in paths]
    if package_json and package_json.exists():
        configs.append(str(package_json))
    return {"files": configs}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inventory deterministic tooling configs."
    )
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    package_json = root / "package.json"

    semgrep_files = find_files(
        root,
        [
            ".semgrep.yml",
            ".semgrep.yaml",
            "semgrep.yml",
            "semgrep.yaml",
            ".semgrep/*.yml",
            ".semgrep/*.yaml",
        ],
    )
    ruff_files = find_files(root, ["pyproject.toml", "ruff.toml", ".ruff.toml"])
    eslint_files = find_files(
        root,
        [
            ".eslintrc",
            ".eslintrc.json",
            ".eslintrc.cjs",
            ".eslintrc.js",
            ".eslintrc.yaml",
            ".eslintrc.yml",
            "eslint.config.js",
            "eslint.config.cjs",
        ],
    )
    prettier_files = find_files(
        root,
        [
            ".prettierrc",
            ".prettierrc.json",
            ".prettierrc.yaml",
            ".prettierrc.yml",
            "prettier.config.js",
            "prettier.config.cjs",
        ],
    )

    inventory = {
        "collectedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "tools": {
            "semgrep": parse_semgrep(semgrep_files),
            "ruff": parse_ruff(ruff_files),
            "eslint": parse_eslint(eslint_files, package_json),
            "prettier": parse_prettier(prettier_files, package_json),
        },
    }

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    print(f"Wrote tooling inventory to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
