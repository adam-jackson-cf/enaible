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

    quality_gates = _inventory_quality_gates(target, tests_inventory)
    _write_json(artifact_root / "quality-gates.json", quality_gates)

    docs_risk = _docs_risk(target, quality_gates)
    _write_json(artifact_root / "docs-risk.json", docs_risk)

    mcp_scan = _mcp_scan(target)
    _write_json(artifact_root / "mcp-scan.json", mcp_scan)

    history = _history_concentration(target, days=180)
    _write_json(artifact_root / "history-concentration.json", history)

    docs_freshness = _docs_freshness(target)
    _write_json(artifact_root / "docs-freshness.json", docs_freshness)

    readiness = _compute_agentic_readiness(
        jscpd_result,
        coupling_result,
        history,
        quality_gates,
        docs_risk,
        mcp_scan,
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


def _inventory_quality_gates(
    root: Path, tests_inventory: dict[str, object]
) -> dict[str, object]:
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

    precommit_files: list[Path] = []
    for name in (
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
    ):
        candidate = root / name
        if candidate.exists():
            precommit_files.append(candidate)

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
    local_gate_files = list(dict.fromkeys(local_files + precommit_files))
    local_hits = scan_gate_hits(local_gate_files)
    precommit_hits = scan_gate_hits(precommit_files)
    ci_gates = {k: bool(v) for k, v in ci_hits.items()}
    local_gates = {k: bool(v) for k, v in local_hits.items()}
    precommit_gates = {k: bool(v) for k, v in precommit_hits.items()}

    ci_files_present = bool(ci_files)
    local_files_present = bool(local_gate_files)
    ci_gate_signals_present = ci_files_present and any(ci_gates.values())
    local_gate_signals_present = local_files_present and any(local_gates.values())

    parity_gaps = {
        "missing_in_ci": [k for k, v in local_gates.items() if v and not ci_gates[k]],
        "missing_local": [k for k, v in ci_gates.items() if v and not local_gates[k]],
    }
    parity_ok = not parity_gaps["missing_in_ci"] and not parity_gaps["missing_local"]

    lint_config_present = bool(lint_configs)
    lint_enforced = lint_config_present and ci_gates["lint"] and precommit_gates["lint"]
    hard_tests_present = bool(tests_inventory.get("hard_tests_present"))
    tests_enforced = (
        hard_tests_present
        and ci_gates["integration"]
        and precommit_gates["integration"]
    )

    return {
        "ci_files": [str(p) for p in ci_files],
        "local_files": [str(p) for p in local_files],
        "precommit_files": [str(p) for p in precommit_files],
        "lint_configs": lint_configs,
        "typecheck_configs": typecheck_configs,
        "ci_hits": ci_hits,
        "local_hits": local_hits,
        "precommit_hits": precommit_hits,
        "ci_gates": ci_gates,
        "local_gates": local_gates,
        "precommit_gates": precommit_gates,
        "ci_files_present": ci_files_present,
        "local_files_present": local_files_present,
        "ci_gate_signals_present": ci_gate_signals_present,
        "local_gate_signals_present": local_gate_signals_present,
        "parity_gaps": parity_gaps,
        "parity_ok": parity_ok,
        "lint_config_present": lint_config_present,
        "lint_enforced": lint_enforced,
        "tests_enforced": tests_enforced,
    }


def _docs_risk(root: Path, quality_gates: dict[str, object]) -> dict[str, object]:
    lint_config_present = bool(quality_gates.get("lint_config_present"))

    doc_candidates = [
        root / "README.md",
        root / "CONTRIBUTING.md",
        root / "AGENTS.md",
        root / "ARCHITECTURE.md",
    ]
    doc_roots = [
        root / "docs",
        root / "documentation",
        root / "handbook",
        root / "runbooks",
        root / "guides",
    ]

    doc_files = [p for p in doc_candidates if p.exists()]
    for doc_root in doc_roots:
        if doc_root.exists():
            doc_files.extend(sorted(doc_root.rglob("*.md")))
    doc_files = list(dict.fromkeys(doc_files))

    enforce_modals = {"must", "required", "should", "shall", "never"}
    enforce_terms = {
        "lint",
        "format",
        "style",
        "typecheck",
        "mypy",
        "ruff",
        "eslint",
        "prettier",
        "flake8",
        "golangci",
        "clippy",
        "test",
        "ci",
        "pre-commit",
        "precommit",
        "gate",
    }
    review_terms = {"review", "code review", "review criteria", "review checklist"}
    agent_terms = {"llm", "ai", "agent", "assistant"}

    enforceable_hits: list[str] = []
    review_standards_present = False

    for doc in doc_files:
        try:
            text = doc.read_text(errors="ignore")
        except Exception:
            continue
        lower = text.lower()
        if any(term in lower for term in agent_terms) and any(
            term in lower for term in review_terms
        ):
            review_standards_present = True
        for line in lower.splitlines():
            if any(modal in line for modal in enforce_modals) and any(
                term in line for term in enforce_terms
            ):
                enforceable_hits.append(str(doc))
                break

    auto_included_docs = (
        [str(root / "AGENTS.md")] if (root / "AGENTS.md").exists() else []
    )
    guidance_present = bool(doc_files)
    doc_rules_unenforced = bool(enforceable_hits) and not lint_config_present

    risk_reasons: list[str] = []
    if auto_included_docs:
        risk_reasons.append("auto_included_docs_present")
    if enforceable_hits:
        risk_reasons.append("enforceable_rules_in_docs")
    if doc_rules_unenforced:
        risk_reasons.append("doc_rules_without_lint_config")
    if guidance_present and not review_standards_present:
        risk_reasons.append("missing_llm_review_standards")

    risk_score = 1 if risk_reasons else 0

    return {
        "doc_files": [str(p) for p in doc_files],
        "doc_roots": [str(p) for p in doc_roots],
        "auto_included_docs": auto_included_docs,
        "enforceable_hits": enforceable_hits,
        "review_standards_present": review_standards_present,
        "doc_rules_unenforced": doc_rules_unenforced,
        "risk_reasons": risk_reasons,
        "risk_score": risk_score,
    }


def _mcp_scan(root: Path) -> dict[str, object]:
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

    direct_candidates = [
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

    matches: list[str] = []
    for rel in direct_candidates:
        candidate = root / rel
        if candidate.exists():
            matches.append(str(candidate))

    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
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

    matches = sorted(set(matches))
    return {"matches": matches, "mcp_present": bool(matches)}


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
    concentration: dict[str, object],
    quality_gates: dict[str, object],
    docs_risk: dict[str, object],
    mcp_scan: dict[str, object],
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
    norm_dup = _norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
    norm_concentration = _norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)
    consistency = round((norm_dup + norm_concentration) / 2, 4)
    parallelizability = _norm_lower_is_better(coupling_score, bad=2.0, good=0.0)
    lint_enforced = 1.0 if quality_gates.get("lint_enforced") else 0.0
    tests_enforced = 1.0 if quality_gates.get("tests_enforced") else 0.0
    ci_local_parity = 1.0 if quality_gates.get("parity_ok") else 0.0
    doc_risk = 0.0 if docs_risk.get("risk_score") == 1 else 1.0
    mcp_risk = 0.0 if mcp_scan.get("mcp_present") else 1.0

    objective = round(
        (0.20 * consistency)
        + (0.20 * parallelizability)
        + (0.20 * lint_enforced)
        + (0.20 * tests_enforced)
        + (0.10 * ci_local_parity)
        + (0.05 * doc_risk)
        + (0.05 * mcp_risk),
        4,
    )

    return {
        "signals": {
            "duplication_percent": dup_pct,
            "concentration_ratio": concentration_ratio,
            "coupling_score": coupling_score,
            "lint_enforced": quality_gates.get("lint_enforced"),
            "tests_enforced": quality_gates.get("tests_enforced"),
            "ci_local_parity": quality_gates.get("parity_ok"),
            "doc_risk_reasons": docs_risk.get("risk_reasons", []),
            "mcp_present": mcp_scan.get("mcp_present"),
        },
        "normalized": {
            "consistency": consistency,
            "parallelizability": parallelizability,
            "lint_enforced": lint_enforced,
            "tests_enforced": tests_enforced,
            "ci_local_parity": ci_local_parity,
            "doc_risk": doc_risk,
            "mcp_risk": mcp_risk,
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
