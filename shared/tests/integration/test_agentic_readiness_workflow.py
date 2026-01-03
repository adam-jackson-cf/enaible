from __future__ import annotations

import json
import os
import subprocess
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pytest
from analyzers.architecture.coupling_analysis import CouplingAnalyzer
from analyzers.quality.complexity_lizard import LizardComplexityAnalyzer
from analyzers.quality.jscpd_analyzer import JSCPDAnalyzer
from core.base.analyzer_base import create_analyzer_config


@pytest.mark.slow
def test_agentic_readiness_workflow_juice_shop(tmp_path: Path) -> None:
    project_root = Path(__file__).resolve().parents[3]
    target = (
        project_root
        / "shared"
        / "tests"
        / "fixture"
        / "test_codebase"
        / "juice-shop-monorepo"
    )
    assert target.is_dir(), f"Expected fixture at {target}"

    artifact_root = tmp_path / "agentic-readiness"
    artifact_root.mkdir(parents=True, exist_ok=True)

    jscpd_config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    jscpd_config.timeout_seconds = 300
    jscpd_analyzer = JSCPDAnalyzer(config=jscpd_config)
    jscpd_result = jscpd_analyzer.analyze(str(target))
    if not jscpd_result.success:
        message = (jscpd_result.error_message or "").lower()
        if "jscpd is not available" in message:
            pytest.skip("jscpd not available in environment")
        pytest.fail(jscpd_result.error_message or "jscpd analysis failed")

    (artifact_root / "quality-jscpd.json").write_text(jscpd_result.to_json())

    coupling_config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    coupling_config.max_files = 1200
    coupling_analyzer = CouplingAnalyzer(config=coupling_config)
    coupling_result = coupling_analyzer.analyze(str(target))
    assert coupling_result.success, coupling_result.error_message
    (artifact_root / "architecture-coupling.json").write_text(coupling_result.to_json())

    lizard_config = create_analyzer_config(
        target_path=str(target),
        min_severity="low",
        output_format="json",
    )
    lizard_config.max_files = 600
    lizard_analyzer = LizardComplexityAnalyzer(config=lizard_config)
    if not getattr(lizard_analyzer, "lizard_available", True):
        pytest.skip("Lizard CLI is not available in this environment")

    lizard_result = lizard_analyzer.analyze(str(target))
    assert lizard_result.success, lizard_result.error_message
    (artifact_root / "quality-lizard.json").write_text(lizard_result.to_json())

    recon = _run_recon(target)
    _write_json(artifact_root / "recon.json", recon)

    repo_map = _build_repo_map(target)
    _write_json(artifact_root / "repo-map.json", repo_map)

    tests_inventory = _inventory_tests(target)
    _write_json(artifact_root / "tests-inventory.json", tests_inventory)

    quality_gates = _inventory_quality_gates(target)
    _write_json(artifact_root / "quality-gates.json", quality_gates)

    guidelines = _inventory_guidelines(target)
    _write_json(artifact_root / "guidelines.json", guidelines)

    guardrails = _derive_guardrails(quality_gates, tests_inventory)
    _write_json(artifact_root / "guardrails.json", guardrails)

    docs_exposure = _docs_exposure(target)
    _write_json(artifact_root / "docs-exposure.json", docs_exposure)

    history = _history_concentration(target, days=180)
    _write_json(artifact_root / "history-concentration.json", history)

    docs_freshness = _docs_freshness(target)
    _write_json(artifact_root / "docs-freshness.json", docs_freshness)

    readiness = _compute_agentic_readiness(
        jscpd_result, coupling_result, guidelines, guardrails, history, docs_freshness
    )
    _write_json(artifact_root / "agentic-readiness.json", readiness)

    maintenance = _compute_maintenance_score(jscpd_result, lizard_result, history)
    _write_json(artifact_root / "maintenance-score.json", maintenance)

    assert recon["languages"], "Expected at least one detected language"
    assert repo_map["entries"], "Repo map should not be empty"
    assert readiness["objective_score"] >= 0
    assert readiness["objective_score"] <= 1
    assert maintenance["objective_score"] >= 0
    assert maintenance["objective_score"] <= 1


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2))


def _run_recon(root: Path) -> dict[str, object]:
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

    exclusions = [
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

    return {"languages": languages, "exclusions": exclusions}


def _build_repo_map(root: Path) -> dict[str, object]:
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
    for p in root.iterdir():
        if not p.is_dir():
            continue
        category = "other"
        for key, names in category_map.items():
            if p.name.lower() in names:
                category = key
                break
        entries.append({"path": str(p), "category": category})
    return {"entries": entries}


def _inventory_tests(root: Path) -> dict[str, object]:
    skip_dirs = {
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
    test_categories = {
        "unit": {"tests", "test", "unit", "spec", "specs", "__tests__"},
        "integration": {"integration", "integrations", "it"},
        "e2e": {"e2e", "end-to-end", "end_to_end"},
        "smoke": {"smoke"},
        "system": {"system", "system_tests", "acceptance"},
    }
    tests: dict[str, list[str]] = {k: [] for k in test_categories}

    for dirpath, dirnames, _ in os.walk(root):
        parts = Path(dirpath).parts
        if any(part in skip_dirs for part in parts):
            dirnames[:] = []
            continue
        for d in list(dirnames):
            name = d.lower()
            for category, names in test_categories.items():
                if name in names:
                    tests[category].append(str(Path(dirpath) / d))
                    break

    frameworks: list[str] = []
    if (root / "pytest.ini").exists():
        frameworks.append("pytest")
    elif (root / "pyproject.toml").exists():
        text = (root / "pyproject.toml").read_text(errors="ignore").lower()
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

    hard_tests_present = any(
        tests[cat] for cat in ("integration", "e2e", "smoke", "system")
    )

    return {
        "frameworks": frameworks,
        "categories": tests,
        "hard_tests_present": hard_tests_present,
    }


def _inventory_quality_gates(root: Path) -> dict[str, object]:
    ci_files: list[Path] = []
    if (root / ".github" / "workflows").exists():
        ci_files.extend((root / ".github" / "workflows").glob("*.y*ml"))
    if (root / ".gitlab-ci.yml").exists():
        ci_files.append(root / ".gitlab-ci.yml")
    if (root / ".circleci" / "config.yml").exists():
        ci_files.append(root / ".circleci" / "config.yml")
    if (root / "azure-pipelines.yml").exists():
        ci_files.append(root / "azure-pipelines.yml")

    local_files: list[Path] = []
    for name in (
        "Makefile",
        "Taskfile.yml",
        "Taskfile.yaml",
        "justfile",
        "package.json",
    ):
        candidate = root / name
        if candidate.exists():
            local_files.append(candidate)
    if (root / "scripts" / "run-ci-quality-gates.sh").exists():
        local_files.append(root / "scripts" / "run-ci-quality-gates.sh")

    gate_signals = {
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
        "format": [
            "format",
            "prettier",
            "black",
            "gofmt",
            "ruff format",
            "dotnet format",
        ],
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
        "integration": ["integration", "e2e", "playwright", "cypress"],
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

    lint_configs: list[str] = []
    for name in (
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
    ):
        candidate = root / name
        if candidate.exists():
            lint_configs.append(str(candidate))
    if (root / "pyproject.toml").exists():
        text = (root / "pyproject.toml").read_text(errors="ignore").lower()
        if "tool.ruff" in text or "tool.black" in text or "tool.flake8" in text:
            lint_configs.append(str(root / "pyproject.toml"))

    typecheck_configs: list[str] = []
    for name in ("mypy.ini", "pyrightconfig.json", "tsconfig.json"):
        candidate = root / name
        if candidate.exists():
            typecheck_configs.append(str(candidate))

    def scan_gate_hits(paths: list[Path]) -> dict[str, list[str]]:
        hits = {k: [] for k in gate_signals}
        for path in paths:
            try:
                text = path.read_text(errors="ignore").lower()
            except Exception:
                continue
            for gate, terms in gate_signals.items():
                for term in terms:
                    if term in text:
                        hits[gate].append(str(path))
                        break
        return hits

    ci_hits = scan_gate_hits(ci_files)
    local_hits = scan_gate_hits(local_files)
    ci_gates = {k: bool(v) for k, v in ci_hits.items()}
    local_gates = {k: bool(v) for k, v in local_hits.items()}

    ci_files_present = bool(ci_files)
    local_files_present = bool(local_files)
    ci_gate_signals_present = ci_files_present and any(ci_gates.values())
    local_gate_signals_present = local_files_present and any(local_gates.values())

    parity_gaps = {
        "missing_in_ci": [k for k, v in local_gates.items() if v and not ci_gates[k]],
        "missing_local": [k for k, v in ci_gates.items() if v and not local_gates[k]],
    }

    return {
        "ci_files": [str(p) for p in ci_files],
        "local_files": [str(p) for p in local_files],
        "lint_configs": lint_configs,
        "typecheck_configs": typecheck_configs,
        "ci_hits": ci_hits,
        "local_hits": local_hits,
        "ci_gates": ci_gates,
        "local_gates": local_gates,
        "ci_files_present": ci_files_present,
        "local_files_present": local_files_present,
        "ci_gate_signals_present": ci_gate_signals_present,
        "local_gate_signals_present": local_gate_signals_present,
        "parity_gaps": parity_gaps,
    }


def _inventory_guidelines(root: Path) -> dict[str, object]:
    guideline_candidates = {
        "agents": root / "AGENTS.md",
        "contributing": root / "CONTRIBUTING.md",
        "readme": root / "README.md",
        "architecture": root / "ARCHITECTURE.md",
        "docs_dir": root / "docs",
    }
    present = {k: p.exists() for k, p in guideline_candidates.items()}
    score = 1 if sum(present.values()) >= 2 else 0
    return {
        "candidates": {k: str(v) for k, v in guideline_candidates.items()},
        "present": present,
        "score": score,
    }


def _derive_guardrails(
    quality_gates: dict[str, object], tests_inventory: dict[str, object]
) -> dict[str, object]:
    has_ci = bool(quality_gates.get("ci_gate_signals_present"))
    has_local_gate = bool(quality_gates.get("local_gate_signals_present"))
    hard_tests_present = bool(tests_inventory.get("hard_tests_present"))
    score = 1 if (has_ci and has_local_gate and hard_tests_present) else 0
    return {
        "has_ci": has_ci,
        "has_local_gate": has_local_gate,
        "hard_tests_present": hard_tests_present,
        "score": score,
    }


def _docs_exposure(root: Path) -> dict[str, object]:
    doc_roots = [
        root / "docs",
        root / "documentation",
        root / "handbook",
        root / "runbooks",
        root / "guides",
    ]
    present = [str(p) for p in doc_roots if p.exists()]

    referenced = False
    for doc in (root / "README.md", root / "AGENTS.md"):
        if doc.exists():
            text = doc.read_text(errors="ignore").lower()
            if "docs/" in text or "documentation" in text or "handbook" in text:
                referenced = True
                break

    return {
        "doc_roots": [str(p) for p in doc_roots],
        "present": present,
        "referenced_in_readme_or_agents": referenced,
    }


def _history_concentration(root: Path, *, days: int) -> dict[str, object]:
    if not _git_available():
        pytest.skip("git is not available")

    log_cmd = [
        "git",
        "-C",
        str(root),
        "log",
        f"--since={days} days ago",
        "--name-only",
        "--pretty=format:",
    ]
    try:
        files = subprocess.check_output(log_cmd, text=True).splitlines()
    except subprocess.CalledProcessError as exc:
        pytest.skip(f"git log failed: {exc}")

    files = [f for f in files if f.strip()]
    counts = Counter(files)
    total = sum(counts.values())
    top10 = sum(c for _, c in counts.most_common(10))
    concentration = round(top10 / total, 4) if total else 0.0

    return {
        "window_days": days,
        "total_file_touches": total,
        "top10_file_touches": top10,
        "concentration_ratio": concentration,
    }


def _docs_freshness(root: Path) -> dict[str, object]:
    if not _git_available():
        pytest.skip("git is not available")

    doc_candidates = [
        root / "README.md",
        root / "CONTRIBUTING.md",
        root / "AGENTS.md",
        root / "docs",
    ]
    doc_paths = [p for p in doc_candidates if p.exists()]
    doc_age_days = 999
    last_doc_ts = None

    if doc_paths:
        doc_args = [str(p) for p in doc_paths]
        try:
            ts = subprocess.check_output(
                ["git", "-C", str(root), "log", "-1", "--format=%ct", "--"] + doc_args,
                text=True,
            ).strip()
        except subprocess.CalledProcessError as exc:
            pytest.skip(f"git log failed: {exc}")
        if ts:
            last_doc_ts = int(ts)
            doc_age_days = int((datetime.now(UTC).timestamp() - last_doc_ts) / 86400)

    return {
        "candidates": [str(p) for p in doc_candidates],
        "present": [str(p) for p in doc_paths],
        "last_doc_commit_unix": last_doc_ts,
        "doc_age_days": doc_age_days,
    }


def _compute_agentic_readiness(
    jscpd_result,
    coupling_result,
    guidelines: dict[str, object],
    guardrails: dict[str, object],
    concentration: dict[str, object],
    docs: dict[str, object],
) -> dict[str, object]:
    dup_pct = (
        jscpd_result.metadata.get("statistics", {})
        .get("total", {})
        .get("percentage", 0.0)
    )
    findings = coupling_result.to_dict().get("findings", [])
    coupling_values = [
        f.get("evidence", {}).get("metric_value", 0)
        for f in findings
        if f.get("evidence", {}).get("metric_value") is not None
    ]
    coupling_score = (
        round(sum(coupling_values) / len(coupling_values), 4)
        if coupling_values
        else 0.0
    )
    concentration_ratio = concentration.get("concentration_ratio", 0.0)
    docs_age = docs.get("doc_age_days", 999)

    norm_dup = _norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
    norm_concentration = _norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)
    consistency = round((norm_dup + norm_concentration) / 2, 4)
    parallelizability = _norm_lower_is_better(coupling_score, bad=2.0, good=0.0)
    guidelines_score = 1.0 if guidelines.get("score") == 1 else 0.0
    guardrails_score = 1.0 if guardrails.get("score") == 1 else 0.0
    docs_freshness = _norm_lower_is_better(docs_age, bad=180.0, good=0.0)

    objective = round(
        (0.30 * consistency)
        + (0.30 * parallelizability)
        + (0.15 * guidelines_score)
        + (0.15 * guardrails_score)
        + (0.10 * docs_freshness),
        4,
    )

    return {
        "signals": {
            "duplication_percent": dup_pct,
            "concentration_ratio": concentration_ratio,
            "coupling_score": coupling_score,
            "docs_age_days": docs_age,
            "guidelines_score": guidelines.get("score"),
            "guardrails_score": guardrails.get("score"),
        },
        "normalized": {
            "consistency": consistency,
            "parallelizability": parallelizability,
            "guidelines": guidelines_score,
            "guardrails": guardrails_score,
            "docs_freshness": docs_freshness,
        },
        "objective_score": objective,
    }


def _compute_maintenance_score(
    jscpd_result, lizard_result, concentration: dict[str, object]
) -> dict[str, object]:
    dup_pct = (
        jscpd_result.metadata.get("statistics", {})
        .get("total", {})
        .get("percentage", 0.0)
    )
    findings = lizard_result.to_dict().get("findings", [])
    long_functions = sum(1 for f in findings if f.get("title") == "Long Function")
    cc_outliers = sum(
        1 for f in findings if f.get("title") == "High Cyclomatic Complexity"
    )
    param_outliers = sum(1 for f in findings if f.get("title") == "Too Many Parameters")
    concentration_ratio = concentration.get("concentration_ratio", 0.0)

    norm_dup = _norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
    norm_long = _norm_lower_is_better(long_functions, bad=20.0, good=0.0)
    norm_cc = _norm_lower_is_better(cc_outliers, bad=10.0, good=0.0)
    norm_param = _norm_lower_is_better(param_outliers, bad=15.0, good=0.0)
    norm_concentration = _norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)

    objective = round(
        (0.35 * norm_dup)
        + (0.20 * norm_long)
        + (0.20 * norm_cc)
        + (0.15 * norm_param)
        + (0.10 * norm_concentration),
        4,
    )

    return {
        "signals": {
            "duplication_percent": dup_pct,
            "long_functions": long_functions,
            "cc_outliers": cc_outliers,
            "param_outliers": param_outliers,
            "concentration_ratio": concentration_ratio,
        },
        "normalized": {
            "duplication": norm_dup,
            "long_functions": norm_long,
            "cc_outliers": norm_cc,
            "param_outliers": norm_param,
            "concentration": norm_concentration,
        },
        "objective_score": objective,
    }


def _norm_lower_is_better(x: float, *, bad: float, good: float) -> float:
    if bad == good:
        return 0.0
    return max(0.0, min(1.0, (bad - x) / (bad - good)))


def _git_available() -> bool:
    try:
        subprocess.check_output(["git", "--version"], text=True)
        return True
    except Exception:
        return False
