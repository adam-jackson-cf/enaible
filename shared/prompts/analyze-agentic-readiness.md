# Purpose

Assess agentic readiness and maintenance by scoring consistency, parallelizability, guidelines, guardrails strength, and documentation alignment using deterministic artifacts and KPI formulas.

## Variables

### Required

- @TARGET_PATH = $1 — path to analyze; defaults to repo root

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @DAYS = --days — history window for concentration and docs freshness (default 180)
- @MIN_SEVERITY = --min-severity — defaults to "low"; accepts critical|high|medium|low
- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude

### Derived (internal)

- @ARTIFACT_ROOT = <derived> — timestamped artifacts directory for readiness evidence
- @TARGET_ABS = <derived> — absolute path to the target directory
- @PROJECT_ROOT = <derived> — absolute path to the repo root

## Instructions

- ALWAYS run Enaible analyzers via the CLI (uv + enaible); do not call analyzer modules directly.
- Persist every output (analyzer JSON plus derived metrics) under @ARTIFACT_ROOT for auditability.
- Always read artifacts via absolute paths derived from `@ARTIFACT_ROOT` (avoid relative `.enaible/...` reads).
- Support the Enaible language targets listed in `README.md`: Python, TypeScript, Go, Rust, C#.
- Do not modify repository files; collect evidence only.
- Respect `@MIN_SEVERITY` for reporting; do not rerun at lower severity.
- Respect STOP confirmations unless @AUTO is provided; when auto is active, treat checkpoints as approved without altering other behavior.
- Use the KPI scoring formulas and thresholds exactly as specified in this prompt.
- After synthesis, explicitly identify gaps in deterministic tool coverage and backfill where possible.

## Workflow

1. **Establish artifacts directory**
   - Resolve the repo root, target path, and artifact root:

     ```bash
     PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
     TARGET_PATH="@TARGET_PATH"
     if [ -z "$TARGET_PATH" ] || [ "$TARGET_PATH" = "." ]; then
       TARGET_PATH="$PROJECT_ROOT"
     elif [ "${TARGET_PATH#/}" = "$TARGET_PATH" ]; then
       TARGET_PATH="$PROJECT_ROOT/$TARGET_PATH"
     fi
     TARGET_ABS="$(cd "$TARGET_PATH" && pwd)"
     ARTIFACT_ROOT="$PROJECT_ROOT/.enaible/artifacts/analyze-agentic-readiness/$(date -u +%Y%m%dT%H%M%SZ)"
     mkdir -p "$ARTIFACT_ROOT"
     export PROJECT_ROOT TARGET_ABS ARTIFACT_ROOT
     export DAYS="@DAYS"
     ```

2. **Reconnaissance (language + repo map)**
   - Detect supported languages (Python, TypeScript, Go, Rust, C#) via markers:
     - Python: `pyproject.toml`, `requirements*.txt`
     - TypeScript: `package.json`, `tsconfig.json`
     - Go: `go.mod`
     - Rust: `Cargo.toml`
     - C#: `*.sln`, `*.csproj`
   - Build a simple implementation map for top-level directories.
   - Record detected languages, map, and exclusions in artifacts.

     ```bash
     python - <<'PY'
     import json
     import os
     from pathlib import Path

     root = Path(os.environ["TARGET_ABS"])
     artifact_root = Path(os.environ["ARTIFACT_ROOT"])

     def has_glob(pattern: str) -> bool:
         return any(root.glob(pattern))

     languages = []
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

     category_map = {
         "apps": {"app", "apps", "api", "server", "services", "service", "backend"},
         "frontend": {"web", "frontend", "client", "ui"},
         "libs": {"lib", "libs", "pkg", "packages", "shared", "common", "core"},
         "tests": {"test", "tests", "__tests__", "spec", "specs", "integration", "e2e", "smoke"},
         "docs": {"docs", "doc", "documentation", "handbook", "runbooks", "guides"},
     }

     top_level = [p for p in root.iterdir() if p.is_dir()]
     map_entries = []
     for p in top_level:
         name = p.name
         category = "other"
         for key, names in category_map.items():
             if name.lower() in names:
                 category = key
                 break
         map_entries.append({"path": str(p), "category": category})

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

     (artifact_root / "recon.json").write_text(
         json.dumps(
             {"languages": languages, "exclusions": exclusions},
             indent=2,
         )
     )
     (artifact_root / "repo-map.json").write_text(
         json.dumps({"entries": map_entries}, indent=2)
     )
     PY
     ```

3. **Run analyzers (consistency + coupling + complexity)**
   - Execute each Enaible command, storing JSON output beneath @ARTIFACT_ROOT:

     ```bash
     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:jscpd \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/quality-jscpd.json" \
       @EXCLUDE

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run architecture:coupling \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/architecture-coupling.json" \
       @EXCLUDE

     ENAIBLE_REPO_ROOT="$PROJECT_ROOT" uv run --directory tools/enaible enaible analyzers run quality:lizard \
       --target "$TARGET_ABS" \
       --min-severity "@MIN_SEVERITY" \
       --out "$ARTIFACT_ROOT/quality-lizard.json" \
       @EXCLUDE
     ```

4. **Inventory tests and quality gates (local + CI parity)**
   - Detect test types, frameworks, CI gates, and local gate commands.
   - Produce parity gaps between local and CI quality checks.

     ```bash
     python - <<'PY'
     import json
     import os
     from pathlib import Path

     root = Path(os.environ["TARGET_ABS"])
     artifact_root = Path(os.environ["ARTIFACT_ROOT"])

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

     tests = {k: [] for k in test_categories}

     for dirpath, dirnames, filenames in os.walk(root):
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

     frameworks = []
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
     if (root / "playwright.config.ts").exists() or (root / "playwright.config.js").exists():
         frameworks.append("playwright")
     if (root / "cypress.config.ts").exists() or (root / "cypress.config.js").exists():
         frameworks.append("cypress")

     hard_tests_present = any(tests[cat] for cat in ("integration", "e2e", "smoke", "system"))

     ci_files = []
     if (root / ".github" / "workflows").exists():
         ci_files.extend((root / ".github" / "workflows").glob("*.y*ml"))
     if (root / ".gitlab-ci.yml").exists():
         ci_files.append(root / ".gitlab-ci.yml")
     if (root / ".circleci" / "config.yml").exists():
         ci_files.append(root / ".circleci" / "config.yml")
     if (root / "azure-pipelines.yml").exists():
         ci_files.append(root / "azure-pipelines.yml")

     local_files = []
     for name in ("Makefile", "Taskfile.yml", "Taskfile.yaml", "justfile", "package.json"):
         candidate = root / name
         if candidate.exists():
             local_files.append(candidate)
     if (root / "scripts" / "run-ci-quality-gates.sh").exists():
         local_files.append(root / "scripts" / "run-ci-quality-gates.sh")

     gate_signals = {
         "lint": ["lint", "eslint", "ruff", "flake8", "golangci-lint", "clippy", "swiftlint", "dotnet format"],
         "format": ["format", "prettier", "black", "gofmt", "ruff format", "dotnet format"],
         "typecheck": ["mypy", "pyright", "tsc", "typecheck", "go vet", "cargo check", "dotnet build"],
         "test": ["pytest", "go test", "cargo test", "dotnet test", "jest", "vitest", "npm test", "pnpm test", "bun test"],
         "integration": ["integration", "e2e", "playwright", "cypress"],
         "coverage": ["coverage", "lcov", "nyc", "pytest --cov", "go test -cover", "codecov"],
         "duplication": ["jscpd", "duplication", "sonar"],
         "complexity": ["lizard", "complexity", "sonar"],
     }

     lint_configs = []
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

     typecheck_configs = []
     for name in ("mypy.ini", "pyrightconfig.json", "tsconfig.json"):
         candidate = root / name
         if candidate.exists():
             typecheck_configs.append(str(candidate))

     def scan_gate_hits(paths):
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
     ci_present = ci_files_present and any(ci_gates.values())
     local_present = local_files_present and any(local_gates.values())
     parity_gaps = {
         "missing_in_ci": [k for k, v in local_gates.items() if v and not ci_gates[k]],
         "missing_local": [k for k, v in ci_gates.items() if v and not local_gates[k]],
     }

     (artifact_root / "tests-inventory.json").write_text(
         json.dumps(
             {
                 "frameworks": frameworks,
                 "categories": tests,
                 "hard_tests_present": hard_tests_present,
             },
             indent=2,
         )
     )
     (artifact_root / "quality-gates.json").write_text(
         json.dumps(
             {
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
                 "ci_gate_signals_present": ci_present,
                 "local_gate_signals_present": local_present,
                 "parity_gaps": parity_gaps,
             },
             indent=2,
         )
     )
     PY
     ```

5. **Guidelines, guardrails, and documentation exposure**
   - Evaluate guidance signals and whether human documentation is referenced or drifting away from execution paths.

     ```bash
     python - <<'PY'
     import json
     import os
     from pathlib import Path

     root = Path(os.environ["TARGET_ABS"])
     artifact_root = Path(os.environ["ARTIFACT_ROOT"])

     guideline_candidates = {
         "agents": root / "AGENTS.md",
         "contributing": root / "CONTRIBUTING.md",
         "readme": root / "README.md",
         "architecture": root / "ARCHITECTURE.md",
         "docs_dir": root / "docs",
     }
     guideline_present = {k: p.exists() for k, p in guideline_candidates.items()}
     guidelines_score = 1 if sum(guideline_present.values()) >= 2 else 0

     quality_gates = json.loads((artifact_root / "quality-gates.json").read_text())
     tests_inventory = json.loads((artifact_root / "tests-inventory.json").read_text())

     has_ci = quality_gates.get("ci_gate_signals_present", False)
     has_local_gate = quality_gates.get("local_gate_signals_present", False)
     hard_tests_present = tests_inventory.get("hard_tests_present", False)

     guardrails_score = 1 if (has_ci and has_local_gate and hard_tests_present) else 0

     doc_roots = [
         root / "docs",
         root / "documentation",
         root / "handbook",
         root / "runbooks",
         root / "guides",
     ]
     doc_present = [str(p) for p in doc_roots if p.exists()]

     referenced = False
     for doc in (root / "README.md", root / "AGENTS.md"):
         if doc.exists():
             text = doc.read_text(errors="ignore").lower()
             if "docs/" in text or "documentation" in text or "handbook" in text:
                 referenced = True
                 break

     (artifact_root / "guidelines.json").write_text(
         json.dumps(
             {
                 "candidates": {k: str(v) for k, v in guideline_candidates.items()},
                 "present": guideline_present,
                 "score": guidelines_score,
             },
             indent=2,
         )
     )
     (artifact_root / "guardrails.json").write_text(
         json.dumps(
             {
                 "has_ci": has_ci,
                 "has_local_gate": has_local_gate,
                 "hard_tests_present": hard_tests_present,
                 "score": guardrails_score,
             },
             indent=2,
         )
     )
     (artifact_root / "docs-exposure.json").write_text(
         json.dumps(
             {
                 "doc_roots": [str(p) for p in doc_roots],
                 "present": doc_present,
                 "referenced_in_readme_or_agents": referenced,
             },
             indent=2,
         )
     )
     PY
     ```

6. **Compute concentration + docs freshness**
   - Create evidence files under @ARTIFACT_ROOT for concentration and documentation freshness:

     ```bash
     python - <<'PY'
     import json
     import os
     import subprocess
     from collections import Counter
     from pathlib import Path
     from datetime import datetime, timezone

     root = Path(os.environ["TARGET_ABS"])
     artifact_root = Path(os.environ["ARTIFACT_ROOT"])
     days = int(os.environ.get("DAYS", "180"))

     log_cmd = [
         "git",
         "-C",
         str(root),
         "log",
         f"--since={days} days ago",
         "--name-only",
         "--pretty=format:",
     ]
     files = subprocess.check_output(log_cmd, text=True).splitlines()
     files = [f for f in files if f.strip()]
     counts = Counter(files)
     total = sum(counts.values())
     top10 = sum(c for _, c in counts.most_common(10))
     concentration = round(top10 / total, 4) if total else 0.0

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
         ts = subprocess.check_output(
             ["git", "-C", str(root), "log", "-1", "--format=%ct", "--"] + doc_args,
             text=True,
         ).strip()
         if ts:
             last_doc_ts = int(ts)
             doc_age_days = int((datetime.now(timezone.utc).timestamp() - last_doc_ts) / 86400)

     (artifact_root / "history-concentration.json").write_text(
         json.dumps(
             {
                 "window_days": days,
                 "total_file_touches": total,
                 "top10_file_touches": top10,
                 "concentration_ratio": concentration,
             },
             indent=2,
         )
     )
     (artifact_root / "docs-freshness.json").write_text(
         json.dumps(
             {
                 "candidates": [str(p) for p in doc_candidates],
                 "present": [str(p) for p in doc_paths],
                 "last_doc_commit_unix": last_doc_ts,
                 "doc_age_days": doc_age_days,
             },
             indent=2,
         )
     )
     PY
     ```

7. **Compute Agentic Readiness KPI**
   - Parse artifacts and compute the KPI using the formula below; save to `@ARTIFACT_ROOT/agentic-readiness.json`.

   **Scoring Primer**
   - Formula: `S = round(0.7*O + 0.3*A, 1)`
   - Anchor A (single definition): `10/8/5/2/0 = Excellent/Strong/Adequate/Weak/Critical`
   - Normalization: each signal → `[0,1]` by clamping between good (=1) and bad (=0)
   - Lower‑is‑better signals: `norm = clamp((bad − x)/(bad − good))`
   - Objective score: `O = Σ w_i * norm_i` (weights sum to 1)

   **Agentic Readiness**
   - Signals (w): consistency `0.30`; parallelizability `0.30`; guidelines `0.15`; guardrails `0.15`; docs_freshness `0.10`
   - Thresholds (bad ≥): dup `20%`; coupling `2.0`; concentration `0.5`; docs_age `180d`
   - Normalization: invert vs bad thresholds; lower than bad scales up toward `1`
   - Use artifact‑derived signals only; anchors are reviewer judgment applied once per KPI

     ```bash
     python - <<'PY'
     import json
     import os
     from pathlib import Path

     artifact_root = Path(os.environ["ARTIFACT_ROOT"])
     jscpd = json.loads((artifact_root / "quality-jscpd.json").read_text())
     coupling = json.loads((artifact_root / "architecture-coupling.json").read_text())
     guidelines = json.loads((artifact_root / "guidelines.json").read_text())
     guardrails = json.loads((artifact_root / "guardrails.json").read_text())
     concentration = json.loads((artifact_root / "history-concentration.json").read_text())
     docs = json.loads((artifact_root / "docs-freshness.json").read_text())

     dup_pct = (
         jscpd.get("metadata", {})
         .get("statistics", {})
         .get("total", {})
         .get("percentage", 0.0)
     )

     findings = coupling.get("findings", [])
     coupling_values = [
         f.get("evidence", {}).get("metric_value", 0)
         for f in findings
         if f.get("evidence", {}).get("metric_value") is not None
     ]
     coupling_score = round(sum(coupling_values) / len(coupling_values), 4) if coupling_values else 0.0

     concentration_ratio = concentration.get("concentration_ratio", 0.0)
     docs_age = docs.get("doc_age_days", 999)

     def clamp(value, low=0.0, high=1.0):
         return max(low, min(high, value))

     def norm_lower_is_better(x, bad, good=0.0):
         if bad == good:
             return 0.0
         return clamp((bad - x) / (bad - good))

     norm_dup = norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
     norm_concentration = norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)
     consistency = round((norm_dup + norm_concentration) / 2, 4)
     parallelizability = norm_lower_is_better(coupling_score, bad=2.0, good=0.0)
     guidelines_score = 1.0 if guidelines.get("score") == 1 else 0.0
     guardrails_score = 1.0 if guardrails.get("score") == 1 else 0.0
     docs_freshness = norm_lower_is_better(docs_age, bad=180.0, good=0.0)

     objective = round(
         (0.30 * consistency)
         + (0.30 * parallelizability)
         + (0.15 * guidelines_score)
         + (0.15 * guardrails_score)
         + (0.10 * docs_freshness),
         4,
     )

     output = {
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
     (artifact_root / "agentic-readiness.json").write_text(json.dumps(output, indent=2))
     PY
     ```

8. **Compute Maintenance Score**
   - Derive a maintenance score from duplication and complexity evidence; save to `@ARTIFACT_ROOT/maintenance-score.json`.

   **Maintenance Scoring**
   - Formula: `S = round(0.7*O + 0.3*A, 1)`
   - Anchor A (single definition): `10/8/5/2/0 = Excellent/Strong/Adequate/Weak/Critical`
   - Signals (w): duplication `0.35`; long_functions `0.20`; cc_outliers `0.20`; param_outliers `0.15`; concentration `0.10`
   - Thresholds (bad ≥): dup `20%`; long_functions `20`; cc_outliers `10`; param_outliers `15`; concentration `0.5`
   - Normalization: lower is better for all signals; use `norm = clamp((bad − x)/(bad − good))`

     ```bash
     python - <<'PY'
     import json
     import os
     from pathlib import Path

     artifact_root = Path(os.environ["ARTIFACT_ROOT"])
     jscpd = json.loads((artifact_root / "quality-jscpd.json").read_text())
     lizard = json.loads((artifact_root / "quality-lizard.json").read_text())
     concentration = json.loads((artifact_root / "history-concentration.json").read_text())

     dup_pct = (
         jscpd.get("metadata", {})
         .get("statistics", {})
         .get("total", {})
         .get("percentage", 0.0)
     )
     concentration_ratio = concentration.get("concentration_ratio", 0.0)

     findings = lizard.get("findings", [])
     long_functions = sum(1 for f in findings if f.get("title") == "Long Function")
     cc_outliers = sum(1 for f in findings if f.get("title") == "High Cyclomatic Complexity")
     param_outliers = sum(1 for f in findings if f.get("title") == "Too Many Parameters")

     def clamp(value, low=0.0, high=1.0):
         return max(low, min(high, value))

     def norm_lower_is_better(x, bad, good=0.0):
         if bad == good:
             return 0.0
         return clamp((bad - x) / (bad - good))

     norm_dup = norm_lower_is_better(dup_pct, bad=20.0, good=0.0)
     norm_long = norm_lower_is_better(long_functions, bad=20.0, good=0.0)
     norm_cc = norm_lower_is_better(cc_outliers, bad=10.0, good=0.0)
     norm_param = norm_lower_is_better(param_outliers, bad=15.0, good=0.0)
     norm_concentration = norm_lower_is_better(concentration_ratio, bad=0.5, good=0.0)

     objective = round(
         (0.35 * norm_dup)
         + (0.20 * norm_long)
         + (0.20 * norm_cc)
         + (0.15 * norm_param)
         + (0.10 * norm_concentration),
         4,
     )

     output = {
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
     (artifact_root / "maintenance-score.json").write_text(json.dumps(output, indent=2))
     PY
     ```

9. **Deliver report**
   - Summarize readiness and maintenance, include KPI scores, list the contributing signals, and reference artifact files directly.
   - Call out gaps in CI/local parity, missing hard tests, or unreferenced documentation roots.

## Output

```md
# RESULT

- Summary: Agentic readiness assessment completed for <@TARGET_PATH>.
- Artifacts: `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/`

## RECONNAISSANCE

- Supported languages detected: <Python | TypeScript | Go | Rust | C#>
- Auto-excluded: <patterns applied>

## IMPLEMENTATION MAP

| Path  | Category |
| ----- | -------- | -------- | ---- | ----- | ---- | ------ |
| <dir> | <apps    | frontend | libs | tests | docs | other> |

## SIGNALS

| Signal               | Value | Evidence                   |
| -------------------- | ----- | -------------------------- |
| Duplication %        | <n>   | quality-jscpd.json         |
| Coupling score       | <n>   | architecture-coupling.json |
| Change concentration | <n>   | history-concentration.json |
| Docs age (days)      | <n>   | docs-freshness.json        |
| Guidelines present   | <0/1> | guidelines.json            |
| Guardrails present   | <0/1> | guardrails.json            |

## QUALITY GATES & TESTS

- Hard tests present: <yes/no> (integration/e2e/smoke/system)
- Lint configs present: <yes/no> (see quality-gates.json)
- CI/Local parity gaps: <summary>

## KPI SCORING

- Formula: `S = round(0.7*O + 0.3*A, 1)`
- Objective score (O): <n>
- Anchor (A): <10/8/5/2/0>
- Agentic Readiness score (S): <n>
- Legend: 🟢 7–10 Good, 🟠 4–6 Watch, 🔴 0–3 Risk

## MAINTENANCE SCORE

- Formula: `S = round(0.7*O + 0.3*A, 1)`
- Objective score (O): <n>
- Anchor (A): <10/8/5/2/0>
- Maintenance score (S): <n>

## RISKS & GAPS

1. <risk or missing evidence>
2. <risk>

## RECOMMENDATIONS

1. <highest impact readiness improvement>
2. <follow-on improvement>

## ATTACHMENTS

- recon → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/recon.json`
- repo map → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/repo-map.json`
- quality:jscpd → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-jscpd.json`
- quality:lizard → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-lizard.json`
- architecture:coupling → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/architecture-coupling.json`
- tests inventory → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/tests-inventory.json`
- quality gates → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/quality-gates.json`
- guidelines evidence → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/guidelines.json`
- guardrails evidence → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/guardrails.json`
- docs exposure → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/docs-exposure.json`
- history concentration → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/history-concentration.json`
- docs freshness → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/docs-freshness.json`
- readiness score → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/agentic-readiness.json`
- maintenance score → `.enaible/artifacts/analyze-agentic-readiness/<timestamp>/maintenance-score.json`
```
