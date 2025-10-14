# ExecPlan: Enaible CLI Phase 1 Migration

- Status: Proposed
- Repo/Branch: `local/ai-assisted-workflows` • `main`
- Scope: feature • Priority: P1
- Start: 2025-10-14 • Last Updated: 2025-10-14T22:29Z
- Links: spec `shared/tests/integration/fixtures/plan-exec/spec.md`; report `shared/tests/integration/fixtures/plan-exec/report.md`; backlog `todos/cli-migration/cli-improvements.md`

## Purpose / Big Picture

Accelerate the CLI migration by delivering the first Enaible CLI slice that centralizes analyzer invocation and prompt rendering so the Codex, Claude Code, and OpenCode systems stop duplicating brittle path-probing workflows, reducing drift and improving maintainability.

## Success Criteria / Acceptance Tests

- [ ] `uv run enaible analyzers list` enumerates all registered analyzer ids with the normalized JSON schema v1 contract.
- [ ] `uv run enaible prompts render -s claude-code -p analyze-security -o .enaible/artifacts` regenerates the managed prompt with `<!-- generated: enaible -->` header and no legacy path-probing text.
- [ ] `uv run enaible prompts diff` reports no drift after migrating the `analyze-security` and `get-primer` prompts.
- Non-Goals: Shipping optional `enaible install` modes beyond scaffolding; migrating unmanaged, system-specific prompts.

## Context & Orientation

- Code: `shared/prompts/analyze-security.md:22`, `systems/codex/prompts/analyze-security.md:15`, `shared/core/cli/run_analyzer.py:7`
- Data/Contracts: Analyzer registry JSON outputs (`shared/core/utils/output_formatter.py:73`), prompt rendering templates (`docs/system/*/templates` placeholder paths).
- Constraints/Assumptions: Use Typer+Jinja2 under `tools/enaible/`; no fallback modes; maintain JSON output compatibility as defined in spec decisions.

## Plan of Work (Prose)

1. Catalog current prompt templates and wrappers, confirming or relocating them under `docs/system/<system>/templates/*` to eliminate drift and document any gaps.
2. Scaffold the `enaible` CLI package in `tools/enaible/cli.py:app`, wiring Typer commands for `analyzers list|run` that delegate to `shared/core/cli/run_analyzer.py:main` while enforcing the normalized JSON schema.
3. Implement prompt rendering adapters in `tools/enaible/prompts/renderer.py:render_prompt` using Jinja2 templates and shared prompt bodies; support system metadata casing per adapter.
4. Migrate `shared/prompts/analyze-security.md` and `shared/prompts/get-primer.md` to call the new CLI, regenerate system-specific outputs, and remove legacy path-probing blocks under `systems/*/(commands|prompts)/`.
5. Add CI hooks so `enaible prompts render --systems all --prompts all` and `enaible prompts diff` are wired into `.github/workflows/ci-quality-gates-incremental.yml:17` without bypassing existing quality gates.

## Concrete Steps (Checklist)

| #   | File                                                 | Type   | Action                                                                                  |
| --- | ---------------------------------------------------- | ------ | --------------------------------------------------------------------------------------- |
| 1   | `docs/system/claude-code/templates`                  | Write  | Ensure wrapper templates exist; migrate legacy markdown into Jinja2 scaffolds.          |
| 2   | `docs/system/opencode/templates`                     | Write  | Mirror template structure and document adapter metadata placeholders.                   |
| 3   | `docs/system/codex/templates`                        | Write  | Create Codex wrapper templates without YAML frontmatter per decision #1.                |
| 4   | `tools/enaible/__init__.py`                          | Write  | Initialize package exports and Typer `app`.                                             |
| 5   | `tools/enaible/cli.py`                               | Write  | Define Typer commands for analyzers list/run, prompts render/diff/validate, and doctor. |
| 6   | `tools/enaible/analyzers/service.py`                 | Write  | Wrap registry bootstrap and normalize JSON schema for CLI output.                       |
| 7   | `tools/enaible/prompts/renderer.py`                  | Write  | Load shared prompt bodies and render system templates via Jinja2 includes.              |
| 8   | `shared/prompts/analyze-security.md`                 | Update | Remove path-probing text; replace with `enaible analyzers run` instructions.            |
| 9   | `shared/prompts/get-primer.md`                       | Update | Reference `enaible` invocation and shared includes.                                     |
| 10  | `systems/claude-code/commands/analyze-security.md`   | Update | Regenerate managed file via CLI and add generated header.                               |
| 11  | `systems/codex/prompts/analyze-security.md`          | Update | Regenerate managed file via CLI, ensuring no frontmatter.                               |
| 12  | `systems/opencode/command/analyze-security.md`       | Update | Regenerate managed file via CLI with system-specific frontmatter.                       |
| 13  | `.github/workflows/ci-quality-gates-incremental.yml` | Update | Add Enaible render/diff steps after install stage.                                      |
| 14  | `shared/tests/integration/test_enaible_cli.py`       | Add    | Cover CLI list/run behavior using temporary artifacts directory.                        |

## Progress (Running Log)

- (2025-10-14T22:29Z) Plan created; pending stakeholder review.

## Surprises & Discoveries

- Observation: Legacy prompts still perform path probing in Codex variant • Evidence: `systems/codex/prompts/analyze-security.md:15`

## Decision Log

- Decision: Adopt Typer + Jinja2 within `tools/enaible/` and store artifacts under `.enaible/` • Rationale: Aligns with spec decisions (spec.md) for maintainability and portability • Date/Author: 2025-10-14 • Codex

## Risks & Mitigations

- Risk: Analyzer schema divergence causing CLI regressions • Mitigation: Define shared dataclass in `tools/enaible/analyzers/service.py` and add contract tests.
- Risk: Template relocation breaking unmanaged prompts • Mitigation: Keep unmanaged files untouched and document exclusions before running sync.

## Dependencies

- Upstream/Downstream: Shared analyzer registry (`shared/core/base/registry_bootstrap.py`), prompt bodies (`shared/prompts/*.md`), CI workflow definitions (`.github/workflows/ci-quality-gates-incremental.yml`).
- External Events: None identified; CLI packaging via `uv` assumed available.

## Security / Privacy / Compliance

- Data touched: Analyzer metadata only; no PII.
- Secrets: None; CLI must consume existing secrets via environment without storing them.
- Checks: Ensure detect-secrets analyzer remains runnable via new CLI path.

## Observability (Optional)

- Metrics: Pending definition; likely counts of analyzer runs per invocation.
- Logs/Traces: CLI should reuse shared logging in `shared/core/base/analyzer_base.py`.
- Feature Flags/Experiments: None scoped for phase 1.

## Test Plan

- Unit: Add Typer command tests for analyzers and prompt rendering modules.
- Integration/E2E: Execute `uv run enaible prompts render` followed by `uv run enaible prompts diff` against pilot prompts.
- Performance/Accessibility: Ensure CLI completes analyzer list/run within existing sequential bounds; no UI scope.
- How to run: `uv run pytest tools/enaible/tests -v`

### Quality Gates

| Gate        | Command                                          | Threshold / Expectation |
| ----------- | ------------------------------------------------ | ----------------------- |
| Lint        | `uv run ruff check tools/enaible`                | 0 errors                |
| Type        | `uv run mypy tools/enaible`                      | 0 errors                |
| Tests       | `uv run pytest tools/enaible/tests -v`           | 100% passing            |
| Duplication | `uv run jscpd --min-lines 8 tools/enaible`       | ≤ 3%                    |
| Complexity  | `uv run python -m lizard tools/enaible --CCN 10` | Max CC ≤ 10             |

## PR & Review

- PR URL: <to be filled>
- PR Number/Status: <pending> • <OPEN>
- Required Checks: CI quality gates, Enaible render/diff, pytest • Last CI run: <pending>

## Handoff & Next Steps

- Remaining work to productionize: Document CLI usage in README and system-specific guides; plan installer modes for phase 2.
- Follow-ups/backlog: Evaluate caching strategy for analyzer runs; design `enaible doctor` deep diagnostics.

## Outcomes & Retrospective

- Result vs Goals: pending • Evidence: <pending>
- What went well: <pending>
- What to change next time: <pending>
