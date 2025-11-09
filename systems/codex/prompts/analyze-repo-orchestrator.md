# analyze-repo-orchestrator v1.1

# Purpose

Run a parallel, tmux-based repository analysis that reuses existing deterministic workflows (architecture, code quality, security) and adds quality-gates, tests, and history. Produce a single 0–10 score per section with attached evidence. Use the Output section as the scoring and formatting guide.

## Variables

### Required

- @TARGET_PATH = $1 — path to analyze; defaults to repo root

### Optional (derived from $ARGUMENTS)

- @AUTO = --auto — skip STOP confirmations (auto-approve checkpoints)
- @VERBOSE = --verbose — add extended reasoning in final report
- @TIMEOUT_SEC = --timeout — overall wait timeout per session (default 3600)
- @EXCLUDE = --exclude [repeatable] — additional glob patterns to exclude (passed to child prompts where applicable)

### Derived (internal)

- @ORCH_ROOT — timestamped orchestrator artifact directory

## Instructions

- ALWAYS call Enaible analyzers via the CLI (uv + enaible); do not call other prompts from this prompt.
- Launch each analysis in its own tmux session to run in parallel and avoid blocking on long tasks.
- Persist all outputs under @ORCH_ROOT and the analyzer-specific directories; capture paths to a manifest for provenance.
- Use the Output section to compute scores deterministically from artifacts (anchors, normalization, and final format).
- Respect STOP confirmations unless @AUTO is provided.

## Workflow

1. Init artifacts

- `ORCH_TS="$(date -u +%Y%m%dT%H%M%SZ)"`; `@ORCH_ROOT=".enaible/artifacts/orchestrator/${ORCH_TS}"`
- Create: `@ORCH_ROOT/{gates/backend,gates/frontend,tests,history}`

2. Launch core analyses (parallel via tmux; call analyzers directly)

- Architecture:
  ```bash
  tmux new-session -d -s ra-arch "\
    ARCH_ROOT=.enaible/artifacts/analyze-architecture/${ORCH_TS}; mkdir -p \"$ARCH_ROOT\"; \
    uv run --project tools/enaible enaible analyzers run architecture:patterns \
      --target '@TARGET_PATH' --out \"$ARCH_ROOT/architecture-patterns.json\"; \
    uv run --project tools/enaible enaible analyzers run architecture:dependency \
      --target '@TARGET_PATH' --out \"$ARCH_ROOT/architecture-dependency.json\"; \
    uv run --project tools/enaible enaible analyzers run architecture:coupling \
      --target '@TARGET_PATH' --out \"$ARCH_ROOT/architecture-coupling.json\"; \
    uv run --project tools/enaible enaible analyzers run architecture:scalability \
      --target '@TARGET_PATH' --out \"$ARCH_ROOT/architecture-scalability.json\"; \
    printf '%s' $? > '@ORCH_ROOT/ra-arch.exit'"
  ```
- Code Quality:
  ```bash
  tmux new-session -d -s ra-quality "\
    QUAL_ROOT=.enaible/artifacts/analyze-code-quality/${ORCH_TS}; mkdir -p \"$QUAL_ROOT\"; \
    uv run --project tools/enaible enaible analyzers run quality:lizard \
      --target '@TARGET_PATH' --out \"$QUAL_ROOT/quality-lizard.json\"; \
    uv run --project tools/enaible enaible analyzers run quality:jscpd \
      --target '@TARGET_PATH' --out \"$QUAL_ROOT/quality-jscpd.json\"; \
    printf '%s' $? > '@ORCH_ROOT/ra-quality.exit'"
  ```
- Security:
  ```bash
  tmux new-session -d -s ra-sec "\
    SEC_ROOT=.enaible/artifacts/analyze-security/${ORCH_TS}; mkdir -p \"$SEC_ROOT\"; \
    uv run --project tools/enaible enaible analyzers run security:semgrep \
      --target '@TARGET_PATH' --out \"$SEC_ROOT/semgrep.json\"; \
    uv run --project tools/enaible enaible analyzers run security:detect_secrets \
      --target '@TARGET_PATH' --out \"$SEC_ROOT/detect-secrets.json\"; \
    printf '%s' $? > '@ORCH_ROOT/ra-sec.exit'"
  ```

3. Quality Gates (auto-detect)

- Backend (Python):

```bash
if rg -l "^\s*import |^\s*from .* import" --glob "**/*.py" -n >/dev/null 2>&1; then
  tmux new-session -d -s ra-gates-backend "\
    (uv run --project tools/enaible ruff check . || true) 2>&1 | tee '@ORCH_ROOT/gates/backend/ruff.txt'; \
    (uv run --project tools/enaible mypy . || true) 2>&1 | tee '@ORCH_ROOT/gates/backend/mypy.txt'; \
    (uv run --project tools/enaible black --check . || true) 2>&1 | tee '@ORCH_ROOT/gates/backend/black.txt' \
  ; printf '%s' $? > '@ORCH_ROOT/ra-gates-backend.exit'"
fi
```

- Frontend (JS/TS):

```bash
if [ -f package.json ] || rg -l --glob "**/*.{ts,tsx,js,jsx}" -n >/dev/null 2>&1; then
  tmux new-session -d -s ra-gates-frontend "\
    (bunx tsc --noEmit || true) 2>&1 | tee '@ORCH_ROOT/gates/frontend/tsc.txt'; \
    (bunx eslint . -f json || true) > '@ORCH_ROOT/gates/frontend/eslint.json'; \
    (bunx ultracite check src || true) 2>&1 | tee '@ORCH_ROOT/gates/frontend/ultracite.txt' \
  ; printf '%s' $? > '@ORCH_ROOT/ra-gates-frontend.exit'"
fi
```

4. Tests (best-effort)

```bash
if rg -q "^\s*pytest" pyproject.toml tools/enaible/pyproject.toml 2>/dev/null || [ -d tests ] || [ -d tooltests ]; then
  tmux new-session -d -s ra-tests "(uv run --project tools/enaible pytest -q || true) 2>&1 | tee '@ORCH_ROOT/tests/pytest.txt'; printf '%s' $? > '@ORCH_ROOT/ra-tests.exit'"
elif [ -f package.json ]; then
  tmux new-session -d -s ra-tests "(bun run test -- --coverage || bun run test || true) 2>&1 | tee '@ORCH_ROOT/tests/frontend-tests.txt'; printf '%s' $? > '@ORCH_ROOT/ra-tests.exit'"
fi
```

5. Repo History (for smells/churn)

```bash
tmux new-session -d -s ra-history "\
  (git log --since='120 days ago' --pretty=format:'%h %ad %an %s' --date=iso --numstat || true) > '@ORCH_ROOT/history/git-numstat.txt'; \
  (git log --name-only --pretty=format: | sort | uniq -c | sort -nr | head -200 || true) > '@ORCH_ROOT/history/top-touched-files.txt' \
; printf '%s' $? > '@ORCH_ROOT/ra-history.exit'"
```

6. Await completion / timeout

- For each started name: `ra-arch ra-quality ra-sec ra-gates-backend ra-gates-frontend ra-tests ra-history`
- Poll until `@TIMEOUT_SEC`: `tmux has-session -t <name> 2>/dev/null || echo done`
- On timeout: mark failed; retain partial artifacts.

7. Build artifact manifest (no external scripts)

- Use the orchestrator timestamp to resolve directories:
  - `ARCH_DIR = .enaible/artifacts/analyze-architecture/${ORCH_TS}` (omit if missing)
  - `QUAL_DIR = .enaible/artifacts/analyze-code-quality/${ORCH_TS}` (omit if missing)
  - `SEC_DIR  = .enaible/artifacts/analyze-security/${ORCH_TS}` (omit if missing)
- Create `@ORCH_ROOT/artifacts-manifest.json` with keys:
  - `analyze_architecture`: all files matching `${ARCH_DIR}/architecture-*.json`
  - `analyze_code_quality`: all files matching `${QUAL_DIR}/quality-*.json`
  - `analyze_security`: all JSON files in `${SEC_DIR}`
  - `quality_gates.backend`: `@ORCH_ROOT/gates/backend/{ruff.txt,mypy.txt,black.txt}` that exist
  - `quality_gates.frontend`: `@ORCH_ROOT/gates/frontend/{tsc.txt,eslint.json,ultracite.txt}` that exist
  - `tests`: any files in `@ORCH_ROOT/tests/`
  - `history`: any files in `@ORCH_ROOT/history/`
- Serialize as JSON with absolute or repo-relative paths; omit non-existent files.

8. Score and emit report

- Compute Objective (O) from artifacts; choose Anchor (L) from anchors based on evidence; `S = round(0.7*O + 0.3*L, 1)`.
- Produce `@ORCH_ROOT/scorecard.json` and `@ORCH_ROOT/scorecard.md` exactly per Output examples.

## Output

Artifacts and scoring are defined by the following example outputs. Follow them exactly.

1. `@ORCH_ROOT/artifacts-manifest.json`

```json
{
  "orchestrator_root": "/abs/or/relative/path/.enaible/artifacts/orchestrator/20250101T000000Z",
  "analyze_architecture": [
    ".enaible/artifacts/analyze-architecture/20250101T000000Z/architecture-dependency.json",
    ".enaible/artifacts/analyze-architecture/20250101T000000Z/architecture-coupling.json",
    ".enaible/artifacts/analyze-architecture/20250101T000000Z/architecture-patterns.json"
  ],
  "analyze_code_quality": [
    ".enaible/artifacts/analyze-code-quality/20250101T000000Z/quality-lizard.json",
    ".enaible/artifacts/analyze-code-quality/20250101T000000Z/quality-jscpd.json"
  ],
  "analyze_security": [
    ".enaible/artifacts/analyze-security/20250101T000000Z/semgrep.json",
    ".enaible/artifacts/analyze-security/20250101T000000Z/detect-secrets.json"
  ],
  "quality_gates": {
    "backend": [
      "@ORCH_ROOT/gates/backend/ruff.txt",
      "@ORCH_ROOT/gates/backend/mypy.txt",
      "@ORCH_ROOT/gates/backend/black.txt"
    ],
    "frontend": [
      "@ORCH_ROOT/gates/frontend/tsc.txt",
      "@ORCH_ROOT/gates/frontend/eslint.json",
      "@ORCH_ROOT/gates/frontend/ultracite.txt"
    ]
  },
  "tests": ["@ORCH_ROOT/tests/pytest.txt"],
  "history": [
    "@ORCH_ROOT/history/git-numstat.txt",
    "@ORCH_ROOT/history/top-touched-files.txt"
  ]
}
```

2. `@ORCH_ROOT/scorecard.json`

```json
{
  "run": {
    "timestamp": "2025-01-01T00:00:00Z",
    "git_sha": "<sha>",
    "root": "<path>",
    "config_path": ".enaible/orchestrator.json"
  },
  "sections": [
    {
      "id": "architecture",
      "name": "Architecture & Boundaries",
      "score": 8.4,
      "objective_score": 8.0,
      "anchor": 9,
      "confidence": 0.7,
      "rationale": "Clear domain boundaries, minimal cycles, explicit patterns; data constraints mostly present.",
      "top_drivers": [
        {
          "signal": "cycles_per_1k",
          "value": 1,
          "norm": 1.0,
          "artifact": ".../architecture-dependency.json"
        },
        {
          "signal": "boundary_violations",
          "value": 3,
          "norm": 0.9,
          "artifact": ".../architecture-coupling.json"
        },
        {
          "signal": "data_constraints_missing_pct",
          "value": 4,
          "norm": 0.8,
          "artifact": ".../semgrep.json"
        }
      ],
      "evidence": [
        ".../architecture-dependency.json",
        ".../architecture-coupling.json",
        ".../architecture-patterns.json",
        ".../semgrep.json"
      ],
      "na": false
    },
    {
      "id": "backend_quality",
      "name": "Backend Code Quality",
      "score": 7.5,
      "objective_score": 7.0,
      "anchor": 8,
      "confidence": 0.6,
      "rationale": "Complexity within bounds; some duplication; typing mostly clean.",
      "top_drivers": [
        {
          "signal": "cc_max",
          "value": 12,
          "norm": 0.8,
          "artifact": ".../quality-lizard.json"
        },
        {
          "signal": "dup_pct",
          "value": 6.2,
          "norm": 0.7,
          "artifact": ".../quality-jscpd.json"
        },
        {
          "signal": "type_errors_per_kloc",
          "value": 0.5,
          "norm": 0.95,
          "artifact": "@ORCH_ROOT/gates/backend/mypy.txt"
        }
      ],
      "evidence": [
        ".../quality-lizard.json",
        ".../quality-jscpd.json",
        "@ORCH_ROOT/gates/backend/mypy.txt",
        "@ORCH_ROOT/gates/backend/ruff.txt"
      ],
      "na": false
    },
    {
      "id": "frontend_quality",
      "name": "Frontend Code Quality",
      "score": 6.8,
      "objective_score": 6.5,
      "anchor": 7,
      "confidence": 0.6,
      "rationale": "TS ok; some ESLint issues; components reused; theming present; a few inline styles.",
      "top_drivers": [
        {
          "signal": "ts_errors",
          "value": 3,
          "norm": 0.9,
          "artifact": "@ORCH_ROOT/gates/frontend/tsc.txt"
        },
        {
          "signal": "eslint_problems_per_kloc",
          "value": 12,
          "norm": 0.7,
          "artifact": "@ORCH_ROOT/gates/frontend/eslint.json"
        },
        {
          "signal": "component_reuse_ratio",
          "value": 0.72,
          "norm": 0.8,
          "artifact": ".../quality-jscpd.json"
        }
      ],
      "evidence": [
        "@ORCH_ROOT/gates/frontend/tsc.txt",
        "@ORCH_ROOT/gates/frontend/eslint.json",
        "@ORCH_ROOT/gates/frontend/ultracite.txt"
      ],
      "na": false
    },
    {
      "id": "patterns_consistency",
      "name": "Patterns & Consistency",
      "score": 7.9,
      "objective_score": 7.5,
      "anchor": 8,
      "confidence": 0.6,
      "rationale": "Backend layering/naming consistent; FE uses theme tokens and shadcn; minimal ad‑hoc styles.",
      "top_drivers": [
        {
          "signal": "copy_paste_vs_utils_index",
          "value": 0.18,
          "norm": 0.85,
          "artifact": ".../quality-jscpd.json"
        },
        {
          "signal": "theme_tokens_presence",
          "value": 1,
          "norm": 1.0,
          "artifact": "@ORCH_ROOT/gates/frontend/ultracite.txt"
        },
        {
          "signal": "error_handling_uniformity",
          "value": 0.8,
          "norm": 0.8,
          "artifact": ".../quality-lizard.json"
        }
      ],
      "evidence": [
        ".../architecture-patterns.json",
        "@ORCH_ROOT/gates/frontend/ultracite.txt"
      ],
      "na": false
    },
    {
      "id": "anti_patterns",
      "name": "Anti-Patterns & Smells",
      "score": 6.2,
      "objective_score": 6.0,
      "anchor": 6,
      "confidence": 0.5,
      "rationale": "A few god files; moderate TODO density; no widespread dead code.",
      "top_drivers": [
        {
          "signal": "god_files_count",
          "value": 2,
          "norm": 0.6,
          "artifact": ".../quality-lizard.json"
        },
        {
          "signal": "todo_density_per_kloc",
          "value": 3.2,
          "norm": 0.7,
          "artifact": "@ORCH_ROOT/history/git-numstat.txt"
        },
        {
          "signal": "high_fanout_modules",
          "value": 4,
          "norm": 0.75,
          "artifact": ".../architecture-dependency.json"
        }
      ],
      "evidence": [
        ".../quality-lizard.json",
        "@ORCH_ROOT/history/git-numstat.txt"
      ],
      "na": false
    },
    {
      "id": "testing_cicd",
      "name": "Testing & CI/CD",
      "score": 6.9,
      "objective_score": 6.5,
      "anchor": 7,
      "confidence": 0.5,
      "rationale": "Tests present; partial coverage reports; CI runs tests; flake unknown.",
      "top_drivers": [
        {
          "signal": "coverage_pct",
          "value": 62,
          "norm": 0.62,
          "artifact": "@ORCH_ROOT/tests/pytest.txt"
        },
        {
          "signal": "test_jobs_in_ci",
          "value": 1,
          "norm": 1.0,
          "artifact": ".github/workflows/*.yml"
        }
      ],
      "evidence": ["@ORCH_ROOT/tests/pytest.txt", ".github/workflows"],
      "na": false
    },
    {
      "id": "security",
      "name": "Security & Compliance",
      "score": 8.1,
      "objective_score": 7.8,
      "anchor": 8,
      "confidence": 0.6,
      "rationale": "No secrets; few medium issues; mitigations identified.",
      "top_drivers": [
        {
          "signal": "semgrep_high_or_critical",
          "value": 0,
          "norm": 1.0,
          "artifact": ".../semgrep.json"
        },
        {
          "signal": "secrets_found",
          "value": 0,
          "norm": 1.0,
          "artifact": ".../detect-secrets.json"
        }
      ],
      "evidence": [".../semgrep.json", ".../detect-secrets.json"],
      "na": false
    },
    {
      "id": "quality_gates",
      "name": "Quality Gates",
      "score": 7.3,
      "objective_score": 7.0,
      "anchor": 7,
      "confidence": 0.6,
      "rationale": "Linters and typecheckers configured and mostly clean; CI enforces.",
      "top_drivers": [
        {
          "signal": "backend_lint_errors",
          "value": 4,
          "norm": 0.9,
          "artifact": "@ORCH_ROOT/gates/backend/ruff.txt"
        },
        {
          "signal": "frontend_eslint_errors",
          "value": 10,
          "norm": 0.8,
          "artifact": "@ORCH_ROOT/gates/frontend/eslint.json"
        },
        {
          "signal": "ci_enforcement_present",
          "value": 1,
          "norm": 1.0,
          "artifact": ".github/workflows/*.yml"
        }
      ],
      "evidence": [
        "@ORCH_ROOT/gates/backend/ruff.txt",
        "@ORCH_ROOT/gates/frontend/eslint.json",
        ".github/workflows"
      ],
      "na": false
    },
    {
      "id": "developer_experience",
      "name": "Developer Experience & Docs",
      "score": 7.0,
      "objective_score": 6.8,
      "anchor": 7,
      "confidence": 0.6,
      "rationale": "One-command run; env templates; some ADRs; onboarding is straightforward.",
      "top_drivers": [
        {
          "signal": "one_command_run_present",
          "value": 1,
          "norm": 1.0,
          "artifact": "package.json or Makefile"
        },
        {
          "signal": "env_template_present",
          "value": 1,
          "norm": 1.0,
          "artifact": ".env.example"
        }
      ],
      "evidence": ["README.md", ".env.example", "docs/"],
      "na": false
    }
  ],
  "overall": {
    "score": 7.4,
    "included_sections": [
      "architecture",
      "backend_quality",
      "frontend_quality",
      "patterns_consistency",
      "anti_patterns",
      "testing_cicd",
      "security",
      "quality_gates",
      "developer_experience"
    ]
  },
  "unknowns": ["coverage not reported"]
}
```

Scoring guidance (implicit in the example above):

- Anchors per section: 10 Excellent, 8 Strong, 5 Adequate, 2 Weak, 0 Critical.
- Objective (O) from artifacts (e.g., cycles, boundary violations, complexity, duplication, type/lint errors, secrets). Normalize each signal to 0–1; average per section.
- Final S = round(0.7*O + 0.3*Anchor, 1). If a section is not applicable, set `na: true` and exclude from the overall average.

3. `@ORCH_ROOT/scorecard.md` (render succinctly)

```md
# RESULT

- Summary: Repository analysis for <@TARGET_PATH> completed.
- Artifacts: `@ORCH_ROOT`
- Overall Score: 7.4 / 10

## SECTION SCORES

- Architecture & Boundaries — 8.4
- Backend Code Quality — 7.5
- Frontend Code Quality — 6.8 (present)
- Patterns & Consistency — 7.9
- Anti-Patterns & Smells — 6.2
- Testing & CI/CD — 6.9
- Security & Compliance — 8.1
- Quality Gates — 7.3
- Developer Experience & Docs — 7.0

## TOP FINDINGS (evidence-first)

- Minimal dependency cycles; few boundary violations; explicit patterns.
- Backend complexity within bounds; duplication slightly above target.
- Frontend has theming and component reuse; ESLint issues to address.
- No secrets found; semgrep clean for high/critical.

## ATTACHMENTS

- Manifest → `@ORCH_ROOT/artifacts-manifest.json`
- Architecture → `.enaible/artifacts/analyze-architecture/<ts>/...`
- Code Quality → `.enaible/artifacts/analyze-code-quality/<ts>/...`
- Security → `.enaible/artifacts/analyze-security/<ts>/...`
- Gates/Tests/History → `@ORCH_ROOT/...`
```

## Examples

```bash
# Run orchestrator on entire repository
/analyze-repo-orchestrator . --auto --timeout 5400

# Focus on a subpackage
/analyze-repo-orchestrator services/api --auto
```

<!-- generated: enaible -->
