# Project: AI-Assisted Workflows

---

## Executive Summary

AI-Assisted Workflows orchestrates multi-runtime AI coding prompts and analyzer automation for Claude Code, OpenCode, and Codex. Shared prompt bodies and migration specs are in place, but the `enaible` CLI that is meant to unify analyzer execution and prompt rendering has not been scaffolded yet, leaving each system to maintain brittle, duplicated adapters.

- **Current Readiness**: Shared prompt sources, system templates, and detailed migration plans exist, giving a clear blueprint for centralizing workflows.
- **Immediate Gaps**: No `tools/enaible/` package yet, and every system prompt still performs manual script-path probing before calling analyzers.

## Features

- Centralized analyzer framework with 22 tools covering security, quality, architecture, performance, and root-cause analysis.
- Shared prompt bodies under `shared/prompts/` keep task content system-agnostic while wrappers live in `systems/*`.
- System-specific command sets for Claude Code, OpenCode, and Codex with installation scripts and rulesets.
- Extensive documentation, exec plans, and fixtures that track the in-flight CLI migration work.

## Tech Stack

- **Languages**: Python 3.11+, TypeScript, Bash, SQL
- **Frameworks**: Analyzer core built on custom BaseAnalyzer/registry; future CLI planned with Typer + Jinja2
- **Build Tools**: `uv` for Python tooling; Bun/Tailwind/React standards documented for front-end prompts
- **Package Managers**: `uv`, `pip`, `bun`
- **Testing**: `pytest`, `pytest-cov`, `ruff`, `mypy`, lizard, jscpd

## Structure

```markdown
ai-assisted-workflows/
├── docs/ # System documentation, specs, and template targets
├── shared/ # Analyzer framework, shared prompts, setup scripts, tests
├── systems/ # Claude Code, OpenCode, and Codex prompt wrappers & installers
├── todos/ # Task backlogs and workflow guidance
├── test_codebase/ # Controlled applications for integration testing
└── workspace/ # Generated artifacts and analysis reports
```

**Key Files**:

- `README.md` - Product overview, quick-start install scripts, and current readiness metrics.
- `shared/prompts/analyze-security.md` - Shared security prompt that still performs path probing slated for replacement.
- `docs/systems/codex/templates/prompt.md` - Codex wrapper template placeholder awaiting adapter-driven rendering.
- `session-notes.md` - Timeline capturing repeated enaible exec-plan generation and migration planning.
- `shared/tests/integration/fixtures/scout/spec.md` - Authoritative migration spec describing the desired CLI surface and repository layout.

**Entry Points**:

- `systems/claude-code/commands/*.md` - Claude slash-command prompts (managed artifacts post-migration).
- `systems/opencode/command/*.md` - OpenCode command definitions mirroring the shared bodies.
- `systems/codex/prompts/*.md` - Codex prompt library expected to become render targets.
- `shared/core/cli/run_analyzer.py` - Existing Python entry point used by prompts while awaiting `enaible`.

## Architecture

The analyzer framework lives under `shared/core`, where `BaseAnalyzer` classes register with a shared registry that powers `core.cli.run_analyzer`. Prompts currently shell out to this module after computing PYTHONPATH manually. Shared prompt bodies in `shared/prompts/` are supposed to render through system templates located in `docs/systems/<system>/templates/`, but no rendering pipeline exists yet—each system ships a hand-maintained copy. The enaible migration plan introduces a Python CLI that will wrap analyzer execution, provide prompt rendering/diffing, and manage installers so that system folders hold only generated artifacts.

### Key Components:

- **Analyzer Registry**: Discovers analyzers and enforces configuration validation before execution.
- **Shared Prompt Bodies**: Provide single-source content for prompts like security or primer tasks.
- **System Templates**: System-level front matter and metadata waiting to be driven by adapters.
- **Migration Specs & Exec Plans**: Documented next steps for enaible CLI, adapters, and CI guardrails.

## Backend Patterns and Practices

- Analyzer modules subclass `BaseAnalyzer` and register themselves through `registry_bootstrap`, enabling consistent CLI invocation.
- Prompts currently handle environment discovery (script paths, PYTHONPATH) manually, a pattern scheduled for removal once `enaible analyzers run` exists.
- Quality gates rely on running analyzers via `python -m core.cli.run_analyzer`, producing JSON for downstream inspection.

## Frontend Patterns and Practices

- System rulesets expect React 18 with shadcn/ui atop Radix primitives, styled via Tailwind tokens when front-end changes are required.
- Prompts describe UX patterns (session history handling, confirmation gates) in Markdown; adapters are expected to inject system-specific notices without duplicating bodies.

## Data & State

- Analyzer runs accept targets, file globs, and severity thresholds; results are normalized to JSON and Markdown summaries.
- Migration spec mandates `.enaible/artifacts/<prompt>/<timestamp>/` as the canonical location for storing outputs once the CLI lands.
- System installers currently place scripts under `.claude/`, `.opencode/`, or `.codex/`; the new CLI will own these destinations via install modes (`merge`, `update`, `fresh`, `sync`).

## Performance & Security

- Sequential analyzer execution means CLI startup latency scales with the number of analyzers invoked; the new CLI must keep wrapper overhead minimal.
- Security prompts enforce OWASP coverage with staged confirmations; replacing manual script discovery with `enaible` reduces the risk of environment misconfiguration.
- Analyzer outputs already capture timestamps and severity counts, forming the basis of the CLI’s normalized JSON schema.

## Observability

| Aspect          | Current State                                                                      | Note                                                |
| --------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------- |
| Logging         | Analyzer framework logs via console and JSON outputs; no centralized collector yet | Future CLI can aggregate into `.enaible/artifacts/` |
| Metrics         | Quality metrics gathered ad hoc from analyzer outputs                              | Opportunity to summarize via `enaible doctor`       |
| Analytics/Flags | PostHog enablement deferred until consent handling is wired                        | Documented in system rules for future rollout       |

## Build & Quality Gates

| Purpose     | Command                                                                                                                  | Notes                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| Lint        | `uv run ruff check shared`                                                                                               | Aligns with repo-wide Python linting standards  |
| Type        | `uv run mypy --config-file mypy.ini shared`                                                                              | Strict typing for analyzer core                 |
| Test        | `PYTHONPATH=shared pytest shared/tests/unit -v`                                                                          | Unit coverage for registry and analyzers        |
| Duplication | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:jscpd --target . --output-format json`             | To be abstracted behind `enaible analyzers run` |
| Complexity  | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:complexity_lizard --target . --output-format json` | Target for CLI command parity                   |

## Testing Practices

| Test type                        | File path                                                    | Command                                                                                  |
| -------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests                       | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests                | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration (all analyzers) | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage                         | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |
| E2E / System (controlled apps)   | `test_codebase/`                                             | `PYTHONPATH=shared pytest shared/tests/integration -k e2e -v`                            |

## Git History Insights (20 days)

- Enaible CLI exec plans iterated repeatedly to lock Typer + Jinja2 decisions and risk mitigations (session-notes.md:105-137).
- Plan-exec and scout fixtures underline analyzer path-probing as the primary blocker for rollout (shared/tests/integration/fixtures/plan-exec/report.md:3-42).

---

## Task Impact Analysis

| File/Area                                             | Rationale                                                                                                          |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `shared/prompts/analyze-security.md:22`               | Shared body still walks the filesystem for analyzer scripts; must defer to `enaible analyzers run` once available. |
| `systems/claude-code/commands/analyze-security.md:19` | Claude wrapper duplicates path-probing logic that will be replaced by generated output from templates.             |
| `systems/opencode/command/analyze-security.md:19`     | OpenCode prompt mirrors the same manual resolution steps, creating drift risk without the CLI.                     |
| `systems/codex/prompts/analyze-security.md:15`        | Codex prompt repeats the adapter logic that the enaible CLI is meant to centralize.                                |
| `shared/tests/integration/fixtures/scout/spec.md:58`  | Migration spec calls for a `tools/enaible/` package that is absent in the current tree.                            |

---

## Risks & Recommendations

| Risk                                       | Mitigation                                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Continued prompt drift while CLI is absent | Prioritize scaffolding `tools/enaible/` with stub commands so templates can begin rendering against real adapters.        |
| Missing shared includes/templates tooling  | Create `shared/prompts/includes/` and system adapters before refactoring prompt bodies to avoid blocking regeneration.    |
| Analyzer invocation changes breaking CI    | Define JSON schema and exit codes up front, then backfill tests around `enaible analyzers run` prior to swapping prompts. |

---

## Open Questions

- Should Codex prompts expose any metadata banner (HTML comment) to track enaible generation, or remain completely frontmatter-free?
- What minimum analytics or health checks should `enaible doctor` report to validate analyzer availability?
- How will legacy installer scripts transition once `enaible install` owns the merge/update/fresh/sync flow?
