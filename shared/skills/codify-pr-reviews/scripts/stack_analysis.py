#!/usr/bin/env python
"""Detect stack signals and generate red-flag patterns."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def read_requirements(path: Path) -> set[str]:
    packages: set[str] = set()
    if not path.exists():
        return packages
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        name = re.split(r"[<>=!~]", stripped, maxsplit=1)[0].strip()
        if name:
            packages.add(name.lower())
    return packages


def read_package_json(path: Path) -> set[str]:
    packages: set[str] = set()
    if not path.exists():
        return packages
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        deps = data.get(key, {}) or {}
        for name in deps:
            packages.add(name.lower())
    return packages


def scan_extensions(root: Path, extensions: set[str], limit: int = 500) -> bool:
    for count, path in enumerate(root.rglob("*"), start=1):
        if path.is_file() and path.suffix.lower() in extensions:
            return True
        if count >= limit:
            break
    return False


def detect_stack(project_root: Path) -> dict[str, str]:
    deps = read_package_json(project_root / "package.json")
    py_deps = read_requirements(project_root / "requirements.txt")
    go_mod = (
        (project_root / "go.mod").read_text(encoding="utf-8")
        if (project_root / "go.mod").exists()
        else ""
    )
    pom = (project_root / "pom.xml").exists()
    gemfile = (project_root / "Gemfile").exists()

    stack: dict[str, str] = {}

    backend_map = {
        "express": "Express.js",
        "fastify": "Fastify",
        "@nestjs/core": "NestJS",
        "koa": "Koa",
        "hapi": "Hapi",
    }
    for pkg, name in backend_map.items():
        if pkg in deps:
            stack["backend"] = name
            break

    if "backend" not in stack:
        if "fastapi" in py_deps:
            stack["backend"] = "FastAPI"
        elif "django" in py_deps:
            stack["backend"] = "Django"
        elif "flask" in py_deps:
            stack["backend"] = "Flask"
        elif "gin" in go_mod:
            stack["backend"] = "Gin"
        elif "echo" in go_mod:
            stack["backend"] = "Echo"
        elif pom:
            stack["backend"] = "Spring Boot"
        elif gemfile:
            stack["backend"] = "Rails"

    frontend_map = {
        "react": "React",
        "vue": "Vue",
        "@angular/core": "Angular",
        "svelte": "Svelte",
    }
    for pkg, name in frontend_map.items():
        if pkg in deps:
            stack["frontend"] = name
            break

    if "next" in deps:
        stack["frontend"] = "Next.js (React)"
    if "nuxt" in deps:
        stack["frontend"] = "Nuxt (Vue)"

    database_map = {
        "sqlite3": "SQLite",
        "better-sqlite3": "SQLite",
        "pg": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mysql": "MySQL",
        "mysql2": "MySQL",
        "mongodb": "MongoDB",
    }
    for pkg, name in database_map.items():
        if pkg in deps:
            stack["database"] = name
            break

    if "prisma" in deps:
        stack["database"] = f"{stack.get('database', 'Database')} (via Prisma)"
    if "typeorm" in deps:
        stack["database"] = f"{stack.get('database', 'Database')} (via TypeORM)"
    if "sequelize" in deps:
        stack["database"] = f"{stack.get('database', 'Database')} (via Sequelize)"

    if (project_root / "tsconfig.json").exists() or scan_extensions(
        project_root, {".ts", ".tsx"}
    ):
        stack["language"] = "TypeScript"
    elif scan_extensions(project_root, {".py"}):
        stack["language"] = "Python"
    elif scan_extensions(project_root, {".go"}):
        stack["language"] = "Go"
    elif scan_extensions(project_root, {".java"}):
        stack["language"] = "Java"
    elif scan_extensions(project_root, {".rb"}):
        stack["language"] = "Ruby"
    elif scan_extensions(project_root, {".cs"}):
        stack["language"] = "C#"
    else:
        stack["language"] = "JavaScript"

    return stack


def build_red_flags(stack: dict[str, str]) -> list[str]:
    flags: list[str] = [
        "hardcoded password",
        "hardcoded secret",
        "hardcoded api key",
        "sql injection",
        "todo: security",
        "fixme: security",
    ]

    backend = stack.get("backend", "").lower()
    frontend = stack.get("frontend", "").lower()
    language = stack.get("language", "").lower()

    if "express" in backend or "fastify" in backend or "nestjs" in backend:
        flags.extend(["bcrypt sync", "eval(", "new Function("])

    if "react" in frontend:
        flags.extend(["dangerouslySetInnerHTML", "key={index}", "missing key prop"])

    if "python" in language:
        flags.extend(["pickle.loads", "eval(", "exec("])

    if "typescript" in language:
        flags.extend(["any type", "as any", "@ts-ignore"])

    return sorted({flag.lower() for flag in flags})


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect project stack and generate red flags."
    )
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--force-refresh", action="store_true")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    output_path = Path(args.output_path).resolve()

    if output_path.exists() and not args.force_refresh:
        print(f"Using existing red flags at {output_path}")
        return 0

    defaults = load_defaults(Path(args.config))

    stack = detect_stack(project_root)
    red_flags = build_red_flags(stack)

    payload: dict[str, Any] = {
        "generatedAt": datetime.utcnow().isoformat() + "Z",
        "projectRoot": str(project_root),
        "stack": stack,
        "redFlags": red_flags,
        "defaults": {
            "defaultDaysBack": defaults.get("defaultDaysBack"),
            "defaultMinOccurrences": defaults.get("defaultMinOccurrences"),
            "defaultMinCommentLength": defaults.get("defaultMinCommentLength"),
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote red flags to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
