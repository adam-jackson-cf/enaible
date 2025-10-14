# ExecPlan: Enaible CLI Migration Kickoff

- Status: Proposed
- Repo/Branch: `adam-versed/ai-assisted-workflows` • `main`
- Scope: feature • Priority: P1
- Start: 2025-10-14 • Last Updated: 2025-10-14T22:57Z
- Links: `shared/tests/integration/fixtures/plan-exec/spec.md`, `shared/tests/integration/fixtures/plan-exec/report.md`, `todos/cli-migration/cli-improvements.md`

## Purpose / Big Picture

Stand up the `enaible` CLI so Codex, Claude Code, and OpenCode prompts invoke analyzers and render prompt variants through one maintained interface, eliminating brittle path probing and reducing template drift across systems.

## Success Criteria / Acceptance Tests

- [ ] `enaible analyzers run <category:tool>` executes existing analyzers with normalized JSON output and exit codes validated against registry expectations.
- [ ] `enaible prompts render|diff|sync` renders Codex and Claude pilot prompts from shared bodies/templates and fails CI when managed outputs drift.
- [ ] Pilot prompts (`analyze-security`, `get-primer`) call `enaible` instead of ad-hoc script resolution, with Codex variant remaining frontmatter-free.
- Non-Goals: Reintroducing legacy script-discovery flows, widening analyzer scope beyond currently registered tools, or building installer UX beyond agreed v1 behaviors.

## Context & Orientation

- Code: `shared/core/cli/run_analyzer.py`, `shared/prompts/analyze-security.md`, `systems/codex/prompts/analyze-security.md`, `systems/claude-code/commands/analyze-security.md`
- Data/Contracts: Analyzer registry JSON schema (normalize to `tool`, `version`, `timestamps`, `findings[]`, `stats`, `exit_code`); managed prompt header `<!-- generated: enaible -->`.
- Constraints/Assumptions: No dual-mode fallbacks; Typer/Click + Jinja2; maintain cyclomatic complexity ≤ 10; enforce instructions in `systems/claude-code/rules/global.claude.rules.md`.

## Plan of Work (Prose)

1. Map current prompt/template locations and reconcile with target `docs/system/<system>/templates/*.j2` structure to avoid drift during migration.
2. Scaffold the `enaible` CLI package under `tools/enaible/` using Typer, wiring analyzer registry entry points for `analyzers run|list` with normalized JSON output.
3. Introduce prompt templating utilities (Jinja2 includes, system adapters) and migrate the pilot prompts, replacing legacy path-probing with CLI invocations, followed by CI drift enforcement.

## Concrete Steps (Checklist)

| #   | File                                                       | Type     | Action                                                                                                       |
| --- | ---------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------ | ----- | ------ | ---------------- |
| 1   | docs/system                                                | Research | Inventory existing template locations and confirm migration targets under `docs/system/<system>/templates/`. |
| 2   | shared/prompts/includes                                    | Write    | Create reusable Jinja2 includes for session history and analyzer callouts.                                   |
| 3   | tools/enaible/**init**.py                                  | Write    | Initialize Typer app with project metadata and CLI entry point.                                              |
| 4   | tools/enaible/analyzers/run.py                             | Write    | Wrap `shared/core/cli/run_analyzer.py` to execute analyzers with normalized JSON schema and exit codes.      |
| 5   | tools/enaible/analyzers/list.py                            | Write    | Enumerate registered analyzers via registry bootstrap.                                                       |
| 6   | tools/enaible/prompts/render.py                            | Write    | Implement templating pipeline that reads shared bodies and system templates into managed outputs.            |
| 7   | tools/enaible/prompts/diff.py                              | Write    | Add drift detection comparing rendered outputs to committed files.                                           |
| 8   | tools/enaible/prompts/sync.py                              | Write    | Provide sync command to update managed prompt artifacts.                                                     |
| 9   | tools/enaible/install.py                                   | Write    | Implement installer surface with `fresh                                                                      | merge | update | sync` behaviors. |
| 10  | shared/prompts/analyze-security.md                         | Update   | Replace path-probing instructions with `enaible analyzers run` invocation and managed artifact header.       |
| 11  | shared/prompts/get-primer.md                               | Update   | Apply same CLI invocation pattern as pilot prompt.                                                           |
| 12  | docs/system/codex/templates/analyze-security.j2            | Write    | Encode Codex adapter wrapper without frontmatter and include managed header.                                 |
| 13  | docs/system/claude-code/templates/analyze-security.j2      | Write    | Encode Claude-specific frontmatter and include managed header.                                               |
| 14  | systems/codex/prompts/analyze-security.md                  | Write    | Regenerate via `enaible prompts render` and ensure managed marker present.                                   |
| 15  | systems/claude-code/commands/analyze-security.md           | Write    | Regenerate with new CLI instructions and permissions guidance.                                               |
| 16  | .github/workflows/ci-quality-gates.yml                     | Update   | Add `uv run enaible prompts diff --systems all --prompts all` quality gate.                                  |
| 17  | shared/tests/integration/test_integration_all_analyzers.py | Update   | Cover `enaible analyzers run` wrapper invocation.                                                            |
| 18  | tools/enaible/tests                                        | Write    | Add CLI unit tests for analyzers and prompts commands.                                                       |
| 19  | docs/analysis-scripts.md                                   | Update   | Document `enaible` workflow and artifact directories.                                                        |

## Progress (Running Log)

- (2025-10-14T22:57Z) Plan created; awaiting stakeholder review.

## Surprises & Discoveries

- None yet.

## Decision Log

- Decision: CLI name `enaible`, Typer/Click + Jinja2 stack, managed prompt headers, and installer modes.
  Rationale: Aligns with 2025-10-13 architecture agreement to remove path probing and centralize tooling.
  Date/Author: 2025-10-14 • Codex (GPT-5)

## Risks & Mitigations

- Risk: Analyzer output schema drift causing downstream incompatibility • likelihood medium • Mitigation: Validate against registry schema and add unit tests before replacing prompts.
- Risk: Template migration overwrites unmanaged prompts • likelihood low • Mitigation: Honor `<!-- generated: enaible -->` guard and audit destinations prior to sync.
- Risk: Installer behaviors diverge from legacy scripts • likelihood medium • Mitigation: Mirror existing shell installer logic and provide dry-run with backups.

## Dependencies

- Upstream/Downstream: Analyzer registry bootstrap, shared prompt bodies, system rules/commands.
- External Events: CI integration updates; potential stakeholder sign-off on CLI packaging.

## Security / Privacy / Compliance

- Data touched: None (no PII); analyzer results remain local artifacts.
- Secrets: None; rely on existing secrets scanning analyzers.
- Checks: Maintain detect-secrets, Ruff, and future Semgrep gates via CI.

## Observability (Optional)

- Metrics: Track CLI command durations and analyzer success/failure counts in future release.
- Logs/Traces: Provide structured JSON logs for CLI commands when `--verbose` enabled.
- Feature Flags/Experiments: Consider `ENAIBLE_EXPERIMENTAL` env flag for beta adapters.

## Test Plan

- Unit: `uv run pytest tools/enaible/tests -v`
- Integration/E2E: `PYTHONPATH=shared uv run pytest shared/tests/integration/test_integration_all_analyzers.py -v`
- Performance/Accessibility: N/A for CLI; monitor command runtimes manually.
- How to run: `uv run enaible analyzers run quality:coverage --target . --json`

### Quality Gates

| Gate        | Command                              | Threshold / Expectation |
| ----------- | ------------------------------------ | ----------------------- |
| Lint        | `uv run ruff check .`                | 0 errors                |
| Type        | `uv run mypy tools/enaible shared`   | 0 errors                |
| Tests       | `uv run pytest -v`                   | 100% passing            |
| Duplication | `uv run jscpd --min-lines 5`         | ≤ 3%                    |
| Complexity  | `uv run lizard tools/enaible shared` | Max CC ≤ 10             |

## PR & Review

- PR URL: <to be filled>
- PR Number/Status: <number> • <OPEN>
- Required Checks: Ruff, Mypy, pytest, enaible drift • Last CI run: <pending>

## Handoff & Next Steps

- Remaining work to productionize: Publish `enaible` to internal package index; author runbook and migration guide.
- Follow-ups/backlog: Evaluate `enaible doctor` command telemetry; scope PostHog integration post-consent.

## Outcomes & Retrospective

- Result vs Goals: Pending • Evidence: <pending>
- What went well: <pending>
- What to change next time: <pending>
