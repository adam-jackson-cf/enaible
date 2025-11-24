# ExecPlan: Finish Enaible CLI Unification

- Status: Proposed
- Repo/Branch: `adam-versed/ai-assisted-workflows` • `cli-migration`
- Scope: feature • Priority: P1
- Start: 2025-11-09 • Last Updated: 2025-11-09T14:29Z
- Links: todos/cli-migration/spec.md; todos/cli-migration/execplan.md; shared/tests/integration/fixtures/plan-exec/report.md

## Purpose / Big Picture

Deliver the remaining Enaible CLI capabilities so every managed prompt (Codex, Claude Code, OpenCode, Copilot) calls a single, versioned command surface, analyzer runs emit normalized JSON into `.enaible/`, and system wrappers are rendered from shared templates. Completing this work removes brittle path-probing blocks, halves drift risk between systems, and gives contributors a professional workflow they can install or sync with `uv run enaible install` in one step.

## Success Criteria / Acceptance Tests

- [ ] `uv run --project tools/enaible enaible analyzers run security:detect_secrets --target . --summary --out .enaible/artifacts/dev/detect-secrets.json` produces JSON that validates against the published schema and matches `shared/core/cli/run_analyzer.py` exit semantics.
- [ ] `uv run --project tools/enaible enaible prompts render --prompt analyze-security --system claude-code --out systems/claude-code/commands` re-renders without git diffs, proving adapters + templates reproduce committed assets.
- [ ] `uv run --project tools/enaible enaible install codex --mode merge --scope project --target . --dry-run` lists managed writes/skips without touching unmanaged files, confirming installer safety.
- Non-Goals: Adding new analyzer categories, supporting legacy path-probing, or introducing parallel prompt pipelines outside the Enaible renderer.

## Tech stack

- **Languages**: Python 3.12, Markdown, shell scripting
- **Frameworks**: Typer CLI, Jinja2 templating
- **Build Tools**: uv (sync/run/tool install), pytest harness
- **Package Managers**: uv-managed virtualenv with pip interoperability
- **Testing**: pytest for unit/integration, CLI smoke tests, git-based drift checks

## Constraints

- Use `.enaible/artifacts/<prompt>/<timestamp>/` for every analyzer artifact to honor the 2025-10-13 decision.
- Codex wrappers must remain frontmatter-free (metadata limited to optional HTML comments per spec).
- No dual-mode prompts: legacy path-probing blocks must be deleted once an Enaible command replaces them.
- Follow AGENTS.md guidance: prefer established libs, keep complexity low, remove fallbacks, and keep cyclomatic complexity under 10.

## Development approach

- Align CLI contracts with the existing registry (`shared/core/cli/run_analyzer.py:7`) before modifying prompts so JSON schema + exit codes are stable.
- Treat Jinja2 templates under `docs/system/<system>/templates/*.j2` as the single wrapper source, adding shared includes for repeated fragments.
- Refactor shared prompts (starting with `analyze-security`, `get-primer`) to call `enaible` commands, then regenerate all system variants with `enaible prompts render`.
- Bake drift protection into CI (`.github/workflows/ci-quality-gates-incremental.yml:60`) and document installer behaviors to prevent accidental overwrites.
- Capture evidence (CLI output + rendered files) under `.enaible/artifacts/cli-migration/<timestamp>/` for auditability.

## Context & Orientation

- Code: `shared/core/cli/run_analyzer.py:7` exposes the current analyzer entrypoint; `tools/enaible/src/enaible/commands/analyzers.py:1` and `tools/enaible/src/enaible/models/results.py:1` form the Typer command & JSON schema; `tools/enaible/src/enaible/prompts/catalog.py:31` and `tools/enaible/src/enaible/prompts/renderer.py:1` drive template rendering; `docs/system/claude-code/templates/command.md.j2:1` and `docs/system/codex/templates/prompt.md.j2:1` define wrapper shells; `shared/prompts/analyze-security.md:22` and `shared/prompts/get-codebase-primer.md:1` are the first bodies to refactor; `.github/workflows/ci-quality-gates-incremental.yml:60` hosts CLI gates.
- Data/Contracts: Analyzer payload normalization in `tools/enaible/src/enaible/models/results.py:1`; managed file sentinel `<!-- generated: enaible -->` defined in `tools/enaible/src/enaible/constants.py:1`; installer scopes + directories in `tools/enaible/src/enaible/prompts/adapters.py:1`.
- Constraints/Assumptions: Global behavior rules from AGENTS.md require no fallbacks and strict quality gates; installers must preserve unmanaged files while supporting `fresh|merge|update|sync` modes per todos/cli-migration/spec.md.

## High level Phase Plan

- Phase 1: CLI contract hardening — finalize analyzer schema, artifact layout, and documentation so prompts can rely on stable commands.
- Phase 2: Template & adapter audit — ensure every system wrapper lives under `docs/system/<system>/templates`, add shared includes, and verify catalog metadata.
- Phase 3: Prompt migration pilots — refactor `analyze-security` and `get-primer`, regenerate Codex/Claude/OpenCode/Copilot outputs, and validate drift.
- Phase 4: Installer & CI guardrails — expand CLI (`prompts sync`, install dry-runs), enforce drift + analyzer smoke tests in CI, and document rollout guidance.

## Detailed Phase Task Steps

Status key: `@` = in progress, `X` = complete, blank = outstanding. Task types: Code, Read, Action, Test, Gate, Human.

| Status | Phase # | Task # | Task Type | Description                                                                                                                                                                                                                                                                  |
| ------ | ------- | ------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|        | 1       | 1      | Read      | Re-read todos/cli-migration/spec.md:1 and shared/tests/integration/fixtures/plan-exec/report.md:1 to enumerate objectives, constraints, and blockers before changing code.                                                                                                   |
|        | 1       | 2      | Read      | Review `shared/core/cli/run_analyzer.py:7` plus `tools/enaible/src/enaible/commands/analyzers.py:1` to map required flags, exit codes, and registry wiring.                                                                                                                  |
|        | 1       | 3      | Code      | Codify the analyzer JSON schema inside `tools/enaible/src/enaible/models/results.py:1` and publish it to `.enaible/schema.json`, ensuring timestamps, severity, and stats fields are documented.                                                                             |
|        | 1       | 4      | Code      | Enhance `tools/enaible/src/enaible/commands/analyzers.py:40` to always route artifacts into `.enaible/artifacts/<tool>/<timestamp>/` (create directories, honor `--out`, support `--no-external`).                                                                           |
|        | 1       | 5      | Test      | Run `uv run --project tools/enaible enaible analyzers run quality:lizard --target test_codebase --summary --out .enaible/artifacts/cli-migration/lizard.json` and capture output under `.enaible/artifacts/cli-migration/<ts>/`.                                             |
|        | 2       | 6      | Read      | Inspect `docs/system/claude-code/templates/command.md.j2:1` and `docs/system/codex/templates/prompt.md.j2:1` to confirm frontmatter + managed sentinel placement.                                                                                                            |
|        | 2       | 7      | Code      | Create shared includes (`shared/prompts/includes/session-history.j2:1`, `shared/prompts/includes/stop-confirmations.j2:1`) and update `tools/enaible/src/enaible/prompts/renderer.py:1` to load them for every prompt.                                                       |
|        | 2       | 8      | Code      | Extend `tools/enaible/src/enaible/prompts/catalog.py:31` so each prompt definition records system metadata (frontmatter hints, Codex comment tags) and add any missing systems.                                                                                              |
|        | 2       | 9      | Test      | Execute `uv run --project tools/enaible enaible prompts render --prompt analyze-security --system codex --out systems/codex/prompts` and verify diffs stay zero.                                                                                                             |
|        | 3       | 10     | Code      | Replace legacy path-probing paragraphs in `shared/prompts/analyze-security.md:22` with direct `uv run --project tools/enaible enaible analyzers run …` blocks and regenerate all system wrappers.                                                                            |
|        | 3       | 11     | Code      | Update `shared/prompts/get-codebase-primer.md:1` to reference Enaible context capture commands (git history steps, STOP handling) and ensure template variables follow @TOKEN rules.                                                                                         |
|        | 3       | 12     | Action    | Render pilots end-to-end: `uv run --project tools/enaible enaible prompts render --prompt analyze-security,get-codebase-primer --system claude-code,codex,copilot -o systems` then commit regenerated files with `<!-- generated: enaible -->`.                              |
|        | 4       | 13     | Code      | Implement `enaible prompts sync` inside `tools/enaible/src/enaible/commands/prompts.py:1` to combine render+write+diff for CI/local workflows.                                                                                                                               |
|        | 4       | 14     | Code      | Harden installer logic in `tools/enaible/src/enaible/commands/install.py:1` (dry-run summaries, backups, unmanaged preservation) and document usage in README.md:84.                                                                                                         |
|        | 4       | 15     | Gate      | Update `.github/workflows/ci-quality-gates-incremental.yml:60` to run `uv run --project tools/enaible enaible prompts diff --prompt all --system all` and a dry-run `enaible install codex --dry-run` before greenlighting merges.                                           |
|        | 4       | 16     | Gate      | Run quality gates: `uv run --project tools/enaible ruff check tools/enaible/src shared`, `uv run --project tools/enaible mypy tools/enaible/src`, `uv run --project tools/enaible pytest tools/enaible/tests -v`, and `uv run --project tools/enaible enaible prompts diff`. |

## Progress Per Session (Running Summary Log)

- (2025-11-09T14:29Z) Drafted ExecPlan from spec + report artifacts; implementation not yet started.

## Surprises & Discoveries

- None yet — begin recording once code execution surfaces unexpected behaviors.

## Decision Log

- Decision: `.enaible/` is the canonical artifact root for analyzer + prompt runs.
  Rationale: Aligns with the 2025-10-13 migration decision and keeps outputs system-agnostic.
  Date/Author: 2025-10-13 • CLI migration working group
- Decision: Codex prompt renders remain frontmatter-free, using only optional HTML comments.
  Rationale: Matches Codex conventions and avoids breaking existing Codex CLI parsing.
  Date/Author: 2025-10-13 • CLI migration working group
- Decision: Enaible installers support `fresh|merge|update|sync` with backups enabled by default.
  Rationale: Prevents accidental overwrites while still allowing a one-command rollout path.
  Date/Author: 2025-10-13 • CLI migration working group

## Risks & Mitigations

- Risk: Analyzer schema drift breaks downstream automation • Mitigation: check new schema into `.enaible/schema.json`, add pytest contract tests for `AnalyzerRunResponse`, and document required fields before release.
- Risk: Prompt regeneration could overwrite unmanaged customizations • Mitigation: ensure `tools/enaible/src/enaible/commands/install.py:1` respects the managed sentinel and default to MERGE mode with backups.
- Risk: `uv run enaible` performance regressions discourage adoption • Mitigation: profile CLI startup, cache template environments, and document tmux guidance for long-running renders.

## Dependencies

- Analyzer maintainers (shared/core) to approve JSON schema changes and ensure registry compatibility.
- Docs/UI owners to review updates under `docs/system/<system>/templates` and README instructions.
- CI maintainers to accept workflow updates in `.github/workflows/ci-quality-gates-incremental.yml` and provision uv on runners.

## Security / Privacy / Compliance

- Data touched: internal repo metadata only; no PII processed.
- Secrets: installer must never copy `.env` or credential files; detect-secrets remains part of analyzer suite.
- Checks: run `uv run --project tools/enaible enaible analyzers run security:detect_secrets --target .` before releasing CLI binaries.

## Observability (Optional)

- Metrics: record analyzer durations + exit codes in the normalized JSON payload; optionally aggregate counts in `.enaible/logs/enaible-cli.log`.
- Logs/Traces: add `--verbose` flag handling in `enaible analyzers run` to emit structured debug lines.
- Feature Flags/Experiments: gate future opt-in features behind env vars (`ENAIBLE_EXPERIMENTAL_INSTALL=1`).

## Test Plan

- Unit: pytest modules under `tools/enaible/tests` covering analyzers command, prompts renderer, installers, and schema serialization.
- Integration/E2E: run `/analyze-security` and `/get-primer` prompts end-to-end via `uv run --project tools/enaible enaible prompts render` + `enaible install` dry-run, verifying artifacts under `.enaible/artifacts/`.
- Performance/Accessibility: measure CLI cold start (<1s) and prompt render throughput; ensure generated prompts preserve shadcn/Radix guidance from `systems/claude-code/rules/global.claude.rules.md:12`.
- How to run: `uv run --project tools/enaible pytest tools/enaible/tests -v`, `uv run --project tools/enaible enaible prompts diff`, `uv run --project tools/enaible enaible analyzers run quality:lizard --target test_codebase`.

### Quality Gates

| Gate      | Command                                                                                       | Threshold / Expectation |
| --------- | --------------------------------------------------------------------------------------------- | ----------------------- |
| Lint      | `uv run --project tools/enaible ruff check tools/enaible/src shared`                          | 0 errors                |
| Type      | `uv run --project tools/enaible mypy tools/enaible/src shared`                                | 0 errors                |
| Tests     | `uv run --project tools/enaible pytest tools/enaible/tests shared/tests -v`                   | 100% passing            |
| Prompts   | `uv run --project tools/enaible enaible prompts diff --prompt all --system all`               | No drift                |
| Installer | `uv run --project tools/enaible enaible install codex --mode merge --scope project --dry-run` | No unmanaged overwrites |

## Idempotence & Recovery

- Enaible commands are side-effect free when run with `--dry-run` or `--out`; rerun renders/tests as needed and overwrite artifacts under `.enaible/artifacts/cli-migration/<timestamp>/`.
- Installer backups (`*.bak`) created in merge/update modes enable quick rollback—restore the backup file or re-run install with `--fresh` after cleaning the target directory.
- CI drift checks fail fast; rerun `enaible prompts render` locally, review diffs, and recommit to recover.

## Artifacts & Notes

- Store analyzer runs, prompt render logs, and CI transcripts under `.enaible/artifacts/cli-migration/<timestamp>/`.
- Capture git diffs for `systems/*` outputs plus schema documentation excerpts inside the same artifact folder for reviewers.
- Record installer dry-run summaries (stdout) to `.enaible/artifacts/cli-migration/install-summary.txt` for provenance.

## PR & Review

- PR URL: <to be assigned>
- PR Number/Status: <pending> • OPEN
- Required Checks: Lint, Type, Tests, Prompts Diff, Installer Dry-Run • Last CI run: <pending>

## Outcomes & Retrospective (populate after merge)

- What went well: <tbd>
- What to change next time: <tbd>
- What behaviours/actions should be codified in AGENTS.md: <tbd>
