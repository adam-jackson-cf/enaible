<!-- ran on codex medium took 10 mins -->

# Project: AI-Assisted Workflows

---

## Executive Summary

AI-Assisted Workflows unifies automation for Codex, Claude Code, and OpenCode by pairing Markdown command specs with a shared Python analyzer framework and multi-agent orchestration, enabling repeatable build and analysis flows.

- **Current Readiness**: Codex prompts and shared analyzers are production-ready, but Claude Code lacks the todo-build orchestration that anchors full-plan execution.
- **Immediate Gaps**: Replicating todo-build for Claude requires aligning command syntax, subagent wiring, and quality gates with the Codex source while validating installer expectations.

## Features

- Multi-runtime CLI command suites with cross-platform installers (`systems/codex`, `systems/claude-code`, `systems/opencode`).
- Shared BaseAnalyzer framework with 20+ analyzers covering quality, security, architecture, performance, and root-cause analysis (`shared/analyzers`).
- ExecPlan and todo orchestration prompts that drive worktree-based implementation loops (`systems/codex/prompts/todo-build.md`).
- Specialized Claude subagents for research, implementation, and escalation (`systems/claude-code/agents`).
- Context capture and monitoring automation spanning session logs, unified `./dev.log`, and task documentation (`shared/context`, `docs/monitoring.md`).

## Tech Stack

- **Languages**: Python 3.11, TypeScript/JavaScript, Bash (`README.md`, `shared/core/base/analyzer_base.py`).
- **Frameworks**: Custom BaseAnalyzer/AnalyzerRegistry runtime, Markdown command specs, Claude subagent protocols (`shared/core/base/analyzer_registry.py`, `docs/subagents.md`).
- **Build Tools**: `uv`-driven Python workflows, Bash installers, Node-based analyzers (jscpd), Bun-first front-end scaffolds per global rules (`systems/codex/install.sh`, `systems/claude-code/install.sh`, `systems/claude-code/rules/global.claude.rules.md`).
- **Package Managers**: `uv`/`pip` for Python, `npm`/`bun` for analyzer and front-end tooling (`requirements-dev.txt`, `systems/claude-code/install.sh`).
- **Testing**: `pytest`, `pytest-cov`, `ruff`, `mypy`, `xenon`, `detect-secrets`, JSCPD analyzer smoke tests (`requirements-dev.txt`, `shared/tests`).

## Structure

```markdown
project-root/
├── systems/claude-code/ # Claude Code command specs, agents, installers
├── systems/codex/ # Codex prompt library, installers, exec plan tooling
├── shared/ # Analyzer framework, utilities, tests, setup scripts
├── docs/ # Process, monitoring, and subagent documentation
├── todos/ # Workflow artifacts and planning documents
└── test_codebase/ # Validation applications for analyzer regression
```

**Key Files**:

- `systems/codex/prompts/todo-build.md:1` - Canonical todo-build workflow defining INIT→PREPARE→EXECUTE loops for replication.
- `docs/subagents.md:1` - Subagent orchestration spec describing todo-build expectations across platforms.
- `systems/claude-code/commands/create-project.md:1` - Reference Claude command layout and front matter conventions.
- `shared/core/cli/run_analyzer.py:1` - Registry-driven analyzer entrypoint invoked by command workflows.
- `requirements-dev.txt:1` - Authoritative list of dev quality gates (pytest, ruff, mypy, detect-secrets, xenon, radon).

**Entry Points**:

- `systems/claude-code/install.sh:1` - Installs Claude command suite, analyzer scripts, and Node tooling (eslint+jscpd).
- `systems/codex/install.sh:1` - Mirrors installer logic for Codex; useful for parity checks when porting commands.
- `shared/core/cli/run_analyzer.py:1` - Python CLI executed by analyzer-focused commands and gates.
- `systems/claude-code/statusline-worktree` - Compiled helper packaged with Claude install; ensure new command interactions respect existing status hooks.

## Architecture

Claude/Codex/OpenCode share a layered architecture: Markdown commands (or prompts) define workflows, installers provision analyzers and Node tooling, and the Python BaseAnalyzer framework executes registry-registered analyzers via `run_analyzer.py`. Subagent definitions in `systems/claude-code/agents` coordinate complex tasks, while docs such as `docs/subagents.md` codify orchestration sequences and quality expectations.

### Key Components:

- **Prompt & Command Libraries**: `systems/codex/prompts`, `systems/claude-code/commands` encapsulate workflow definitions, variables, and step-by-step behavior contracts.
- **Shared Analyzer Runtime**: `shared/core/base` provides `BaseAnalyzer`, `AnalyzerConfig`, and registry bootstrap to expose quality, security, and performance analyzers.
- **Specialist Subagents**: `systems/claude-code/agents` define reusable experts (research, infrastructure, UX) for delegated tasks inside todo-build loops.

## Backend Patterns and Practices

- Analyzer classes register via `@register_analyzer` into `AnalyzerRegistry`, enabling decoupled CLI invocation (`shared/core/base/analyzer_registry.py`).
- Commands rely on environment resolution patterns (`SCRIPTS_ROOT`, `.claude/scripts`) before invoking analyzers, ensuring consistent script discovery (`systems/claude-code/commands/analyze-architecture.md`).
- Analyzer configs constrain file scanning, batching, and thresholds (e.g., `LizardComplexityAnalyzer` sets language extensions and limits, `shared/analyzers/quality/complexity_lizard.py`).
- Dev dependencies enforce lint/type/test gates across Python and Node ecosystems (`requirements-dev.txt`).
- Installers idempotently provision Node tools such as eslint and jscpd for duplication detection (`systems/claude-code/install.sh`).

## Frontend Patterns and Practices

- Global Claude rules prescribe Bun + React 18 + shadcn/ui layered on Radix primitives with Tailwind tokens locked as design contracts (`systems/claude-code/rules/global.claude.rules.md`).
- State guidance favors Zustand for client stores and TanStack Query for async data, with SQLite + Drizzle for persistence in prototypes.
- Production guidance mandates Ultracite linting, strict TypeScript (`bunx tsc --noEmit`), and PostHog initialization post-consent.
- UX work should leverage documented subagents (`docs/subagents.md`) and avoid bespoke styling—stick to Shadcn components.

## Data & State

- Context capture modules (`shared/context/context_bundle_capture_claude.py`) parse Claude session JSONL history, redact sensitive data, and emit structured bundles.
- ExecPlan/todo workflows persist progress in markdown plans under `todos/` and `.workspace/` directories, ensuring plan-as-source-of-truth semantics.
- Analyzer results funnel through `ResultFormatter` for JSON/console outputs, standardizing severity filtering and summary modes (`shared/core/utils/output_formatter.py`).
- Session and monitoring docs emphasize unified log ingestion into `./dev.log`, easing state introspection (`docs/monitoring.md`).

## Performance & Security

- Complexity thresholds and batch sizes enforced via Lizard analyzer keep cyclomatic complexity under control; testing environments fail fast if tooling missing (`shared/analyzers/quality/complexity_lizard.py`).
- JSCPD analyzer shells out via npx/local binaries with explicit error messaging when Node tooling is absent, aligning with installer setup (`shared/analyzers/quality/jscpd_analyzer.py`).
- Security suite combines detect-secrets and Semgrep analyzers (registered in `shared/core/base/registry_bootstrap.py`), with docs discouraging fallback logic.
- Quality gates rely on detect-secrets and `uv run` workflows per dev requirements, reinforcing secret hygiene and type safety (`requirements-dev.txt`).

## Observability

| Aspect          | Current State                                                                                                                | Note                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Logging         | Unified `./dev.log` via `/setup-dev-monitoring`; Makefile/Procfile generation streams service output (`docs/monitoring.md`). | Verify Claude commands append or reference this log when adding todo-build telemetry. |
| Metrics         | Planned via monitoring workflow; no dedicated metrics collectors committed yet.                                              | Consider extending todo-build to emit phase timings into monitoring scripts.          |
| Analytics/Flags | PostHog initialization stubbed post-consent per global rules; not enabled by default.                                        | Ensure any new Claude command defers analytics until consent is persisted.            |

## Build & Quality Gates

| Purpose     | Command                                                                                                       | Notes                                                                                              |
| ----------- | ------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Lint        | `uv run ruff check shared`                                                                                    | Python lint + performance heuristics from `requirements-dev.txt` (extend to other dirs as needed). |
| Type        | `uv run mypy --config-file mypy.ini`                                                                          | Targets `shared/core/base`, `shared/core/config`, key utils per `mypy.ini`.                        |
| Test        | `PYTHONPATH=shared pytest shared/tests -v`                                                                    | Runs unit + integration suites; respect markers for slow/external tests.                           |
| Duplication | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:jscpd --target . --output-format json`  | Wraps JSCPD; requires Node tooling from installers.                                                |
| Complexity  | `PYTHONPATH=shared python -m core.cli.run_analyzer --analyzer quality:lizard --target . --output-format json` | Enforces cyclomatic thresholds defined in analyzer config.                                         |

## Testing Practices

| Test type                        | File path                                                    | Command                                                                                  |
| -------------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests                       | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests                | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration (all analyzers) | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage                         | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |
| E2E / System (controlled apps)   | `test_codebase/`                                             | `PYTHONPATH=shared pytest shared/tests/integration -k e2e -v`                            |

## Git History Insights (20 days)

- Codex build orchestration advanced via shared prompts and new workflows (`fd9d977`, `98ca489`, `2eb8b39`), providing the blueprint that Claude must mirror for todo-build.
- Prompt/docs refinements and scout tooling adjustments (`3ae05e5`, `4eff9ac`, `f42a22b`, `a9afca7`) highlight active parity work and GitHub Actions fixes that Claude replication must respect.

---

## Task Impact Analysis

| File/Area                                              | Rationale                                                                                                     |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `systems/codex/prompts/todo-build.md:1`                | Source-of-truth workflow to adapt for Claude command semantics and variable handling.                         |
| `systems/claude-code/commands/create-project.md:1`     | Demonstrates required front matter, usage examples, and behavioral structuring for Claude slash commands.     |
| `docs/subagents.md:1`                                  | Documents the todo-build orchestration phases and subagent assignments that Claude command must invoke.       |
| `systems/claude-code/agents/research-coordinator.md:1` | Shows agent capabilities and tooling access; reuse ensures delegated tasks align with existing orchestrators. |
| `shared/tests/integration/test_codex_plan_exec.py:1`   | Existing integration coverage for Codex todo workflows—use as template for Claude parity tests.               |

---

## Risks & Recommendations

| Risk                                                                                               | Mitigation                                                                                                                        |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Divergence between Codex and Claude build workflows could introduce inconsistent gate enforcement. | Mirror todo-build instructions line-by-line, and create shared snippets or include files to minimize drift.                       |
| Claude environments may lack Node/jscpd tooling required by duplication gates.                     | Ensure installer hooks run (or document prerequisites) before enabling the command; add pre-flight checks akin to Codex workflow. |
| Binary helpers like `statusline-worktree` could be impacted by new automation loops.               | Validate command interactions in a worktree session and document any required statusline updates.                                 |

---

## Open Questions

- Should the Claude todo-build command reuse Codex’s plan file mutation semantics verbatim, or adapt to Claude’s existing plan-manager agent expectations?
- Do we need additional Claude-specific integration tests (e.g., worktree lifecycle) beyond mirroring `test_codex_plan_exec.py`, or can we extend shared fixtures to cover both CLI surfaces?
