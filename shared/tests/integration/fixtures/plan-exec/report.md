# CLI migration improvements — Codebase Scoution (20 days)

Current analyzers still rely on manual script resolution, underscoring the need for the planned enaible CLI to centralize prompt execution (todos/cli-migration/cli-improvements.md:52).

## Repository Overview

- Languages: Python-first automation with multi-language analyzer coverage highlighted in the repo badges (README.md:19).
- Package Managers: Analyzer tooling is delivered through pip/uv requirements alongside shared CLI dependencies (requirements-dev.txt:1; shared/setup/requirements.txt:4).
- Key Manifests/Configs: Analyzer docs enumerate `shared/analyzers/`, `core/`, `ci/`, and other configuration roots that anchor the workflow (docs/analysis-scripts.md:100-107).
- Top-Level Directories: The same structure callout shows `shared/`, `systems/`, `docs/`, and `tests/` as primary directories (docs/analysis-scripts.md:100-107).
- Primary Commands: Quick start instructions rely on system install scripts for each CLI (`./systems/*/install.sh`) (README.md:84-94).

## Architecture

- Apps/Services/CLIs: `core.cli.run_analyzer` exposes a registry-driven CLI that orchestrates analyzer executions via CLI arguments (shared/core/cli/run_analyzer.py:7-95).
- Entry Points: `registry_bootstrap` imports every analyzer module at startup to populate the shared registry (shared/core/base/registry_bootstrap.py:9-43).
- Composition Roots / DI: Shared security prompt still performs script path discovery before shelling out to the registry, showing the brittle adapter layer the migration must remove (shared/prompts/analyze-security.md:22-46).
- Layering/Boundaries/Patterns: The exec plan names `tools/enaible` plus adapters/templates as the future composition root above existing analyzer infrastructure (execplans/20251014-cli-migration-improvements.md:32-42).

## Quality

- Organization/Conventions: `BaseAnalyzer` centralizes configuration validation, file filtering, and logging while pre-commit enforces Python/Markdown formatting (shared/core/base/analyzer_base.py:47-198; .pre-commit-config.yaml:4-49).
- Complexity hotspots (by scoution): The batch analyzer pipeline pulls scanning, batching, and metadata assembly into one method, making it a candidate for refinement (shared/core/base/analyzer_base.py:389-487).
- Duplication hints: Registry unit tests prove idempotent registration, yet system prompts duplicate identical path-probing workflows (shared/tests/unit/test_analyzer_registry.py:22-62; systems/codex/prompts/analyze-security.md:15-112).

## Performance

- Hotspots: `run_all_analyzers` drives sequential analyzer execution and flags external-tool skips, illustrating current runtime characteristics (shared/integration/cli/run_all_analyzers.py:32-118).
- Analyzer Coverage: Performance analyzer inventory spans profiling, ESLint-based checks, Ruff optimizations, and SQL heuristics (docs/analysis-scripts.md:126-161).
- Memoization/Cache: Base analyzer batch processing tracks files and errors but lacks caching, relying on per-run scans (shared/core/base/analyzer_base.py:389-487).

## Security

- Secrets patterns: Detect-secrets analyzer wraps the upstream CLI, validates config, and normalizes findings (shared/analyzers/security/detect_secrets_analyzer.py:36-323).
- AuthN/AuthZ flows & risky endpoints: Shared security prompt enforces OWASP stops and manual gap assessments (shared/prompts/analyze-security.md:22-108).
- System wrappers: Codex prompt duplicates the same script-path resolution and confirmations, highlighting cross-system drift the migration targets (systems/codex/prompts/analyze-security.md:15-112).

## Data & State

- Analyzer configuration: `AnalyzerConfig` manages target paths, file filters, severity thresholds, and validation for every run (shared/core/base/analyzer_base.py:47-155).
- Result shaping: `ResultFormatter` stores findings with severity filters and JSON export for downstream consumption (shared/core/utils/output_formatter.py:73-185).
- Future artifact layout: Migration plan moves prompts and templates under `.enaible` conventions with adapters feeding templates (todos/cli-migration/cli-improvements.md:42-61).

## Visual Design & UX

- UI libs/tokens: Guidelines require React Router with shadcn/ui over Radix primitives and Tailwind tokens (systems/claude-code/rules/global.claude.rules.md:12-15).
- Accessibility posture: Production rules insist on Radix accessibility audits and PostHog gating (systems/claude-code/rules/global.claude.rules.md:22-26).
- Scoution cues: Audit command instructs scoutors to search for Radix/shadcn/Tailwind usage across the repo (systems/codex/prompts/get-feature-primer.md:38-53).

## Tests

- Frameworks: Unit tests register dummy analyzers to exercise registry semantics via pytest (shared/tests/unit/test_analyzer_registry.py:22-83).
- Layout: Integration smoke test lives under `shared/tests/integration` and covers the CLI runner (shared/tests/integration/test_integration_all_analyzers.py:8-21).
- Commands: CI runs pytest with coverage thresholds via the incremental gate workflow (.github/workflows/ci-quality-gates-incremental.yml:32-43).

## CI/CD & Tooling

- Workflows: Incremental quality gate installs Node and Python, enforces coverage, lint, and mypy ( .github/workflows/ci-quality-gates-incremental.yml:17-53).
- Toolchain deps: Shared setup requirements install lizard, ruff, sqlglot, detect-secrets, and supporting CLIs (shared/setup/requirements.txt:4-16).
- Pre-commit hooks: Field report notes prettier-induced hook failures requiring restaging, underscoring strict hooks (orchestrate-issues.md:20-33).

## Observability

- Logging: Dev monitoring doc standardizes unified logging to `./dev.log` with dashboards and service health views (docs/monitoring.md:12-44).
- Analytics gating: Prototype stage stubs PostHog until consent is recorded (systems/claude-code/rules/global.claude.rules.md:15-16).
- Production analytics: Rules require enabling PostHog with feature flag tracking once consent exists (systems/claude-code/rules/global.claude.rules.md:25-26).

## Git Insights (last 20 days)

- Status summary: Orchestration log captures a recent run on `feature/cli-migration-cli-improvements` with missing CLI tooling called out (orchestrate-issues.md:3-53).
- Churn hotspots: Exec plan updated on 2025-10-14 lists outstanding tasks for `tools/enaible` and prompt rewrites (execplans/20251014-cli-migration-improvements.md:15-48).
- Turning points: Migration spec outlines next actions to migrate templates and enforce `enaible prompts diff` in CI (todos/cli-migration/cli-improvements.md:112-116).

## Task Impact Analysis

- Impacted files/modules: `systems/codex/prompts/analyze-security.md:15` — Replace path-probing workflow with `enaible` invocation (systems/codex/prompts/analyze-security.md:15-112); `systems/claude-code/commands/analyze-security.md:21` — Mirror update required for Claude Code command variant (systems/claude-code/commands/analyze-security.md:17-120); `shared/core/cli/run_analyzer.py:7` — Existing registry runner should be wrapped rather than called directly from prompts (shared/core/cli/run_analyzer.py:7-95).
- Risks/Assumptions: Spec forbids keeping legacy path probing alongside `enaible`, so rollout must be atomic (todos/cli-migration/cli-improvements.md:51-55); Templates must be relocated under `docs/system/<system>/templates/` before render pipeline can work (todos/cli-migration/cli-improvements.md:79-82); Prior orchestration run showed missing `cdx-exec`, so the migration needs a single Codex entrypoint (orchestrate-issues.md:44-53).
- Search cues used: `rg -n --hidden "@tanstack/(react-router|router)|react-router-dom|routeTree\.gen\.ts" .` confirmed routing references sit in rules documentation; `rg -n --hidden "drizzle|drizzle-orm|better-sqlite3|drizzle\.config\.(ts|js)" .` showed ORM mentions concentrated in command docs; `rg -n --hidden "@radix-ui/react-|shadcn/ui|tailwind\.config\.(ts|js|cjs)" .` highlighted design guidance in rules files (systems/claude-code/rules/global.claude.rules.md:12).

## Evidence Ledger

- README.md:19 — Badge set lists supported languages • Command: "nl -ba README.md | sed -n '1,120p'"
- README.md:84 — Quick start install commands for CLIs • Command: "nl -ba README.md | sed -n '80,120p'"
- requirements-dev.txt:1 — Dev dependencies for analyzer tooling • Command: "nl -ba requirements-dev.txt"
- shared/setup/requirements.txt:4 — Shared CLI dependency list • Command: "nl -ba shared/setup/requirements.txt"
- .github/workflows/ci-quality-gates-incremental.yml:17 — Workflow installs Node and Python • Command: "nl -ba .github/workflows/ci-quality-gates-incremental.yml"
- .github/workflows/ci-quality-gates-incremental.yml:32 — CI runs pytest with coverage • Command: "nl -ba .github/workflows/ci-quality-gates-incremental.yml"
- shared/core/cli/run_analyzer.py:7 — Registry-based analyzer CLI entrypoint • Command: "nl -ba shared/core/cli/run_analyzer.py | sed -n '1,200p'"
- shared/core/base/registry_bootstrap.py:9 — Import side-effect registers analyzers • Command: "nl -ba shared/core/base/registry_bootstrap.py | sed -n '1,200p'"
- shared/core/base/analyzer_base.py:47 — AnalyzerConfig default settings • Command: "nl -ba shared/core/base/analyzer_base.py | sed -n '1,200p'"
- shared/core/base/analyzer_base.py:389 — Batch processing loop • Command: "nl -ba shared/core/base/analyzer_base.py | sed -n '360,520p'"
- shared/core/utils/output_formatter.py:73 — AnalysisResult structure • Command: "nl -ba shared/core/utils/output_formatter.py | sed -n '1,200p'"
- shared/analyzers/security/detect_secrets_analyzer.py:36 — Detect-secrets config and registration • Command: "nl -ba shared/analyzers/security/detect_secrets_analyzer.py | sed -n '1,200p'"
- shared/analyzers/security/detect_secrets_analyzer.py:290 — analyze_target standardizes findings • Command: "nl -ba shared/analyzers/security/detect_secrets_analyzer.py | sed -n '200,360p'"
- shared/prompts/analyze-security.md:22 — Shared prompt path-probing workflow • Command: "nl -ba shared/prompts/analyze-security.md | sed -n '1,200p'"
- systems/codex/prompts/analyze-security.md:15 — Codex wrapper duplicating instructions • Command: "nl -ba systems/codex/prompts/analyze-security.md | sed -n '1,200p'"
- systems/claude-code/commands/analyze-security.md:21 — Claude Code command path probing • Command: "nl -ba systems/claude-code/commands/analyze-security.md | sed -n '1,200p'"
- docs/analysis-scripts.md:126 — Performance analyzer inventory • Command: "nl -ba docs/analysis-scripts.md | sed -n '100,220p'"
- docs/monitoring.md:12 — Unified logging to ./dev.log • Command: "nl -ba docs/monitoring.md | sed -n '1,120p'"
- systems/claude-code/rules/global.claude.rules.md:12 — Frontend stack guidance • Command: "nl -ba systems/claude-code/rules/global.claude.rules.md | sed -n '1,120p'"
- systems/claude-code/rules/global.claude.rules.md:25 — Production PostHog guidance • Command: "nl -ba systems/claude-code/rules/global.claude.rules.md | sed -n '1,120p'"
- systems/codex/prompts/get-feature-primer.md:38 — Search cues for UI libraries • Command: "nl -ba systems/codex/prompts/get-feature-primer.md | sed -n '1,200p'"
- shared/tests/unit/test_analyzer_registry.py:22 — Registry unit test • Command: "nl -ba shared/tests/unit/test_analyzer_registry.py | sed -n '1,200p'"
- shared/tests/integration/test_integration_all_analyzers.py:8 — Integration smoke test • Command: "nl -ba shared/tests/integration/test_integration_all_analyzers.py | sed -n '1,200p'"
- shared/integration/cli/run_all_analyzers.py:32 — Analyzer mapping dictionary • Command: "nl -ba shared/integration/cli/run_all_analyzers.py | sed -n '1,200p'"
- orchestrate-issues.md:20 — Pre-commit formatting failure noted • Command: "nl -ba orchestrate-issues.md | sed -n '1,200p'"
- execplans/20251014-cli-migration-improvements.md:15 — Acceptance tests for enaible CLI • Command: "nl -ba execplans/20251014-cli-migration-improvements.md | sed -n '1,120p'"
- todos/cli-migration/cli-improvements.md:52 — Directive to remove path probing • Command: "nl -ba todos/cli-migration/cli-improvements.md | sed -n '1,200p'"
- (codex references removed)
- systems/claude-code/rules/global.claude.rules.md:12 — Result from UI library search cue • Command: "rg -n --hidden "@radix-ui/react-|shadcn/ui|tailwind\.config\.(ts|js|cjs)" ."

## Open Questions

- None.
