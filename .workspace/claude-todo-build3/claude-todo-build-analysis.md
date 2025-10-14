<!-- ran on glm 4.6 took less than 4 mins -->

# Project: AI-Assisted Workflows

---

## Executive Summary

AI-Assisted Workflows is a comprehensive development automation system combining Claude Code CLI workflows, Python analysis tools, and multi-agent orchestration for intelligent code quality management. The project demonstrates a mature architecture with three distinct system implementations (Codex, Claude Code, OpenCode) built around a shared Python analysis infrastructure.

- **Current Readiness**: The codebase shows excellent architectural maturity with a well-established BaseAnalyzer framework, 22+ analysis tools, and sophisticated agent orchestration patterns. Recent ExecPlan and orchestration improvements indicate active development of advanced workflow automation.
- **Immediate Gaps**: Missing direct Claude Code equivalent of the sophisticated Codex todo-build workflow; opportunity exists to leverage Claude Code's native Task tool and agent system for enhanced implementation.

## Features

- **Multi-System Architecture**: Three parallel CLI implementations (Codex, Claude Code, OpenCode) with shared analysis backend
- **22 Analysis Tools**: Security, quality, architecture, performance, and root-cause analysis capabilities
- **8-Agent Orchestration**: State-machine workflow management with quality gates and escalation patterns
- **ExecPlan System**: Living project documentation and execution planning framework
- **Comprehensive Testing**: Unit, integration, and E2E test suites with controlled test applications
- **Cross-Platform Support**: Installation scripts for multiple platforms and CI/CD integration

## Tech Stack

- **Languages**: Python 3.11+, TypeScript/JavaScript, Bash/Shell, SQL
- **Frameworks**: pytest, FastAPI concepts, GitHub Actions
- **Build Tools**: Custom Python CLI framework, Rich CLI, Click patterns
- **Package Managers**: pip, uv (in migration plans), npm (for MCP tools)
- **Testing**: pytest, pytest-cov, custom evaluation frameworks
- **Security Tools**: Semgrep (deferred), detect-secrets, pattern analysis
- **Quality Analysis**: Lizard, Ruff, JSCPD, custom complexity analyzers

## Structure

```markdown
ai-assisted-workflows/
├── systems/ # CLI workflows and configurations for supported runtimes
│ ├── claude-code/ # Claude Code CLI workflows and configurations
│ │ ├── commands/ # 24 slash commands for development workflows
│ │ ├── agents/ # 23 specialized agents (orchestration, specialists, research/UX, handlers)
│ │ ├── rules/ # Technology-specific coding standards and best practices
│ │ └── install.sh/.ps1 # Cross-platform installation scripts
│ ├── codex/ # Codex CLI prompts, rules, and installers
│ │ ├── prompts/ # Prompt definitions and bodies for Codex workflows
│ │ └── rules/ # Codex-specific operating rules and guardrails
│ └── opencode/ # OpenCode CLI workflows and configurations
├── shared/ # Core Python analysis infrastructure
│ ├── core/base/ # BaseAnalyzer and BaseProfiler frameworks
│ ├── analyzers/ # 22 analysis tools across 5 categories
│ ├── config/ # Configuration templates and CI workflows
│ └── tests/ # Comprehensive test suite with E2E integration tests
├── test_codebase/ # Controlled test applications for validation
└── docs/ # Comprehensive project documentation
```

**Key Files**:

- `systems/codex/prompts/todo-build.md` - Reference implementation for todo-build workflow
- `shared/core/base/analyzer_base.py` - Base framework for all analysis tools
- `systems/claude-code/commands/` - Existing Claude Code slash commands
- `systems/claude-code/agents/research-coordinator.md` - Agent orchestration patterns

**Entry Points**:

- `systems/claude-code/commands/` - Claude Code slash commands
- `shared/analyzers/` - Direct Python analysis tool execution
- `shared/tests/integration/` - Comprehensive testing and evaluation frameworks

## Architecture

The system uses a hybrid AI-automation approach combining traditional static analysis with modern ML techniques. The architecture demonstrates clear separation of concerns with three CLI frontends sharing a common Python analysis backend, enabling consistent tooling across different development environments.

### Key Components:

- **BaseAnalyzer Framework**: Provides shared infrastructure for all 22 analysis tools with strict validation, file scanning, configuration management, and result formatting
- **Multi-Agent Orchestration**: 8-agent system with state-machine workflow management, quality gates, and CTO escalation patterns
- **ExecPlan System**: Living project documentation framework that serves as single source of truth for planning and execution
- **Analysis Registry**: Centralized tool discovery and execution via `python -m core.cli.run_analyzer` pattern

## Backend Patterns and Practices

The project demonstrates sophisticated backend patterns with strong emphasis on code reuse, validation, and extensibility:

- **Abstract Base Classes**: BaseAnalyzer and BaseProfiler provide consistent interfaces across all analysis tools
- **Registry Pattern**: Centralized analyzer registration with bootstrap system for dependency management
- **Configuration Factory**: Standardized configuration management with validation rules
- **Result Formatting**: Consistent finding structure with validation rules preventing placeholder content
- **Batch Processing**: Memory-efficient file processing with configurable batch sizes
- **Error Handling**: Comprehensive error handling with detailed logging and operation tracking

## Frontend Patterns and Practices

The system supports multiple frontend approaches while maintaining consistent user experience:

- **Slash Commands**: 24 Claude Code commands following consistent argument patterns and help structures
- **Agent-Based Workflows**: Complex multi-step processes orchestrated through specialized agents
- **CLI Discovery**: Standardized script discovery pattern supporting project-level and user-level installations
- **Status Line Integration**: Git worktree status integration for enhanced developer experience

## Data & State

The project uses a sophisticated approach to data management and state tracking:

- **ExecPlan Documents**: Living project documentation that serves as single source of truth
- **Git Worktrees**: Isolated development environments for parallel workflow execution
- **Configuration Management**: Hierarchical configuration with validation and type safety
- **Analysis Results**: Standardized finding format with metadata and severity classification
- **Operation Logging**: Comprehensive audit trail for all analysis operations

## Performance & Security

Performance and security are core considerations in the system design:

- **File Filtering**: Intelligent file exclusion patterns including vendor code detection
- **Batch Processing**: Memory-efficient processing of large codebases
- **Timeout Management**: Configurable timeouts preventing infinite analysis loops
- **Secrets Detection**: Integration with detect-secrets for sensitive information identification
- **Security Analysis**: 5 dedicated security analyzers covering vulnerability patterns

## Observability

| Aspect          | Current State | Note                                                       |
| --------------- | ------------- | ---------------------------------------------------------- |
| Logging         | Comprehensive | Structured logging with operation tracking in BaseAnalyzer |
| Metrics         | Basic         | File processing counts, error tracking, timing information |
| Analytics/Flags | Limited       | No built-in feature flags or advanced analytics            |

## Build & Quality Gates

| Purpose     | Command       | Notes                                                     |
| ----------- | ------------- | --------------------------------------------------------- |
| Lint        | `ruff check`  | Fast Python linting with configurable rules               |
| Type        | `mypy shared` | Static type checking for Python codebase                  |
| Test        | `pytest`      | Comprehensive test suite with unit/integration separation |
| Duplication | `jscpd`       | Code duplication detection across files                   |
| Complexity  | `lizard`      | Cyclomatic complexity analysis with thresholds            |

## Testing Practices

| Test type         | File path                                                    | Command                                                                                  |
| ----------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Unit tests        | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit -v`                                          |
| Integration tests | `shared/tests/integration/`                                  | `PYTHONPATH=shared pytest shared/tests/integration -v`                                   |
| Full integration  | `shared/tests/integration/test_integration_all_analyzers.py` | `PYTHONPATH=shared pytest shared/tests/integration/test_integration_all_analyzers.py -v` |
| Coverage          | `shared/tests/unit/`                                         | `PYTHONPATH=shared pytest shared/tests/unit --cov=shared --cov-report=html`              |
| E2E / System      | `test_codebase/`                                             | `PYTHONPATH=shared pytest shared/tests/integration -k e2e -v`                            |

## Git History Insights (20 days)

- **ExecPlan Development** • Recent commits show active ExecPlan system development with template creation and integration
- **Orchestration Enhancements** • todo-orchestrate and create-execprompts added to Codex system with refined workflows
- **Migration Planning** • CLI migration improvements with Typer + uv architecture decisions
- **Build Workflow Refinement** • New build workflow iterations with quality gate enforcement

---

## Task Impact Analysis

| File/Area                             | Rationale                                                                                                               |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `systems/codex/prompts/todo-build.md` | Reference implementation showing sophisticated workflow with git worktrees, PR automation, and quality gate enforcement |
| `systems/claude-code/agents/`         | 23 specialized agents provide orchestration patterns that can enhance todo-build implementation                         |
| `shared/core/base/analyzer_base.py`   | BaseAnalyzer framework provides infrastructure for quality gate integration                                             |
| `systems/claude-code/commands/`       | Existing 24 commands show integration patterns for new todo-build implementation                                        |
| `systems/codex/prompts/plan-exec.md`  | ExecPlan creation system that could be integrated with todo-build for planning phase                                    |

---

## Risks & Recommendations

| Risk                         | Mitigation                                                                                  |
| ---------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Complexity Gap**           | Codex todo-build is significantly more sophisticated than typical Claude Code commands      | Leverage Claude Code's native Task tool and agent system to create enhanced implementation |
| **Git Worktree Management**  | Complex git worktree logic requires careful implementation for cross-platform compatibility | Use existing git statusline integration patterns from Claude Code system                   |
| **Quality Gate Integration** | Need to integrate Python analysis tools with Claude Code workflows                          | Leverage existing script discovery pattern and BaseAnalyzer framework                      |
| **PR Automation**            | GitHub CLI integration requires authentication and proper error handling                    | Follow existing patterns from Claude Code commands and use gh command appropriately        |

---

## Open Questions

## Implementation Strategy for Claude Code todo-build

The analysis reveals that replicating Codex's todo-build for Claude Code requires thoughtful adaptation rather than direct translation. Key implementation considerations:

**Architectural Advantages in Claude Code:**

- Native Task tool provides built-in todo management superior to manual todo tracking
- Agent system enables sophisticated orchestration with specialized expertise
- Serena MCP integration provides enhanced codebase search capabilities
- Existing command infrastructure offers proven patterns for implementation

**Recommended Implementation Approach:**

1. **Hybrid Workflow**: Combine ExecPlan planning phase with Claude Code's agent orchestration
2. **Agent-Enhanced Execution**: Use specialized agents (git-manager, quality-monitor, plan-manager) for workflow steps
3. **Native Todo Integration**: Leverage Task tool instead of manual todo list management
4. **Quality Gate Integration**: Use existing script discovery pattern for Python analyzer integration
5. **Progressive Enhancement**: Start with core workflow and add advanced features iteratively

**Key Differentiators from Codex Implementation:**

- Enhanced context awareness through agent orchestration
- Superior search capabilities via Serena MCP
- Native todo management through Task tool
- Simplified git operations through existing statusline integration
- More sophisticated error handling and recovery patterns

The implementation should leverage Claude Code's unique strengths rather than attempting feature-parity replication, resulting in a workflow that's potentially more sophisticated and context-aware than the original Codex implementation.
