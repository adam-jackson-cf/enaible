#!/usr/bin/env python3
"""Scan repository for MCP configuration signals."""

import argparse
import json
from pathlib import Path

from shared.context.agentic_readiness.timing import log_phase

SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".next",
    "vendor",
    ".venv",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".gradle",
    "target",
    "bin",
    "obj",
    "coverage",
    ".turbo",
    ".svelte-kit",
    ".cache",
    ".enaible",
}

DIRECT_CANDIDATES = [
    "mcp.json",
    ".mcp.json",
    "mcp.config.json",
    "mcp.config.toml",
    "mcp.config.yaml",
    "mcp.config.yml",
    ".mcp/config.json",
    ".mcp/config.toml",
    ".mcp/config.yaml",
    ".mcp/config.yml",
    ".cursor/mcp.json",
    ".cursor/mcp.yaml",
    ".cursor/mcp.yml",
    ".cursor/mcp.toml",
]


def scan_mcp(root: Path) -> list[str]:
    matches: list[str] = []
    for rel in DIRECT_CANDIDATES:
        candidate = root / rel
        if candidate.exists():
            matches.append(str(candidate))

    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_dir():
            if path.name == ".mcp":
                matches.append(str(path))
            continue
        if "mcp" in path.name.lower() and path.suffix.lower() in {
            ".json",
            ".toml",
            ".yaml",
            ".yml",
        }:
            matches.append(str(path))

    return sorted(set(matches))


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan for MCP configs")
    parser.add_argument("target", help="Absolute path to analyzed target")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    metadata = {"target": str(root), "artifact_root": str(artifact_root)}
    with log_phase("helper:mcp_scan", metadata):
        matches = scan_mcp(root)
        (artifact_root / "mcp-scan.json").write_text(
            json.dumps({"matches": matches, "mcp_present": bool(matches)}, indent=2)
        )


if __name__ == "__main__":
    main()
