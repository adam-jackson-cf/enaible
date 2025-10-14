# ExecPlan: Enaible CLI Migration Phase 1

- Status: Proposed
- Repo/Branch: `adamjackson/ai-assisted-workflows` • `main`
- Scope: feature • Priority: P1
- Start: 2025-10-14 • Last Updated: 2025-10-14T22:22Z
- Links: spec `shared/tests/integration/fixtures/plan-exec/spec.md`; report `shared/tests/integration/fixtures/plan-exec/report.md`; backlog `todos/cli-migration/cli-improvements.md`

## Purpose / Big Picture

Deliver the `enaible` CLI so all systems (Claude Code, OpenCode, Codex) invoke analyzers and render prompts through a unified, versioned interface, eliminating brittle script path discovery and reducing drift across system-specific wrappers.

## Success Criteria / Acceptance Tests

- [ ] `uv run enaible analyzers run quality:detect-secrets --target shared` succeeds and outputs normalized JSON with tool metadata, timestamps, and exit codes.
- [ ] `uv run enaible prompts render --systems all --prompts all --out .enaible/artifacts/latest` regenerates system wrappers without producing drift on subsequent `enaible prompts diff`.
- [ ] `enaible prompts render` writes managed files with `<!-- generated: enaible -->` header while leaving unmanaged files untouched during `enaible install codex --mode merge`.
- Non-Goals: Support for legacy path-probing inside prompts, partial `install` behaviors that skip agent assets, or bespoke fallbacks per system.

## Context & Orientation

- Code: `shared/core/cli/run_analyzer.py:main`, `shared/analyzers/**`, `systems/*/prompts/**`
- Data/Contracts: Analyzer JSON schema draft (`todos/cli-migration/cli-improvements.md`), prompt bodies under `shared/prompts/*.md`
- Constraints/Assumptions: Typer-based CLI packaged with `uv`; templates live under `docs/system/<system>/templates/*.j2`; complexity per function must remain ≤10.

## Plan of Work (Prose)

1. Implement `tools/enaible/cli.py:app` Typer entrypoint with subcommands delegating to `shared/core/cli/run_analyzer.py:main` for analyzer execution and template helpers for prompt operations.
2. Build templating adapters in `tools/enaible/prompts/render.py:render_prompts` and confirm wrappers live under `docs/system/<system>/templates/*.j2`, moving legacy templates if required.
3. Refactor shared prompts such as `shared/prompts/analyze-security.md` to call `enaible analyzers run` and regenerate system-specific outputs; add CI drift guard in `.github/workflows/ci-quality-gates.yml`.
4. Extend installation workflow via `tools/enaible/install.py:install_system` to copy managed/unmanaged assets according to selected mode and update documentation (`docs/installation.md`).

## Concrete Steps (Checklist)

| #   | File                                      | Type   | Action                                                                                                   |
| --- | ----------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| 1   | tools/enaible/cli.py                      | Write  | Scaffold Typer `app` with `analyzers` and `prompts` command groups.                                      |
| 2   | tools/enaible/analyzers/run.py            | Write  | Wrap registry via `run_analyzer.main` and emit normalized JSON schema.                                   |
| 3   | tools/enaible/prompts/render.py           | Write  | Load `shared/prompts/*.md` and Jinja2 templates from `docs/system/<system>/templates` to render outputs. |
| 4   | docs/system/_/templates/_.j2              | Move   | Relocate or create system wrapper templates under standardized directory.                                |
| 5   | shared/prompts/analyze-security.md        | Update | Replace path-probing instructions with `enaible analyzers run` guidance and includes.                    |
| 6   | systems/codex/prompts/analyze-security.md | Update | Regenerate via CLI with `<!-- generated: enaible -->` marker.                                            |
| 7   | tools/enaible/install.py                  | Write  | Implement install modes (`fresh`, `merge`, `update`, `sync`) respecting managed/unmanaged files.         |
| 8   | .github/workflows/ci-quality-gates.yml    | Update | Add `enaible prompts render` + `enaible prompts diff` quality gates.                                     |
| 9   | docs/installation.md                      | Update | Document `uv tool install enaible` flow and managed artifact directory `.enaible/`.                      |

## Progress (Running Log)

- (2025-10-14T22:22Z) Plan drafted; awaiting approval to begin implementation.

## Surprises & Discoveries

- Observation: None yet • Evidence: n/a

## Decision Log

- Decision: Use Typer-based `enaible` CLI with `.enaible/` artifact root.
  Rationale: Aligns with 2025-10-13 migration decisions to centralize CLI tooling and artifact storage.
  Date/Author: 2025-10-14 • Codex
- Decision: Preserve Codex prompts without YAML frontmatter while still passing through template rendering.
  Rationale: Maintains Codex UX conventions while enabling managed generation.
  Date/Author: 2025-10-14 • Codex

## Risks & Mitigations

- Risk: Analyzer JSON schema changes break downstream consumers • Mitigation: Add contract tests in `tools/enaible/tests/test_analyzers_schema.py` and version schema in CLI output.
- Risk: Template relocation misses unmanaged prompts • Mitigation: Inventory existing prompt locations via `rg --files systems` before moves and flag discrepancies in plan log.
- Risk: Install modes overwrite user customization • Mitigation: Compute checksums before writes and require explicit `--fresh` for destructive actions.

## Dependencies

- Upstream/Downstream: relies on `shared/core/base/registry_bootstrap.py` for analyzer discovery; integrates with `systems/<system>` assets for distribution.
- External Events: None identified.

## Security / Privacy / Compliance

- Data touched: Repository-local prompt content only; no PII.
- Secrets: None; CLI must respect existing secret scanning by Detect Secrets.
- Checks: Ensure `uv run detect-secrets scan` remains in CI after CLI integration.

## Observability (Optional)

- Metrics: Capture CLI invocation durations via verbose logging (`--timing`) for future optimization.
- Logs/Traces: Emit structured log lines to stdout with run id and target path.
- Feature Flags/Experiments: Consider `ENAIBLE_EXPERIMENTAL_INSTALL` flag for beta features.

## Test Plan

- Unit: Cover CLI command parsing and schema serialization (`uv run pytest tools/enaible/tests/unit -v`).
- Integration/E2E: Execute `uv run pytest shared/tests/integration/test_integration_all_analyzers.py -v` with CLI entrypoint.
- Performance/Accessibility: Ensure `enaible analyzers run` completes typical security scan in <30s on reference repo.
- How to run: `uv sync && uv run pytest tools/enaible/tests -v`

### Quality Gates

| Gate        | Command                                                    | Threshold / Expectation |
| ----------- | ---------------------------------------------------------- | ----------------------- |
| Lint        | `uv run ruff check tools/enaible`                          | 0 errors                |
| Type        | `uv run mypy tools/enaible`                                | 0 errors                |
| Tests       | `uv run pytest tools/enaible/tests -v`                     | 100% passing            |
| Duplication | `uv run jscpd --min-tokens 50 --threshold 3 tools/enaible` | ≤ 3%                    |
| Complexity  | `uv run lizard tools/enaible --CCN 10`                     | Max CC ≤ 10             |

## PR & Review

- PR URL: Pending
- PR Number/Status: Pending • OPEN
- Required Checks: CI quality gates, `enaible prompts diff` • Last CI run: Pending

## Handoff & Next Steps

- Remaining work to productionize: Publish CLI via `uv tool install`, update release notes, coordinate adoption with system maintainers.
- Follow-ups/backlog: Automate `enaible doctor` environment diagnostics; evaluate future Convex integration hooks.

## Outcomes & Retrospective

- Result vs Goals: Pending • Evidence: TBD
- What went well: Pending execution
- What to change next time: Pending execution
