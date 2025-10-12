# Project: AI-Assisted Workflows

A comprehensive development automation system that combines Claude Code CLI workflows, Python analysis tools, and an 8-agent orchestration system for intelligent code quality management.

## Tech Stack

- Languages: Python 3.11+, TypeScript/JavaScript, Bash/Shell, SQL
- Security Tools: Semgrep (deferred), Detect-secrets
- Quality Analysis: Lizard, Ruff, JSCPD, Pattern Classifier
- Testing: pytest, pytest-cov, Karma, Jasmine, Custom evaluation frameworks
- Development Tools: Biome, Ruff, Black, Rich CLI, Click
- CI/CD: GitHub Actions, Cross-platform workflows

## Project Structure

ai-assisted-workflows/
├── claude-code/ # Claude Code CLI workflows and configurations
│ ├── commands/ # 24 slash commands for development workflows
│ ├── agents/ # 23 specialized agents (orchestration, specialists, research/UX, handlers)
│ ├── rules/ # Technology-specific coding standards and best practices
│ ├── templates/ # PRD, subagent, and todo templates
│ ├── docs/ # CLI documentation and integration guides
│ └── install.sh/.ps1 # Cross-platform installation scripts
├── opencode/ # OpenCode CLI workflows and configurations
│ ├── command/ # 22 commands for development workflows
│ ├── agent/ # 21 specialized agents (parity with Claude where possible)
│ ├── docs/ # CLI documentation and integration guides
│ ├── rules/ # Technology-specific coding standards and best practices
│ ├── plugin/ # Editor plugin hooks and integrations
│ └── install.sh/.ps1 # Cross-platform installation scripts
├── shared/ # Core Python analysis infrastructure
│ ├── core/base/ # BaseAnalyzer and BaseProfiler frameworks
│ ├── analyzers/ # 22 analysis tools across 5 categories
│ │ ├── security/ # Vulnerability scanning and secrets detection
│ │ ├── quality/ # Code complexity, duplication, and pattern analysis
│ │ ├── architecture/ # Dependency analysis and scalability checks
│ │ ├── performance/ # Profiling, bottleneck detection, and optimization
│ │ └── root_cause/ # Error pattern analysis and trace execution
│ ├── config/ # Configuration templates and CI workflows
│ ├── setup/ # Installation scripts and dependency management
│ └── tests/ # Comprehensive test suite with E2E integration tests
│ └── integration/ # Security analyzer evaluation and E2E CI testing
├── test_codebase/ # Controlled test applications for validation
│ ├── vulnerable-apps/ # 9 vulnerable applications with known security issues
│ ├── clean-apps/ # 5 clean applications for false positive testing
│ └── juice-shop-monorepo/ # Complex real-world application for comprehensive testing
├── docs/ # Comprehensive project documentation
│ ├── installation.md # Installation and setup guide
│ ├── agents.md # Agent orchestration system documentation
│ ├── analysis-scripts.md # Language support and analysis capabilities
│ ├── monitoring.md # Runtime monitoring and logs guidance
│ └── roadmap.md # Progress tracking and upcoming work
└── todos/ # Task management and workflow documentation

### Entry Points

- claude-code/commands/ - Claude Code slash commands
- opencode/command/ - OpenCode slash commands
- shared/analyzers/ - Direct Python analysis tool execution
- shared/tests/integration/ - Comprehensive testing and evaluation frameworks

## Architecture

The system uses a hybrid AI-automation approach combining traditional static analysis with modern ML techniques:

### Core Components

- BaseAnalyzer Framework: Provides shared infrastructure for all 22 analysis tools with strict validation
- 8-Agent Orchestration: State-machine workflow management with quality gates and CTO escalation
- Expert Agent Routing: Language and complexity-based delegation to specialized agents

### Data Flow

User Input → Claude Commands → Agent Orchestration → Analysis Tools → Results

### Key Integrations

- Serena MCP: Enhanced codebase search via Language Server Protocol
- GitHub Actions: Automated CI/CD with quality gate enforcement
- Multi-Language LSP: Symbol extraction across 10+ programming languages

## Dependencies

**Dependencies:**

- `requirements-dev.txt` - Minimal CI/testing dependencies (pytest, ruff, mypy)
- `shared/setup/requirements.txt` - Slim base (lizard, ruff, sqlglot, detect-secrets, infra)

**CI workflow** (`.github/workflows/ci-quality-gates.yml`) - Manually maintained quality gates using dev dependencies for fast execution.

## Script Location Pattern

**Commands use a standardized script discovery pattern:**

Covers command files added under `claude-code/commands/` and `opencode/command/` that invoke scripts located in `shared/` during local development and in their installed locations at runtime.

1. Project-level: `.claude/scripts/analyzers/` and `.opencode/scripts/analyzers/`
2. User-level: `$HOME/.claude/scripts/analyzers/` and `$HOME/.config/opencode/scripts/analyzers/`
3. Interactive fallback: Prompt user for a custom path if neither found

Execution: `PYTHONPATH="$SCRIPTS_ROOT" python -m core.cli.run_analyzer --analyzer category:tool --target . --output-format json`

## Testing

**Unit Test Suite:**

- Run all unit tests: `PYTHONPATH=shared pytest shared/tests/unit -v`
- Run specific test file: `PYTHONPATH=shared pytest shared/tests/unit/test_analyzer_registry.py -v`

**Integration Test Suite:**

- Run all integration tests: `PYTHONPATH=shared pytest shared/tests/integration -v`
- Run specific integration test: `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v`

**Coverage Reports:**

- Generate coverage report: `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`

## Analyzer Registration & Imports

To avoid duplicate analyzer registrations during imports (especially in tests), follow these rules:

- Use the `analyzers.*` package root everywhere (implementation and tests). Do not import via `shared.analyzers.*`.
- The central registry bootstrap (`shared/core/base/registry_bootstrap.py`) imports analyzers via `analyzers.*`. Mixing roots (`shared.analyzers.*` and `analyzers.*`) in the same process causes double registration errors.
- Always run tests with `PYTHONPATH=shared` so the `analyzers` package root resolves to `shared/analyzers`.
- If you must patch module-level constants in tests, patch against the `analyzers.*` path (e.g., `analyzers.quality.coverage_analysis._LANGUAGE_CONFIG_PATH`).
- Never import the same analyzer module through two different roots in a single test session.

Quick example

- Good: `from analyzers.quality.coverage_analysis import TestCoverageAnalyzer`
- Avoid: `from shared.analyzers.quality.coverage_analysis import TestCoverageAnalyzer`
