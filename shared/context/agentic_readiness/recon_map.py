#!/usr/bin/env python3
"""Generate recon and repo map artifacts for agentic readiness."""

import argparse
import json
from pathlib import Path

DEFAULT_EXCLUSIONS = [
    "dist/",
    "build/",
    "node_modules/",
    "__pycache__/",
    ".next/",
    "vendor/",
    ".venv/",
    ".mypy_cache/",
    ".ruff_cache/",
    ".pytest_cache/",
    ".gradle/",
    "target/",
    "bin/",
    "obj/",
    "coverage/",
    ".turbo/",
    ".svelte-kit/",
    ".cache/",
    ".enaible/artifacts/",
]


def detect_languages(root: Path) -> list[str]:
    def has_glob(pattern: str) -> bool:
        return any(root.glob(pattern))

    languages: list[str] = []
    if (root / "pyproject.toml").exists() or has_glob("requirements*.txt"):
        languages.append("Python")
    if (root / "package.json").exists() or (root / "tsconfig.json").exists():
        languages.append("TypeScript")
    if (root / "go.mod").exists():
        languages.append("Go")
    if (root / "Cargo.toml").exists():
        languages.append("Rust")
    if has_glob("*.sln") or has_glob("*.csproj"):
        languages.append("C#")
    return languages


def build_repo_map(root: Path) -> list[dict[str, str]]:
    category_map = {
        "apps": {"app", "apps", "api", "server", "services", "service", "backend"},
        "frontend": {"web", "frontend", "client", "ui"},
        "libs": {"lib", "libs", "pkg", "packages", "shared", "common", "core"},
        "tests": {
            "test",
            "tests",
            "__tests__",
            "spec",
            "specs",
            "integration",
            "e2e",
            "smoke",
        },
        "docs": {"docs", "doc", "documentation", "handbook", "runbooks", "guides"},
    }

    entries: list[dict[str, str]] = []
    for path in sorted(p for p in root.iterdir() if p.is_dir()):
        category = "other"
        for key, names in category_map.items():
            if path.name.lower() in names:
                category = key
                break
        entries.append({"path": str(path), "category": category})
    return entries


def write_json(path: Path, payload: dict | list) -> None:
    path.write_text(json.dumps(payload, indent=2))


def generate_recon(root: Path, artifact_root: Path) -> None:
    write_json(
        artifact_root / "recon.json",
        {"languages": detect_languages(root), "exclusions": DEFAULT_EXCLUSIONS},
    )
    write_json(artifact_root / "repo-map.json", {"entries": build_repo_map(root)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate recon artifacts")
    parser.add_argument("target", help="Absolute path to analyzed target")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    generate_recon(root, artifact_root)


if __name__ == "__main__":
    main()
