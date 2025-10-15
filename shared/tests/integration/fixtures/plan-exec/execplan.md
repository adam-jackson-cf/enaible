# ExecPlan: Enaible CLI Migration Pilot

- Status: Proposed
- Repo/Branch: `adam-versed/ai-assisted-workflows` • `main`
- Scope: feature • Priority: P1
- Start: 2025-10-15 • Last Updated: 2025-10-15T03:59Z
- Links: `shared/tests/integration/fixtures/plan-exec/spec.md:1`, `todos/cli-migration/cli-improvements.md:42`

## Purpose / Big Picture

Deliver a unified `enaible` CLI so prompts across Codex, Claude Code, and OpenCode call a single analyzer runner and renderer, eliminating brittle path probing and shrinking cross-system drift (`shared/tests/integration/fixtures/plan-exec/spec.md:21-55`).

## Success Criteria / Acceptance Tests

- [ ] `uv run enaible analyzers run quality:detect-secrets --target . --json --out .enaible/artifacts/detect-secrets.json` returns normalized schema with tool/version/findings fields (`shared/tests/integration/fixtures/plan-exec/spec.md:30-40`).
- [ ] `uv run enaible prompts render -s codex -p analyze-security -o .enaible/out` emits wrapper with Codex frontmatter rules respected (`shared/tests/integration/fixtures/plan-exec/spec.md:42-58`, `shared/tests/integration/fixtures/plan-exec/spec.md:127-154`).
- [ ] CI job `uv run enaible prompts diff` exits 0 with no unmanaged drift when run after rendering all systems (`shared/tests/integration/fixtures/plan-exec/spec.md:88-95`, `shared/tests/integration/fixtures/plan-exec/spec.md:171-173`).
- Non-Goals: Support for legacy script-path probing, hybrid prompt modes, or alternate runtimes beyond `uv` (per `shared/tests/integration/fixtures/plan-exec/spec.md:53-55`, `shared/tests/integration/fixtures/plan-exec/spec.md:65-68`).

## Context & Orientation

- Code: `shared/core/cli/run_analyzer.py:7-95`, `shared/core/base/registry_bootstrap.py:9-43`, `shared/prompts/analyze-security.md:22-108`, `systems/codex/prompts/analyze-security.md:15-112` (`shared/tests/integration/fixtures/plan-exec/report.md:15-36`).
- Data/Contracts: Analyzer JSON output produced by `shared/core/utils/output_formatter.py:73-185` and registry expectations in `shared/tests/unit/test_analyzer_registry.py:22-83` (`shared/tests/integration/fixtures/plan-exec/report.md:24-41`).
- Constraints/Assumptions: Keep analyzer contracts stable, codify `.enaible/artifacts/<prompt>/<timestamp>` convention, ensure adapters honor Codex frontmatter omission (`shared/tests/integration/fixtures/plan-exec/spec.md:39-41`, `shared/tests/integration/fixtures/plan-exec/spec.md:129-154`).

## Plan of Work (Prose)

1. Scaffold `tools/enaible` Typer CLI that shells into the existing analyzer registry and normalizes JSON payloads, aligning with the spec’s CLI surface (`shared/tests/integration/fixtures/plan-exec/spec.md:30-40`).
2. Establish prompt templating adapters and shared includes so system wrappers render from `shared/prompts/*` bodies while respecting Codex frontmatter decisions (`shared/tests/integration/fixtures/plan-exec/spec.md:42-60`, `shared/tests/integration/fixtures/plan-exec/spec.md:127-154`).
3. Replace legacy path-probing paragraphs in pilot prompts with `enaible` invocations, regenerate system-specific outputs, and add CI drift guardrails (`shared/tests/integration/fixtures/plan-exec/spec.md:51-95`).
4. Document install/update flows and align future optional installer command hooks with the resolved decisions around modes (`shared/tests/integration/fixtures/plan-exec/spec.md:133-166`).

## Concrete Steps (Checklist)

| #   | File                                      | Type   | Action                                                                                                                                                                                                        |
| --- | ----------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | tools/enaible/**init**.py                 | Write  | Create Typer app skeleton with version metadata and shared logging harness.                                                                                                                                   |
| 2   | tools/enaible/analyzers/run.py            | Write  | Wrap `shared/core/cli/run_analyzer.py` entrypoints into `enaible analyzers run` command with normalized output schema (`shared/tests/integration/fixtures/plan-exec/spec.md:30-40`).                          |
| 3   | tools/enaible/analyzers/list.py           | Write  | List available analyzers via registry bootstrap with machine-readable JSON table.                                                                                                                             |
| 4   | tools/enaible/prompts/render.py           | Write  | Load `shared/prompts/*.md` and render via Jinja templates under `docs/system/<system>/templates/*.j2` (`shared/tests/integration/fixtures/plan-exec/spec.md:42-60`).                                          |
| 5   | docs/system/codex/templates/base.j2       | Write  | Establish Codex wrapper template that omits YAML frontmatter per decision 1 (`shared/tests/integration/fixtures/plan-exec/spec.md:127-134`).                                                                  |
| 6   | docs/system/claude-code/templates/base.j2 | Update | Migrate/verify template location; align includes and metadata with shared adapter contract (`shared/tests/integration/fixtures/plan-exec/spec.md:79-87`).                                                     |
| 7   | shared/prompts/includes/session.j2        | Write  | Extract reusable session-history fragment referenced by adapters (`shared/tests/integration/fixtures/plan-exec/spec.md:48-49`).                                                                               |
| 8   | shared/prompts/analyze-security.md        | Update | Replace manual script-resolution paragraphs with `enaible analyzers run …` guidance (`shared/tests/integration/fixtures/plan-exec/spec.md:51-55`).                                                            |
| 9   | systems/codex/prompts/analyze-security.md | Update | Regenerate via `enaible prompts render` and stamp generated header (`shared/tests/integration/fixtures/plan-exec/spec.md:83-87`, `shared/tests/integration/fixtures/plan-exec/spec.md:150-154`).              |
| 10  | .github/workflows/ci-quality-gates.yml    | Update | Add drift check step invoking `enaible prompts render` + `enaible prompts diff` (`shared/tests/integration/fixtures/plan-exec/spec.md:88-95`, `shared/tests/integration/fixtures/plan-exec/spec.md:171-173`). |
| 11  | docs/system/<system>/templates/README.md  | Write  | Document adapter inputs, managed/unmanaged semantics, and install modes (`shared/tests/integration/fixtures/plan-exec/spec.md:150-166`).                                                                      |

## Progress (Running Log)

- (2025-10-15T03:59Z) Plan created; awaiting kickoff.

## Surprises & Discoveries

- Observation: Security prompts still perform manual analyzer path discovery, underscoring pilot priority • Evidence: `shared/prompts/analyze-security.md:22-46` (`shared/tests/integration/fixtures/plan-exec/report.md:17-36`).

## Decision Log

- Decision: Anchor CLI name, tech stack, and template locations on `enaible` with Typer + Jinja2.
  Rationale: Aligns all systems on a single packaged entrypoint and shared templating contracts (`shared/tests/integration/fixtures/plan-exec/spec.md:21-68`, `shared/tests/integration/fixtures/plan-exec/spec.md:140-146`).
  Date/Author: 2025-10-13 • enaible working group.
- Decision: `.enaible/` is the canonical artifacts root with managed/unmanaged prompt headers.
  Rationale: Prevents confusion across `.claude|.opencode|.codex` directories and protects author-owned files (`shared/tests/integration/fixtures/plan-exec/spec.md:131-166`).
  Date/Author: 2025-10-13 • enaible working group.

## Risks & Mitigations

- Risk: Analyzer schema drift causing downstream parsing failures • Mitigation: Freeze formatter contract via JSON schema test fixtures before exposing CLI (`shared/tests/integration/fixtures/plan-exec/spec.md:39-40`, `shared/tests/integration/fixtures/plan-exec/report.md:40-41`).
- Risk: Template relocation misses legacy files leading to render gaps • Mitigation: Script audit of `docs/system/**/templates` before migration and provide `migrate-templates` helper (`shared/tests/integration/fixtures/plan-exec/spec.md:79-82`, `shared/tests/integration/fixtures/plan-exec/spec.md:145-147`).
- Risk: CI drift check increases pipeline time • Mitigation: Cache rendered output directory and parallelize with existing tests (`shared/tests/integration/fixtures/plan-exec/spec.md:88-95`).

## Dependencies

- Upstream/Downstream: Analyzer registry (`shared/core/base/registry_bootstrap.py:9-43`), prompt bodies in `shared/prompts/*`, system wrappers in `docs/system/<system>/templates`.
- External Events: Future `uv` release cadence and PyPI namespace approval for `enaible`.

## Security / Privacy / Compliance

- Data touched: Repository source files and analyzer configuration metadata only; no PII expected.
- Secrets: None; analyzer commands rely on existing configuration without embedding credentials (`shared/tests/integration/fixtures/plan-exec/spec.md:51-55`).
- Checks: Maintain detect-secrets analyzer and security prompt coverage in CI (`shared/tests/integration/fixtures/plan-exec/report.md:33-36`).

## Observability (Optional)

- Metrics: CLI invocation counts and exit codes captured via future `.enaible/artifacts` metadata summary.
- Logs/Traces: Emit structured JSON logs under `.enaible/artifacts/<prompt>/<timestamp>/run.log` for troubleshooting.
- Feature Flags/Experiments: None in scope for v1.

## Test Plan

- Unit: Add Typer command tests for analyzers and prompt renderers using pytest fixtures (`shared/tests/integration/fixtures/plan-exec/report.md:52-62`).
- Integration/E2E: Execute `uv run enaible prompts render -s all -p analyze-security,get-primer -o .enaible/out` followed by analyzer run smoke tests.
- Performance/Accessibility: Target sub-2s CLI startup by reusing registry bootstrap cache; accessibility out of scope for CLI.
- How to run: `uv sync && PYTHONPATH=shared uv run pytest tools/enaible/tests -v`.

### Quality Gates

| Gate        | Command                                     | Threshold / Expectation |
| ----------- | ------------------------------------------- | ----------------------- |
| Lint        | `uv run ruff check .`                       | 0 errors                |
| Type        | `uv run mypy tools/enaible`                 | 0 errors                |
| Tests       | `uv run pytest tools/enaible/tests -v`      | 100% passing            |
| Duplication | `uv run python -m shared.tools.jscpd_check` | ≤ 3%                    |
| Complexity  | `uv run python -m lizard tools/enaible`     | Max CC ≤ 10             |

## PR & Review

- PR URL: <to be filled>
- PR Number/Status: <number> • <OPEN>
- Required Checks: Ruff, mypy, pytest, drift check • Last CI run: <pending>

## Handoff & Next Steps

- Remaining work to productionize: Publish `enaible` via `uv tool install`, update docs/installation guides, train prompt authors on adapters.
- Follow-ups/backlog: Extend `enaible install <system>` flows, add caching for analyzer runs, integrate Semgrep once available.

## Outcomes & Retrospective

- Result vs Goals: Pending implementation; update after pilot render completes.
- What went well: To be captured after execution.
- What to change next time: To be captured after execution.
