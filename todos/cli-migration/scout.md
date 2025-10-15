# Project: AI-Assisted Workflows CLI Migration Assessment

---

## Executive Summary

This is a multi-system AI workflow management platform that maintains shared prompts and analyzers across Claude Code, OpenCode, and Codex systems. The project has a sophisticated analyzer registry system with 50+ specialized analyzers but relies on brittle path-probing in prompts to locate and execute Python modules.

- **Current Readiness**: Architecture foundation is solid with established analyzer registry, but CLI infrastructure is basic and prompts have complex path-discovery logic
- **Immediate Gaps**: Missing unified CLI interface, no standardized JSON output schema, prompts have duplicated path-probing blocks across systems

## Features

- Multi-system AI workflow orchestration (Claude Code, OpenCode, Codex)
- 50+ specialized code analyzers (security, performance, architecture, quality)
- Registry-driven analyzer architecture with pluggable design
- Shared prompt library with system-specific adaptations
- Comprehensive testing framework with unit and integration tests
- Build and quality gates with automated linting and type checking

## Tech Stack

- **Languages**: Python
- **Frameworks**: Custom analyzer framework, pytest for testing
- **Build Tools**: Custom shell installers, Python setuptools
- **Package Managers**: pip, requirements.txt (no uv yet)
- **Testing**: pytest with coverage, integration test suite
- **CLI**: Basic argparse-based CLI (registry-driven only)

## Structure

```markdown
project-root/
├── shared/ # Core analyzer framework and shared prompts
│ ├── analyzers/ # 50+ specialized analyzers by category
│ ├── core/ # Base classes, registry, and CLI infrastructure
│ ├── prompts/ # Shared prompt bodies (system-agnostic)
│ └── tests/ # Comprehensive test suite
├── systems/ # System-specific generated outputs
│ ├── claude-code/ # Claude Code commands and agents
│ ├── opencode/ # OpenCode agents and configurations
│ └── codex/ # Codex prompts and installers
├── docs/systems/ # System templates and documentation
│ └── templates/ # Jinja2 templates for system wrappers
└── tools/ # Empty - ready for enaible CLI
```

**Key Files**:

- `shared/core/base/analyzer_registry.py` - Registry pattern for analyzer management
- `shared/core/cli/run_analyzer.py` - Current CLI entrypoint using argparse
- `shared/analyzers/quality/complexity_lizard.py` - Example analyzer implementation
- `shared/prompts/analyze-security.md` - Example prompt with path-probing blocks
- `systems/claude-code/commands/analyze-security.md` - System-specific rendered prompt

**Entry Points**:

- `shared/core/cli/run_analyzer.py` - Current analyzer CLI
- System-specific prompts executed through Claude Code/OpenCode/Codex

## Architecture

The system follows a plugin architecture with a central registry pattern. Analyzers are registered by category:name (e.g., "quality:lizard", "security:semgrep") and created dynamically. The base analyzer class provides common functionality like file scanning, batch processing, and result formatting. Each system (Claude Code, OpenCode, Codex) renders shared prompts with system-specific frontmatter and configuration.

### Key Components:

- **AnalyzerRegistry**: Central registry for analyzer discovery and instantiation
- **BaseAnalyzer**: Shared infrastructure for file scanning, configuration, and results
- **AnalyzerConfig**: Configuration management with target paths and filtering
- **System Templates**: Jinja2 templates for system-specific prompt rendering
- **Shared Prompts**: System-agnostic prompt bodies with path-probing logic

## Backend Patterns and Practices

- **Registry Pattern**: All analyzers register themselves via decorators
- **Base Class Inheritance**: Common functionality inherited from BaseAnalyzer
- **Configuration Injection**: Analyzers receive configuration objects
- **Batch Processing**: Files processed in configurable batches
- **Result Standardization**: All analyzers produce structured JSON results
- **Error Handling**: Graceful degradation when tools are missing
- **Testing Infrastructure**: Comprehensive unit and integration test coverage

## Frontend Patterns and Practices

Not applicable - this is a CLI/agent system without traditional frontend components.

## Data & State

- **File-based State**: Configuration stored in YAML/JSON files
- **Temporary Artifacts**: Results stored in configurable output directories
- **Registry State**: In-memory analyzer registration during runtime
- **Configuration Factory**: Creates analyzer configs from command line args
- **No Persistent State**: Each execution is independent

## Performance & Security

- **Batch Processing**: Analyzers process files in configurable batches
- **Tool Availability Checks**: Graceful handling of missing external tools
- **Path Sanitization**: Input validation for file paths
- **Dependency Management**: External dependencies checked at runtime
- **Error Boundaries**: Fail-fast behavior with clear error messages

## Observability

| Aspect          | Current State       | Note                              |
| --------------- | ------------------- | --------------------------------- |
| Logging         | Basic stdout/stderr | No structured logging             |
| Metrics         | None                | No performance metrics collection |
| Analytics/Flags | None                | No feature flags or analytics     |

## Build & Quality Gates

| Purpose     | Command                                                | Notes                 |
| ----------- | ------------------------------------------------------ | --------------------- |
| Lint        | `ruff check shared/`                                   | Fast Python linter    |
| Type        | `mypy shared/`                                         | Static type checking  |
| Test        | `PYTHONPATH=shared pytest shared/tests/unit -v`        | Unit tests            |
| Integration | `PYTHONPATH=shared pytest shared/tests/integration -v` | Full workflow tests   |
| Coverage    | `pytest --cov=shared --cov-report=html`                | HTML coverage reports |

## Testing Practices

| Test type         | File path                                                    | Command                                                                                  |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests        | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration  | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage          | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |

## Git History Insights (20 days)

- **High Activity**: 39+ commits with refactor/feat/fix patterns indicating active development
- **CLI Migration Planning**: Recent commits show CLI migration documentation (`docs(cli): capture enaible CLI migration decisions`)
- **Prompt Consolidation**: Major refactoring to migrate prompts to shared system
- **System Installer Updates**: Codex installer improvements with merge behavior
- **Build Workflow**: New orchestration system with plan-exec-build workflow

---

## Task Impact Analysis

| File/Area                               | Rationale                                                           |
| --------------------------------------- | ------------------------------------------------------------------- |
| `shared/core/cli/run_analyzer.py`       | Current CLI needs to be replaced/extended by enaible CLI            |
| `shared/core/base/analyzer_registry.py` | Registry pattern ready for CLI integration                          |
| `shared/prompts/*.md`                   | All 18 prompts need path-probing blocks replaced with enaible calls |
| `systems/*/commands/*.md`               | System-specific prompts will be generated from templates            |
| `docs/systems/*/templates/`             | Template infrastructure ready for enaible integration               |
| `tools/`                                | Empty directory perfect location for enaible CLI package            |
| `requirements-dev.txt`                  | Needs typer/click, jinja2 dependencies added                        |
| `.gitignore`                            | Needs `.enaible/` artifacts directory pattern                       |

## Risks & Recommendations

| Risk                            | Mitigation                                                                  |
| ------------------------------- | --------------------------------------------------------------------------- |
| **Analyzer Contract Stability** | Define and stabilize JSON schema before CLI rollout                         |
| **Template Path Migration**     | Verify all docs/system/_/templates/_.j2 exist or create via migrate command |
| **Backward Compatibility**      | Remove path-probing blocks completely to avoid dual modes                   |
| **Performance**                 | Benchmark `uv run enaible` vs current direct Python execution               |
| **System Testing**              | Comprehensive integration tests for all three systems post-migration        |

## Open Questions

- **uv Integration Strategy**: Should the project adopt uv.lock and fully migrate to uv package management?
- **Artifact Storage**: Finalize `.enaible/` directory structure and retention policies
- **CLI Scope**: Confirm v1 scope includes full system assets or just commands/prompts
- **Template Engine**: Jinja2 integration patterns for system-specific rendering
- **Migration Timeline**: Phased rollout strategy starting with pilot prompts (analyze-security, get-primer)

The codebase is well-architected for the CLI migration with a solid registry pattern and established testing framework. The main work involves replacing path-probing blocks in prompts and building the enaible CLI wrapper around the existing analyzer infrastructure.
