# ExecPlan: Launch Enaible CLI Migration

- Status: In Progress
- Repo/Branch: `adam-versed/ai-assisted-workflows` • `main`
- Scope: feature • Priority: P1
- Start: 2025-10-15 • Last Updated: 2025-10-15T20:20Z
- Links: todos/cli-migration/spec.md; todos/cli-migration/scout.md

## Purpose / Big Picture

Unify analyzer execution and prompt generation across Claude Code, OpenCode, and Codex by delivering the `enaible` CLI, eliminating duplicated path-probing logic, and standardizing artifacts so teams gain faster, safer rollout of shared workflows.

## Success Criteria / Acceptance Tests

- [x] `uv run enaible analyzers list` enumerates every registered analyzer with normalized metadata.
- [x] `uv run enaible prompts render -s claude-code -p analyze-security -o systems/claude-code/commands` regenerates managed prompts without producing diffs.
- [x] `uv run enaible prompts diff` exits 0 during CI, proving rendered prompts are synchronized.
- Non-Goals: Redesigning analyzer internals, introducing new analyzer categories, or supporting legacy path-probing modes once migration completes.

## Tech stack

- **Languages**: Python 3.11+, Markdown
- **Frameworks**: Typer for CLI command graph, Jinja2 for templating.citeturn4search1
- **Build Tools**: uv for environment management and command execution (`uv sync`, `uv run`, `uv tool install`).citeturn4search0
- **Package Managers**: uv (primary), pip-compatible exports for distribution
- **Testing**: pytest (unit/integration), CLI contract tests via `uv run`

## Constraints

- Package and distribute `enaible` exclusively with uv workflows (`uv sync`, `uv tool install`) to ensure reproducible installs.citeturn4search0
- Implement the CLI with Typer command groups and callback patterns to keep the surface ergonomic and testable.citeturn4search1
- Honor 2025-10-13 migration decisions: `.enaible/` is the artifact root and prompts must not retain legacy path-probing fallbacks.
- Follow global AI-Assisted Workflows rules: minimize complexity, prefer established libraries, remove rather than duplicate legacy behavior, and avoid introducing fallbacks.

## Development approach

- Scaffold `tools/enaible/` under uv with strict typing, lean dependencies, and Typer-powered subcommands.
- Wrap the existing analyzer registry via injected adapters; never fork analyzer logic or create dual execution paths.
- Migrate prompt templates to managed Jinja2 renders, rendering pilots before scaling to all prompts.
- Sequence work with atomic commits and enforce quality gates (ruff, mypy, pytest, `enaible` smoke tests) before merging.
- Document all operational commands and quality gates in `docs/` and `session-notes.md` per workflow habits.

## Context & Orientation

- Code: `shared/core/base/analyzer_registry.py:1`, `shared/core/cli/run_analyzer.py:1`, `shared/prompts/analyze-security.md:1`
- Data/Contracts: analyzer JSON schema draft (to finalize under `.enaible/schema.json`), prompt metadata for Claude/OpenCode/Codex
- Constraints/Assumptions: uv becomes authoritative package manager; Codex outputs remain frontmatter-free; installers must support `fresh|merge|update|sync` semantics without destructive defaults.

## High level Phase Plan

- Phase 1:
  - [x] CLI foundation – scaffold uv project, Typer entrypoint, baseline docs/tests
- Phase 2:
  - [x] Analyzer integration – wrap registry, define JSON schema, implement `run`/`list`
- Phase 3:
  - [x] Prompt templating – ensure templates live under `docs/system/<system>/templates`, add adapters/includes
- Phase 4:
  - [x] Prompt migration – refactor shared prompts, render pilot systems, lock diff workflow
- Phase 5:
  - [x] CI & quality gates – introduce drift checks, CLI smoke tests, artifact ignores
- Phase 6:
  - [ ] Installer uplift & rollout – build `enaible install`, docs, adoption playbook

## Detailed Phase Task Steps

- Keep progress updated at start and end of tasks

### Status key:

"@" - in progress
"X" - complete
" " - outstanding

### Type key:

"Code" - code implementation action write/edit
"Read" - reviewing a flie
"Action" - a none code or read action like mcp call, bash command, or ,
"Test" - creating/editing/running any kind of test
"Gate" - quality gate actions - create/edit/run
"Human" - manual action that requires human involvement

| Status | Phase # | Task # | Task Type | Description                                                                                                                                      |
| ------ | ------- | ------ | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----- | ------ | --------------------------------------------------------------- |
| X      | 1       | 1      | Read      | Review `shared/core/base/analyzer_registry.py:1` to map registry APIs needed by Typer commands.                                                  |
| X      | 1       | 2      | Read      | Inspect `shared/core/cli/run_analyzer.py:1` to capture current argparse behavior and options.                                                    |
| X      | 1       | 3      | Code      | Create `tools/enaible/pyproject.toml:1` scoped for uv with Typer, Jinja2, and strict type settings.                                              |
| X      | 1       | 4      | Code      | Add `tools/enaible/src/enaible/__init__.py:1` and `tools/enaible/src/enaible/__main__.py:1` with Typer app skeleton.                             |
| X      | 1       | 5      | Test      | Establish CLI smoke test at `tools/enaible/tests/test_cli_smoke.py:1` covering `--help` and empty commands.                                      |
| X      | 1       | 6      | Action    | Run `uv sync` in `tools/enaible/` to materialize the new project environment.                                                                    |
| X      | 2       | 7      | Code      | Implement `analyzers run` command in `tools/enaible/src/enaible/commands/analyzers.py:1`, delegating to registry adapters.                       |
| X      | 2       | 8      | Code      | Define normalized result schema in `tools/enaible/src/enaible/models/results.py:1` and persist schema to `.enaible/schema.json:1`.               |
| X      | 2       | 9      | Test      | Add contract tests `tools/enaible/tests/test_analyzers_run.py:1` covering exit codes and JSON output.                                            |
| X      | 2       | 10     | Code      | Implement `analyzers list` with registry introspection in `tools/enaible/src/enaible/commands/analyzers.py:120`.                                 |
| X      | 3       | 11     | Read      | Audit template directories `docs/system/claude-code/templates/:1` and `docs/system/codex/templates/:1` for gaps.                                 |
| X      | 3       | 12     | Code      | Create adapter module at `tools/enaible/src/enaible/prompts/adapters.py:1` producing frontmatter/context per system.                             |
| X      | 3       | 13     | Code      | Build render pipeline in `tools/enaible/src/enaible/commands/prompts.py:1` with Jinja2 env and includes.                                         |
| X      | 3       | 14     | Test      | Add golden template tests `tools/enaible/tests/test_prompts_render.py:1` comparing rendered output fixtures.                                     |
| X      | 4       | 15     | Read      | Review `shared/prompts/analyze-security.md:1` and `shared/prompts/get-primer.md:1` to plan replacement of path-probing blocks.                   |
| X      | 4       | 16     | Code      | Refactor shared prompts under `shared/prompts/*.md:1` to invoke `enaible analyzers run …` and remove legacy instructions.                        |
| X      | 4       | 17     | Action    | Execute `uv run enaible prompts render -s claude-code -p analyze-security -o systems/claude-code/commands` for pilot validation.                 |
| X      | 4       | 18     | Test      | Capture pre/post diffs via `uv run enaible prompts diff` ensuring zero drift before expanding scope.                                             |
| X      | 5       | 19     | Code      | Add CI job in `.github/workflows/ci-quality-gates-incremental.yml:1` invoking `uv run enaible prompts render` and `uv run enaible prompts diff`. |
| X      | 5       | 20     | Code      | Update `.gitignore:1` to include `.enaible/` artifacts and rendered scratch directories.                                                         |
| X      | 5       | 21     | Test      | Author CLI smoke script `tools/enaible/tests/test_cli_doctor.py:1` covering `enaible doctor`.                                                    |
| X      | 5       | 22     | Gate      | Document quality gate commands in `README.md:1` and `docs/system/claude-code/templates/USAGE.md:1`.                                              |
| X      | 6       | 23     | Code      | Implement `enaible install` command with `fresh                                                                                                  | merge | update | sync`modes in`tools/enaible/src/enaible/commands/install.py:1`. |
| X      | 6       | 24     | Test      | Write integration test `tools/enaible/tests/test_install_command.py:1` validating merge/update behaviors on managed/unmanaged files.             |
| X      | 6       | 25     | Action    | Produce rollout playbook in `docs/enaible/migration-guide.md:1` and update `session-notes.md:1` with adoption milestones.                        |
| X      | 6       | 26     | Human     | Schedule enablement session with system owners to hand off new CLI workflows.                                                                    |

## Progress Per Session (Running Summary Log)

- (2025-10-15T18:00Z) ExecPlan created; execution pending kickoff approval.
- (2025-10-15T20:20Z) Phases 1-4 completed; Typer upgraded to 0.18.0 to restore CLI help, analyzer commands & pilot prompt renders validated.
- (2025-10-15T21:10Z) Added Enaible CI job, finalized doctor diagnostics (with tests), and confirmed prompt diff gate.
- (2025-10-15T22:00Z) Delivered Enaible install modes with regression tests and documented local quality gate workflow.

## Surprises & Discoveries

- Observation: `tools/` directory is presently empty, confirming greenfield space for `enaible` package.
- Observation: Typer 0.12.x is incompatible with Click 8.3.0; upgrading to Typer 0.18.0 resolves the secondary flag/metavar errors seen during `enaible --help`.

## Decision Log

- Decision: Codex outputs remain frontmatter-free; metadata limited to optional HTML comments.
  Rationale: Aligns with 2025-10-13 migration decisions and preserves Codex conventions.
  Date/Author: 2025-10-13 • Enaible working group
- Decision: `.enaible/` is the canonical artifact root for CLI outputs.
  Rationale: Keeps artifacts system-agnostic and avoids clashing with existing `.claude/` or `.codex/` directories.
  Date/Author: 2025-10-13 • Enaible working group
- Decision: Standardize on Typer ≥0.18.0 to remain compatible with Click 8.3+ in the Enaible CLI project.
  Rationale: Eliminates runtime errors surfaced by the analyzer/prompt commands and keeps dependencies current without pinning Click.
  Date/Author: 2025-10-15 • CLI migration team
- Decision: Enaible install defaults to `merge` mode with managed-file detection; other modes (`update`, `sync`, `fresh`) are available for targeted deployment scenarios.
  Rationale: Provides predictable rollout tooling while preserving unmanaged customizations by default.
  Date/Author: 2025-10-15 • CLI migration team

## Risks & Mitigations

- Risk: Analyzer JSON schema drift could break consumers • Mitigation: lock schema in `.enaible/schema.json`, add contract tests, require approval for schema changes.
- Risk: Prompt regeneration may overwrite unmanaged files • Mitigation: enforce `<!-- generated: enaible -->` markers and respect unmanaged file protections in installer logic.
- Risk: uv adoption friction among contributors • Mitigation: document `uv` workflows, provide `uv tool install enaible` instructions, pair during rollout.citeturn4search0

## Dependencies

- Upstream/Downstream: Analyzer maintainers (for schema validation), Docs team (template updates), CI owners (workflow changes)
- External Events: uv release cadence for tooling stability, Typer updates for CLI features.citeturn4search1

## Security / Privacy / Compliance

- Data touched: none (tooling migration only)
- Secrets: none; ensure installers respect existing secret storage conventions
- Checks: Incorporate detect-secrets and security analyzers within `enaible` smoke runs post-migration

## Observability (Optional)

- Metrics: Track CLI invocation counts and durations via optional structured logs output to `.enaible/logs/`
- Logs/Traces: Standardize Typer logging hooks for debug verbosity levels
- Feature Flags/Experiments: Add `enaible doctor --verbose` flag to capture environment diagnostics

## Test Plan

- Unit: Typer command units, adapter functions, result schema validators via pytest
- Integration/E2E: Render pilots for all three systems, run analyzer commands end-to-end on sample repos
- Performance/Accessibility: Measure CLI cold start (<1s) and template render throughput; ensure generated prompts meet accessibility wording standards
- How to run: `uv run pytest tools/enaible/tests -v`, `uv run enaible prompts render -s all -p all -o ._generated`

### Quality Gates

| Gate        | Command                                                      | Threshold / Expectation |
| ----------- | ------------------------------------------------------------ | ----------------------- |
| Lint        | `uv run ruff check tools/enaible src shared`                 | 0 errors                |
| Type        | `uv run mypy tools/enaible/src shared`                       | 0 errors                |
| Tests       | `uv run pytest tools/enaible/tests shared/tests -v`          | 100% passing            |
| Duplication | `uv run python -m shared.tools.duplication_check`            | ≤ 3%                    |
| Complexity  | `uv run python -m shared.tools.cyclomatic_check --max-cc 10` | Max CC ≤ 10             |

## PR & Review

- PR URL: <to be created>
- PR Number/Status: <pending> • OPEN
- Required Checks: Lint, Type, Tests, CLI Drift • Last CI run: <pending>

## Outcomes & Retrospective (on PR acceptance, add a summary review)

- What went well: <fill in after completion>
- What to change next time: <fill in after completion>
- What behaviours/actions should be codified in AGENTS.md: <fill in after completion>
