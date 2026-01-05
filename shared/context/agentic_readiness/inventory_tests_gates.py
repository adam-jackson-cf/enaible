#!/usr/bin/env python3
"""Inventory tests, local gates, CI gates, and enforcement signals."""

import argparse
import json
import os
from pathlib import Path

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

TEST_CATEGORIES = {
    "unit": {"tests", "test", "unit", "spec", "specs", "__tests__"},
    "integration": {"integration", "integrations", "it"},
    "e2e": {"e2e", "end-to-end", "end_to_end"},
    "smoke": {"smoke"},
    "system": {"system", "system_tests", "acceptance"},
}

GATE_SIGNALS = {
    "lint": [
        "lint",
        "eslint",
        "ruff",
        "flake8",
        "golangci-lint",
        "clippy",
        "swiftlint",
        "dotnet format",
    ],
    "format": ["format", "prettier", "black", "gofmt", "ruff format", "dotnet format"],
    "typecheck": [
        "mypy",
        "pyright",
        "tsc",
        "typecheck",
        "go vet",
        "cargo check",
        "dotnet build",
    ],
    "test": [
        "pytest",
        "go test",
        "cargo test",
        "dotnet test",
        "jest",
        "vitest",
        "npm test",
        "pnpm test",
        "bun test",
    ],
    "integration": ["integration", "e2e", "playwright", "cypress", "smoke"],
    "coverage": [
        "coverage",
        "lcov",
        "nyc",
        "pytest --cov",
        "go test -cover",
        "codecov",
    ],
    "duplication": ["jscpd", "duplication", "sonar"],
    "complexity": ["lizard", "complexity", "sonar"],
}

PRECOMMIT_FILES = (
    ".pre-commit-config.yaml",
    ".pre-commit-config.yml",
    ".lefthook.yml",
    "lefthook.yml",
    ".overcommit.yml",
    "overcommit.yml",
    ".husky/pre-commit",
    ".husky/pre-commit.sh",
    ".githooks/pre-commit",
    ".githooks/pre-commit.sh",
)

LOCAL_GATE_FILES = (
    "Makefile",
    "Taskfile.yml",
    "Taskfile.yaml",
    "justfile",
    "package.json",
)


def walk_tests(root: Path) -> dict[str, list[str]]:
    tests = {k: [] for k in TEST_CATEGORIES}
    for dirpath, dirnames, _filenames in os.walk(root):
        parts = Path(dirpath).parts
        if any(part in SKIP_DIRS for part in parts):
            dirnames[:] = []
            continue
        for d in list(dirnames):
            name = d.lower()
            for category, names in TEST_CATEGORIES.items():
                if name in names:
                    tests[category].append(str(Path(dirpath) / d))
                    break
    return tests


def scan_files(paths: list[Path]) -> dict[str, list[str]]:
    hits = {k: [] for k in GATE_SIGNALS}
    for path in paths:
        try:
            text = path.read_text(errors="ignore").lower()
        except Exception:
            continue
        for gate, terms in GATE_SIGNALS.items():
            if any(term in text for term in terms):
                hits[gate].append(str(path))
    return hits


def collect_paths(root: Path, names: tuple[str, ...]) -> list[Path]:
    collected: list[Path] = []
    for name in names:
        candidate = root / name
        if candidate.exists():
            collected.append(candidate)
    return collected


def collect_ci_files(root: Path) -> list[Path]:
    files: list[Path] = []
    workflows = root / ".github" / "workflows"
    if workflows.exists():
        files.extend(sorted(workflows.glob("*.y*ml")))
    for rel in (".gitlab-ci.yml", ".circleci/config.yml", "azure-pipelines.yml"):
        candidate = root / rel
        if candidate.exists():
            files.append(candidate)
    return files


def collect_lint_configs(root: Path) -> list[str]:
    config_names = (
        ".eslintrc",
        ".eslintrc.js",
        ".eslintrc.cjs",
        ".eslintrc.json",
        ".ruff.toml",
        "ruff.toml",
        ".flake8",
        ".pylintrc",
        ".golangci.yml",
        ".golangci.yaml",
        ".editorconfig",
        ".prettierrc",
        ".prettierrc.json",
        ".prettierrc.js",
        ".prettierrc.cjs",
    )
    configs: list[str] = []
    for name in config_names:
        candidate = root / name
        if candidate.exists():
            configs.append(str(candidate))
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(errors="ignore").lower()
        if any(term in text for term in ("tool.ruff", "tool.black", "tool.flake8")):
            configs.append(str(pyproject))
    return configs


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2))


def generate_inventory(root: Path, artifact_root: Path) -> None:
    tests = walk_tests(root)
    hard_tests_present = any(
        tests[cat] for cat in ("integration", "e2e", "smoke", "system")
    )
    write_json(
        artifact_root / "tests-inventory.json",
        {
            "frameworks": detect_frameworks(root),
            "categories": tests,
            "hard_tests_present": hard_tests_present,
        },
    )

    ci_files = collect_ci_files(root)
    local_files = collect_paths(root, LOCAL_GATE_FILES)
    precommit_files = collect_paths(root, PRECOMMIT_FILES)
    hook_script = root / "scripts" / "run-ci-quality-gates.sh"
    if hook_script.exists():
        local_files.append(hook_script)

    ci_hits = scan_files(ci_files)
    local_gate_files = list(dict.fromkeys(local_files + precommit_files))
    local_hits = scan_files(local_gate_files)
    precommit_hits = scan_files(precommit_files)

    ci_gates = {k: bool(v) for k, v in ci_hits.items()}
    local_gates = {k: bool(v) for k, v in local_hits.items()}
    precommit_gates = {k: bool(v) for k, v in precommit_hits.items()}

    parity_gaps = {
        "missing_in_ci": [k for k, v in local_gates.items() if v and not ci_gates[k]],
        "missing_local": [k for k, v in ci_gates.items() if v and not local_gates[k]],
    }
    parity_ok = not parity_gaps["missing_in_ci"] and not parity_gaps["missing_local"]

    lint_configs = collect_lint_configs(root)
    lint_config_present = bool(lint_configs)
    lint_enforced = lint_config_present and ci_gates["lint"] and precommit_gates["lint"]
    tests_enforced = (
        hard_tests_present
        and ci_gates["integration"]
        and precommit_gates["integration"]
    )

    write_json(
        artifact_root / "quality-gates.json",
        {
            "ci_files": [str(p) for p in ci_files],
            "local_files": [str(p) for p in local_files],
            "precommit_files": [str(p) for p in precommit_files],
            "lint_configs": lint_configs,
            "typecheck_configs": collect_typecheck_configs(root),
            "ci_hits": ci_hits,
            "local_hits": local_hits,
            "precommit_hits": precommit_hits,
            "ci_gates": ci_gates,
            "local_gates": local_gates,
            "precommit_gates": precommit_gates,
            "ci_files_present": bool(ci_files),
            "local_files_present": bool(local_gate_files),
            "ci_gate_signals_present": bool(ci_files) and any(ci_gates.values()),
            "local_gate_signals_present": bool(local_gate_files)
            and any(local_gates.values()),
            "parity_gaps": parity_gaps,
            "parity_ok": parity_ok,
            "lint_config_present": lint_config_present,
            "lint_enforced": lint_enforced,
            "tests_enforced": tests_enforced,
        },
    )


def detect_frameworks(root: Path) -> list[str]:
    frameworks: list[str] = []
    if (root / "pytest.ini").exists():
        frameworks.append("pytest")
    else:
        pyproject = root / "pyproject.toml"
        if pyproject.exists():
            text = pyproject.read_text(errors="ignore").lower()
            if "tool.pytest" in text or "pytest" in text:
                frameworks.append("pytest")
    if (root / "jest.config.js").exists() or (root / "jest.config.ts").exists():
        frameworks.append("jest")
    if (root / "vitest.config.ts").exists() or (root / "vitest.config.js").exists():
        frameworks.append("vitest")
    if (root / "playwright.config.ts").exists() or (
        root / "playwright.config.js"
    ).exists():
        frameworks.append("playwright")
    if (root / "cypress.config.ts").exists() or (root / "cypress.config.js").exists():
        frameworks.append("cypress")
    return frameworks


def collect_typecheck_configs(root: Path) -> list[str]:
    configs: list[str] = []
    for name in ("mypy.ini", "pyrightconfig.json", "tsconfig.json"):
        candidate = root / name
        if candidate.exists():
            configs.append(str(candidate))
    return configs


def main() -> None:
    parser = argparse.ArgumentParser(description="Inventory tests and gate signals")
    parser.add_argument("target", help="Absolute path to analyzed target")
    parser.add_argument("artifact_root", help="Artifacts root directory")
    args = parser.parse_args()

    root = Path(args.target).resolve()
    artifact_root = Path(args.artifact_root).resolve()
    artifact_root.mkdir(parents=True, exist_ok=True)
    generate_inventory(root, artifact_root)


if __name__ == "__main__":
    main()
