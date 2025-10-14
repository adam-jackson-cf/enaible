<!-- ran on gpt 5 high took 16 mins -->

# Project: AI-Assisted Workflows

---

## Executive Summary

AI-Assisted Workflows provides coordinated automation across Claude Code, Codex, and OpenCode CLIs, combining scripted prompts, multi-agent orchestration, and shared Python analyzers to enforce quality gates and ship features from structured plans.

- **Current Readiness**: Codex already ships `/todo-build` v0.2 with end-to-end plan execution, rich orchestration docs, and regression tests that can be ported to Claude Code with minimal prompt translation once adapters are aligned.
- **Immediate Gaps**: Claude Code lacks an active `/todo-build` command and several subagent files are empty or deprecated, so orchestration logic, permissions, and integration tests must be reinstated before parity is real.

## Features

- Plan-driven build orchestration with multi-agent task state machines
- Shared analyzer registry (security, architecture, quality, performance, root-cause) consumable from all CLIs
- Installation scripts and uninstallers that manage commands, agents, and MCP configuration per platform
- Context capture utilities and monitoring setup for unified dev logging and history replay
- Extensive documentation covering prompts, subagents, templates, and operating rules per system

## Tech Stack

- **Languages**: Python 3.11+, TypeScript/JavaScript, Bash, SQL
- **Frameworks**: Claude Code / Codex / OpenCode CLIs with subagent orchestration, BaseAnalyzer infrastructure, plan-exec and todo workflows
- **Build Tools**: `uv`, Bun scripts, Typer/Click-based analyzers, shell installers, Git worktrees
- **Package Managers**: `uv`, Bun, pip (via installers), npm (for analyzer tooling)
- **Testing**: pytest suites (unit/integration), CLI fixtures, analyzer smoke tests, pre-commit pipelines

## Structure

```markdown
project-root/
├── systems/ # CLI-specific assets (commands, agents, rules, installers)
├── shared/ # Analyzer framework, context capture, shared prompts/tests
├── docs/ # Workflow documentation, templates, monitoring guides
├── todos/ # Legacy todo-build specs, deprecated agent prompts
├── test_codebase/ # Sample apps for analyzer validation
└── workspace/ # Generated artifacts (reports, background tasks)
```

**Key Files**:

- `systems/codex/prompts/todo-build.md` - Source prompt implementing plan-driven build orchestration for Codex.
- `docs/subagents.md` - Defines multi-agent roles, state machine expectations, and todo workflow behavior.
- `systems/claude-code/rules/global.claude.rules.md` - Coding rules controlling toolchains and design standards for Claude sessions.
- `shared/core/cli/run_analyzer.py` - Registry-backed CLI entry point leveraged by prompts and analyzers.
- `shared/tests/integration/test_codex_scout_codebase.py` - Fixture ensuring Codex todo-scout pipeline produces reports (mirrors desired Claude coverage).

**Entry Points**:

- `systems/claude-code/commands/` - Slash command definitions executed inside Claude Code sessions.
- `systems/claude-code/agents/` - Subagent configuration files (some currently blank) invoked during workflows.
- `shared/core/base/registry_bootstrap.py` - Imports all analyzers to populate the registry before execution.
- `shared/tests/integration/fixtures/run-todo-scout-codebase.sh` - Example CLI harness for running managed prompts end-to-end.

## Architecture

Prompts in `systems/*/commands` or `systems/*/prompts` define workflow scripts that delegate work to subagents and shared analyzers. Codex’s `/todo-build` prompt drives a six-phase loop (INIT → PREPARE → EXECUTE_LOOP → GATES_LOOP → PR_OPEN → REVIEW_LOOP → FINALIZE) that depends on the shared analyzer registry, Git worktrees, and plan-state files. Claude Code currently exposes the analyzer suite and orchestration docs but lacks the active command wrapper. Conan-level documentation (e.g., `docs/subagents.md`, `todos/todo-build/deprecated/*.md`) describes role responsibilities, state transitions, and `TodoWrite`-based tracking that must be rehydrated when cloning the Codex behavior.

### Key Components:

- **Codex `/todo-build` prompt**: Complete specification for plan execution, git worktree control, and gate enforcement.
- **Claude Code command and template system**: Slash command templates, allowed-tools frontmatter, and platform rules that shape the replication target.
- **BaseAnalyzer/AnalyzerRegistry**: Python infrastructure invoked from prompts for linting, coverage, duplication, and architectural metrics.
- **Integration test harness**: Shell fixtures and pytest suites that validate prompt outputs (`test_codex_scout_codebase.py`, `test_codex_plan_exec.py`, `test_todo_background_script.py`).

## Backend Patterns and Practices

- Analyzer execution always resolves script roots in `.claude/scripts/analyzers` → `$HOME/.claude/scripts` fallbacks before invoking `python -m core.cli.run_analyzer`.
- Base analyzers return standardized finding dictionaries (`title`, `description`, `severity`, `file_path`, `line_number`, `recommendation`, `metadata`) enforced by validation utilities.
- Installation scripts favor idempotent operations, explicit logging, and differentiate between newly installed versus pre-existing dependencies.
- Workflows rely on Git worktrees, atomic commits, and ExecPlan/todo files as single sources of truth.
- MCP integrations (Serena LSP, chrome-devtools) are configured in `config.toml` to keep prompts portable.

## Frontend Patterns and Practices

- Design standards lock in shadcn/ui + Radix primitives with Tailwind tokens; no fallback styles or bespoke class names.
- React 18 + React Router 6.23 scaffolds are expected, with state handled via Zustand and async via TanStack Query.
- Bun is the runtime for local-first prototypes and production builds; Ultracite handles lint/format, `tsc --noEmit` enforces types.
- UI prompts encourage PostHog instrumentation only after consent is stored; analytic stubs exist in default scaffolds.

## Data & State

- Todo orchestration tracks task states (`pending`, `validated`, `in_progress`, `testing`, `quality_review`, etc.) via Plan Manager instructions and TodoWrite symbols.
- Plan execution persists artifacts under `.workspace/<slug>/` including specs, inspect reports, and ExecPlan docs.
- Context capture scripts read CLI session logs (`~/.claude`, `~/.codex`) with configurable redaction and semantic filtering.
- Analyzer outputs conform to `AnalysisResult` schemas with JSON serialization plus summary metadata for aggregation.

## Performance & Security

- Performance analyzers include `profile_code`, `performance_baseline`, and `analyze_frontend` with optional Semgrep heuristics.
- Security coverage is provided via `detect_secrets` and Semgrep rules; installers ensure dependencies are available or warn when deferred.
- Quality monitor subagent enforces dynamic gate detection, respecting `--prototype` shortcuts while maintaining lint/build parity.
- Installers preserve dependency provenance and prompt users before removing pre-existing packages during uninstall.

## Observability

| Aspect          | Current State                                                                           | Note                                                               |
| --------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Logging         | Unified `./dev.log` via `/setup-dev-monitoring` Makefile/Procfile scaffolding           | Captures Claude, OpenCode, Codex services with timestamped entries |
| Metrics         | Analyzer reports summarize severity counts; time-in-state tracked in state machine docs | Consider extending `enaible` CLI plan to surface aggregate KPIs    |
| Analytics/Flags | PostHog stubs in TypeScript rules, feature flags deferred until consent                 | Instrumentation re-enabled post-consent per global rules           |

## Build & Quality Gates

| Purpose     | Command                                                                                                       | Notes                                                             |
| ----------- | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Lint        | `bunx ultracite check src`                                                                                    | Enforced by platform rules for TypeScript/React projects          |
| Type        | `bunx tsc --noEmit`                                                                                           | Strict mode, blocks merges in CI                                  |
| Test        | `PYTHONPATH=shared pytest shared/tests/unit -v`                                                               | Python analyzer unit coverage; extend with CLI fixtures as needed |
| Duplication | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:jscpd --target . --output-format json`  | Wraps JSCpd via registry                                          |
| Complexity  | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:lizard --target . --output-format json` | Lizard thresholds across languages                                |

## Testing Practices

| Test type                        | File path                                                    | Command                                                                                  |
| -------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests                       | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests                | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration (all analyzers) | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage                         | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |
| E2E / System (controlled apps)   | `test_codebase/`                                             | `PYTHONPATH=shared pytest shared/tests/integration -k e2e -v`                            |

## Git History Insights (20 days)

- Codex build orchestration • Commits `98ca489`, `2eb8b39`, `fd9d977` introduced `/todo-orchestrate`, `/create-execplan`, and refined `/todo-build`, establishing the blueprint for Claude parity.
- Prompt consolidation • `4eff9ac`, `d30c2a1`, `16fdf74` migrated prompts into shared directories and removed deprecated configs, easing cross-system rendering.
- Analyzer & monitoring calibration • `1a429f5`, `d6d7625`, `0226a6e` standardized log paths, refreshed analyzer schemas, and tightened detect-secrets enforcement.
- Doc/CLI roadmap updates • `133489c`, `0a6294d` documented the upcoming `enaible` CLI and aligned installer assets, signalling future prompt rendering automation.
- Recent work-in-progress • `systems/claude-code/commands/todo-scout-codebase.md` is untracked locally, indicating Claude parity efforts have begun but are not yet committed.

---

## Task Impact Analysis

| File/Area                                            | Rationale                                                                                                                     |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `systems/codex/prompts/todo-build.md:1`              | Canonical workflow to port; use as source template for Claude command body and step logic.                                    |
| `systems/claude-code/commands/`                      | Target directory for new `/todo-build` slash command; requires frontmatter and tool permissions per Claude rules.             |
| `docs/subagents.md:70`                               | Documents required subagents (plan-manager, quality-monitor, git-manager) and their expected behaviors.                       |
| `todos/todo-build/deprecated/todo-build.md:1`        | Contains legacy Claude-specific orchestration, including STOP checkpoints and TodoWrite integration cues worth re-evaluating. |
| `shared/tests/integration/test_codex_plan_exec.py:1` | Provides fixture pattern to replicate for Claude regression tests once command parity is implemented.                         |

---

## Risks & Recommendations

| Risk                                                                                                                   | Mitigation                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Divergence between Codex prompt and Claude command body leads to drift                                                 | Create a shared source (e.g., via upcoming `enaible`) or script to render Claude/Codex variants from the same template.    |
| Empty/legacy subagent files (`systems/claude-code/agents/codebase-inspector.md`) prevent orchestration from delegating | Restore or regenerate required subagent prompts before enabling the command; validate tool permissions match latest rules. |
| Lack of Claude-specific integration tests for todo workflows                                                           | Port Codex fixtures to Claude CLI (similar to `run-todo-scout-codebase.sh`) to ensure parity before release.               |

---

## Open Questions

- Should the resurrected `/todo-build` for Claude reuse TodoWrite-based plan tracking or adopt ExecPlan-only state (matching Codex v0.2)?
- Will the forthcoming `enaible` CLI generate Claude prompts automatically, or do we need a stopgap rendering approach now?
- Which subagent permission set should guard Git operations (current rules demand explicit `Bash(git *)` allowances)?
