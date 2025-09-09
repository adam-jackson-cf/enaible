# AI Assisted Workflows

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

---

> **Supporting AI Development Workflows with Core Principles**

The principles for this project are designed around the realities of coding with AI. We are approximately 60% complete on the work needed to fully meet these principles—see the [roadmap](docs/roadmap.md).

- **Lightweight (80%)**: Minimize context impact, load information just in time, and outsource to external processes (such as scripts) where possible.
- **Mitigate LLM Weaknesses (60%)**:
  - **Repeatability**: Ensure same inputs produce same outputs by using programmatic scripts for baseline analysis and leveraging LLMs for contextual framing and fallbacks.
  - **Predictability**: Scaffold task output that involves generation (e.g., for coding) using rules and templating.
  - **Duplication**: Create semantic-aware processes to prevent code duplication.
- **Minimize Structure (80%)**: Provide tools rather than dense workflows; aid in common tasks but allow flexibility.
- **LLM Agnostic (0%)**: Make any process agnostic to the LLM used to run them.
- **Popular Language Support (100%)**: Ensure workflows are compatible with baseline language support:
  - Python, TypeScript, Go, Rust, and C#.

---

## Overview

Supports common development activities like code review, planning, analysis, monitoring and debugging through slash commands and specialised agents for specific tasks.

## Example Use Cases (non exhaustive)

### Priming context

**Use case**: Coming in fresh to a new codebase or starting a new session requires systematic context gathering across documentation, architecture, and recent changes to avoid manual exploration and inconsistent understanding.

**LLM actions**:

- **Orchestrates parallel analysis** across documentation, structure, tech stack, commands, and git history
- **Correlates findings** from multiple sources (README, package.json, git commits) for comprehensive understanding
- **Generates standardized primer** with templated format for consistent project overviews
- **Understands recent changes** from recent commits to understand current development
- **Parallel Task agents** analyze purpose, tech stack, architecture, commands, testing in concurrent workflows

**Programmatic actions**:

- **MCP Serena LSP symbol search** - Language Server Protocol integration for semantic codebase analysis
- **Git history analysis** extracts last 3 commits for objective, files changed, and implementation patterns
- **Multi-source scanning** of key files (README, CLAUDE.md, package.json, Makefile, etc.)

**Benefits**:

- Works across any project structure or language
- Same analysis approach produces consistent primers
- Combines automated scanning with contextual interpretation
- Fast onboarding with comprehensive coverage (structure + patterns + recent changes)

**Common workflow**:

```bash
# Generate comprehensive project primer
/todo-primer

# Expected output: Structured markdown with project overview, tech stack,
# architecture, available commands, and recent development patterns
```

### Session history

**Use case**: Development sessions involve multiple decisions, discoveries, and context that gets lost between sessions, leading to repeated investigations and inconsistent approaches across team members.

**LLM actions**:

- **Automatic session documentation** capturing key decisions, discoveries, and reasoning throughout development work
- **Context preservation** maintaining thread of investigation across multiple sessions and team handoffs
- **Decision rationale recording** documenting why certain approaches were chosen or rejected
- **Knowledge synthesis** connecting session insights to broader project understanding

**Programmatic actions**:

- **Structured note templates** ensure consistent documentation format across sessions and team members

**Benefits**:

- Prevents repeated investigation of the same issues
- Enables smooth handoffs between team members and sessions
- Creates searchable knowledge base of project decisions and discoveries
- Maintains development context across extended timeframes

**Common workflow**:

```bash
# Document current session insights and decisions
/session-notes

# Expected output: Timestamped documentation of key decisions,
# discoveries, and reasoning for future reference
```

### Technical research

**Use case**: Complex technical investigations require systematic research across documentation, code repositories, academic sources, and current implementations to make informed decisions without bias toward familiar solutions.

**LLM actions**:

- **Research strategy coordination** planning investigation across multiple sources and specialist researchers
- **Information synthesis** correlating findings from documentation, code analysis, and implementation examples
- **Bias mitigation** ensuring comprehensive coverage beyond familiar technologies and approaches
- **Evidence-based recommendations** weighing technical trade-offs with supporting research and examples
- **@agent-research-coordinator** strategically plans and allocates research tasks across specialist researchers
- **@agent-technical-researcher** analyzes code repositories, GitHub projects, and implementation details
- **@agent-docs-scraper** extracts and processes technical documentation from various sources

**Programmatic actions**:

- **Coordinate scrape and fetch** docs scraper agent uses external tools to gather identified information to minimise context impact

**Benefits**:

- Systematic approach prevents research blind spots and confirmation bias
- Specialist agents provide deep expertise in their respective domains
- Comprehensive coverage across documentation, implementations, and academic sources
- Evidence-based decision making with supporting research and examples

**Common workflow**:

```bash
# Coordinate comprehensive technical research
# @agent-research-coordinator plans investigation strategy
# @agent-technical-researcher analyzes implementations
# @agent-docs-scraper processes documentation

Invoke the @agent-research-coordinator to research a best practices markdown document for implementing Agentic rag, including recent innovations

# Expected output: Synthesized research report with implementation examples,
# documentation analysis, and evidence-based recommendations
```

### Planning a feature

**Use case**: Feature development requires balancing user needs, technical constraints, and existing architecture to deliver valuable functionality without compromising system maintainability or introducing technical debt.

**LLM actions**:

- **Requirements analysis** translating user needs into technical specifications with clear acceptance criteria
- **Architecture integration planning** ensuring new features align with existing system design and patterns
- **Implementation strategy development** breaking complex features into manageable, testable components
- **Risk assessment and mitigation** identifying potential issues early and planning preventive measures

**Programmatic actions**:

- **Technical feasibility validation** analyzing existing codebase constraints and integration points
- **User story template generation** standardizing feature requirements with consistent format and criteria
- **Implementation task breakdown** creating actionable development tasks with dependencies and estimates
- **Quality gate integration** ensuring testing, security, and performance considerations from planning phase

**Benefits**:

- Systematic approach prevents feature creep and scope misalignment
- Early technical validation reduces implementation risks and rework
- Consistent planning format enables better estimation and team coordination
- Quality considerations integrated from planning prevent post-development issues

**Common workflow**:

```bash
# Feature planning with technical validation
# Analyze user requirements and existing system constraints
# Generate implementation strategy and task breakdown
# Validate feasibility and integration approach

# Expected output: Detailed feature specification with user stories,
# technical implementation plan, and quality gate requirements
```

### Planning a product from scratch

**Use case**: New product development requires market research, user needs analysis, and competitive positioning to create products that solve real problems while avoiding feature bloat and market misalignment.

**LLM actions**:

- **Product Requirements Document generation** structuring vision, objectives, target users, and success metrics systematically
- **Feature prioritization framework** balancing user value, technical complexity, and competitive differentiation
- **User experience planning** designing workflows and interactions based on user research insights
- **Go-to-market strategy integration** aligning product features with market positioning and business objectives

**Programmatic actions**:

- **Competitive intelligence agent** analyzes existing solutions, pricing models, and market gaps
- **User research agent** validates assumptions through market analysis and user behavior patterns
- **Multi-agent validation** ensures technical feasibility aligns with market requirements
- **PRD template standardization** maintains consistency across product planning initiatives

**Benefits**:

- Market-informed product decisions reduce launch risks and feature misalignment
- Systematic user research prevents building products nobody wants
- Competitive analysis identifies differentiation opportunities and market gaps
- Structured PRD process ensures all stakeholders align on product vision
- More UX focused than standard PRD, aims to make it focused at LLM's as opposed to PM's

**Common workflow**:

```bash
# Product planning with market validation
/plan-ux-prd "AI-powered code review tool for enterprise teams"

# validate with @agent-competitive-intelligence-analyst
# validate with @agent-user-researcher

# Expected output: Comprehensive PRD with market analysis, user research insights,
# competitive positioning, feature priorities, and go-to-market strategy
```

### Plan technical solution

**Use case**: Complex technical implementations require structured planning with risk assessment, architectural considerations, and validation to avoid over-engineering while ensuring scalable, maintainable solutions.

**LLM actions**:

- **Architecture design guidance** balancing complexity, maintainability, and performance requirements
- **Risk assessment integration** identifying technical risks, scalability concerns, and mitigation strategies
- **Implementation roadmap generation** with milestones, dependencies, and validation checkpoints
- **CTO agent validation** provides senior-level technical review and architectural feedback with --critique (using reasoning through perspective)

**Programmatic actions**:

- **Clarifying questions methodology** gathering requirements, constraints, scale, and success criteria systematically
- **Prototype mode support** enables rapid validation of core concepts before full implementation
- **Implementation plan documentation** captures decisions, rationale, and next steps for team alignment

**Benefits**:

- Structured approach prevents over-engineering and scope creep
- Senior-level validation catches architectural issues early
- Clear implementation roadmap enables team coordination and progress tracking
- Systematic risk assessment reduces project failures

**Common workflow**:

```bash
# Structured technical solution planning
/plan-solution "implement real-time collaboration features with conflict resolution" [Optional: --critique]

# [System asks clarifying questions about scale, requirements, constraints]

# Senior technical validation
# validate the plan with @agent-cto

# Multi-agent implementation orchestration
/todo-orchestrate implementation-plan.md --prototype

# Expected output: Validated technical plan, risk assessment,
# implementation roadmap, and agent orchestration workflow
```

### Project setup including quality gates

**Use case**: New projects require consistent setup of testing frameworks, CI pipelines, quality gates, and monitoring to prevent technical debt accumulation and ensure maintainable development workflows from project inception.

**LLM actions**:

- **Requirements analysis** from todos/markdown files to understand project scope and infrastructure needs
- **Technology-specific configuration** adapting quality gates to detected languages and frameworks
- **Monitoring strategy planning** based on project type (API, frontend, full-stack) and expected scale
- **Integration coordination** ensuring CI, monitoring, and quality tools work together seamlessly

**Programmatic actions**:

- **Standardized configurations** leverages [better-t-stack](https://better-t-stack.dev/) applied across projects: pre-commit hooks, CI workflows, linting rules
- **Automated dependency setup** installs and configures testing frameworks, quality analyzers, monitoring tools
- **MCP Serena integration** provides enhanced LSP-based codebase search capabilities
- **Quality gate enforcement** via pre-commit, CI/CD, and automated analysis tool integration

**Benefits**:

- Consistent development environment across all projects
- Quality enforcement from first commit prevents technical debt accumulation
- Automated setup reduces configuration errors and saves setup time
- Monitoring and analysis tools integrated from project start

**Common workflow**:

```bash
# Create new project with requirements-driven setup
/create-project inventory-api --from-todos project-requirements.md

# Add development monitoring and quality gates
/setup-dev-monitoring
/add-code-precommit-checks

# Enable enhanced codebase search capabilities
/setup-serena-mcp
```

### Code quality analysis

**Use case**: Code quality assessment requires measurable metrics and systematic evaluation to identify technical debt, maintainability issues, and refactoring opportunities before they impact development velocity.

**LLM actions**:

- **Quality metrics interpretation** analyzing complexity, maintainability, and architectural compliance in business context
- **Technical debt prioritization** ranking improvement opportunities by impact and implementation effort
- **Best practices compliance evaluation** comparing code patterns against SOLID principles and design standards
- **Improvement roadmap generation** with specific recommendations and refactoring strategies

**Programmatic actions**:

- **Lizard complexity analyzer** provides cyclomatic complexity, function length, and parameter count analysis
- **Code duplication detection** identifies repeated patterns and refactoring candidates
- **Coverage analysis integration** assesses test quality and testability
- **Pattern classification** detects anti-patterns and design pattern compliance

**Benefits**:

- Measurable quality metrics enable objective improvement tracking
- Systematic evaluation identifies technical debt before it impacts velocity
- Works across multiple programming languages with consistent analysis
- Prioritized recommendations focus efforts on high-impact improvements

**Common workflow**:

```bash
# Comprehensive quality analysis of codebase
/analyze-code-quality src/

# Expected output: Complexity metrics, technical debt assessment,
# best practices compliance, and prioritized improvement recommendations
```

### Code security analysis

**Use case**: Security vulnerability assessment requires comprehensive OWASP Top 10 coverage combined with contextual threat analysis to identify real security risks while minimizing false positives in complex applications.

```bash
/analyze-security src/ --verbose
```

**LLM actions**:

- **Three-phase systematic approach** with user confirmations: automated assessment → gap analysis → risk prioritization
- **OWASP Top 10 framework integration** contextualizing automated findings against standard security categories
- **Technology-specific threat assessment** analyzing framework-specific protections (Django CSRF, React XSS, Express headers)
- **Risk correlation and prioritization** combining automated findings with business context for actionable recommendations

**Programmatic actions**:

- **Semgrep semantic analysis** detects OWASP Top 10 vulnerabilities: injection (A01), XSS (A03), authentication failures (A07)
- **Detect-secrets entropy analysis** finds hardcoded credentials and API keys using advanced pattern matching
- **Framework-specific configuration validation** checks security settings for detected technology stacks
- **Multi-phase execution** with quality gates ensuring thorough coverage without overwhelming output

**Benefits**:

- Comprehensive OWASP coverage reduces security blind spots
- False positive reduction through contextual analysis and semantic understanding
- Framework-aware assessment provides technology-specific recommendations
- Systematic approach prevents security debt accumulation

**Common workflow**:

```bash
# Comprehensive security analysis with detailed output
/analyze-security . --verbose

# Three-phase process:
# Phase 1: Automated scanning (semgrep + detect-secrets)
# Phase 2: Gap assessment and framework-specific analysis
# Phase 3: Risk prioritization and actionable recommendations
```

### Performance bottlenecks

**Use case**: Performance optimization requires systematic identification of bottlenecks across database queries, frontend rendering, algorithm complexity, and network requests to prioritize improvements by user impact and implementation effort.

```bash
/analyze-performance src/
```

**LLM actions**:

- **Multi-layer performance analysis** correlating findings across database, frontend, and algorithm performance
- **Bottleneck prioritization** ranking optimizations by user experience impact and implementation complexity
- **Optimization strategy recommendations** with before/after validation approaches and performance benchmarks
- **User experience context** connecting technical metrics to business impact and user satisfaction

**Programmatic actions**:

- **Flake8-perf analyzer** detects Python performance anti-patterns and inefficient code constructs
- **Frontend performance analysis** examines bundle size, render optimization, and memory leak patterns
- **SQLFluff analyzer** identifies database query optimization opportunities and N+1 problems
- **Algorithm complexity assessment** profiles CPU/memory usage and identifies optimization candidates

**Benefits**:

- Multi-layer analysis catches performance issues across the full stack
- Measurable metrics enable objective optimization tracking and validation
- Prioritized recommendations focus efforts on high-impact improvements
- Works across backend, frontend, and database performance domains

**Common workflow**:

```bash
# Comprehensive performance analysis across all layers
/analyze-performance .

# Expected output: Database optimization opportunities, frontend performance metrics,
# algorithm complexity analysis, and prioritized optimization recommendations
```

### Debugging & Root Cause Analysis

**Use case**: API timeouts, production crashes, and intermittent failures require systematic investigation across code changes, execution patterns, and known error signatures. Traditional debugging relies on developer intuition and manual log analysis, leading to inconsistent results and missed root causes.

```bash
/analyze-root-cause "API timeouts on /users endpoint after deployment" [--verbose]
```

**LLM actions**:

- **Interprets standardized JSON results** from three analyzers with consistent structure for reliable parsing
- **Applies contextual reasoning** to correlate findings across execution patterns, recent changes, and error signatures
- **Generates investigation priorities** based on error context and timing analysis
- **Provides human-readable explanations** while maintaining evidence-based recommendations
- **Verbose flag enables comprehensive diagnostic output** including distributed tracing setup and detailed error context

**Programmatic actions**:

- **`root_cause:trace_execution`** - Analyzes execution patterns with **error-context targeting** (requires specific error info for focused investigation)
  - Parses error messages to extract file/line context using **language-agnostic regex patterns**
  - Identifies missing error handling around failure points with **consistent pattern matching**
- **`root_cause:recent_changes`** - Git history analysis for **risky change correlation** over configurable timeframes (default: 30 days, 100 commits)
  - **Pattern-based detection** of hotfixes, rollbacks, and emergency commits for **repeatable results**
  - **Timing analysis** identifies weekend/late-night commits indicating emergency responses
  - **Change category classification**: authentication, database, API, configuration, dependencies, critical files
- **`root_cause:error_patterns`** - **Known error pattern detection** across 9 categories for **systematic investigation**
  - **Multi-language pattern matching**: memory leaks, null pointers, race conditions, injection vulnerabilities
  - **Contextual pattern analysis** reduces false positives through refined regex patterns
  - **Error clustering analysis** identifies systemic issues across codebase

**Benefits**:

- Works across all project supported languages
- Same error input produces consistent pattern analysis across runs
- Looks for process failures not just bugs
- ensures comprehensive investigation (code patterns + change history + execution analysis)

**Common workflow**:

```bash
# Quick root cause analysis with standard output
/analyze-root-cause "API timeouts on /users endpoint"

# Comprehensive investigation with detailed diagnostics
/analyze-root-cause "Database connection pool exhausted during peak traffic" --verbose

# Focus on specific error with structured investigation
/analyze-root-cause "TypeError: Cannot read property 'id' of undefined at UserService.js:42"

```

### Background task execution

**Use case**: Long-running development tasks like comprehensive refactoring, extensive documentation generation, or complex analysis require autonomous execution without blocking current work sessions, while maintaining progress tracking and result documentation.

**LLM actions**:

- **Autonomous task execution** running complex development workflows independently in background processes
- **Progress documentation** automatically capturing decisions, discoveries, and implementation steps throughout execution
- **Multi-CLI orchestration** coordinating tasks across Claude Code, Qwen, and Gemini based on task requirements and resource availability
- **Continuous reporting** maintaining detailed logs and results in structured markdown reports for later review

**Programmatic actions**:

- **Background process management** launching AI CLI instances with appropriate automation flags for unattended operation
- **Report file generation** creating timestamped documentation with task context, progress updates, and final outcomes
- **CLI-specific optimization** using Claude Code for complex reasoning, Qwen/Gemini for cost-effective long-running tasks
- **Process monitoring** enabling progress tracking and output capture for running background tasks

**Benefits**:

- **Non-blocking execution** allows continued development while complex tasks run autonomously in background
- **Resource optimization** leverages free capacity of Qwen and Gemini CLIs for cost-effective long-running operations
- **Comprehensive documentation** ensures no work is lost with detailed progress tracking and decision capture
- **Flexible model selection** enables choosing appropriate AI capability (Claude Opus for complex reasoning, alternatives for routine tasks)
- **Parallel development** supports multiple concurrent background tasks while maintaining primary development flow

**Common workflow**:

```bash
# Complex refactoring with detailed documentation using Claude Opus
/todo-background "Refactor authentication module to use OAuth 2.0" claude:opus ./reports/auth-refactor.md

# Cost-effective documentation generation using Qwen
/todo-background "Generate comprehensive API documentation for all endpoints" qwen

# Long-running analysis using Gemini with auto-generated report
/todo-background "Analyze codebase for performance optimization opportunities" gemini

# Expected output: Background process running autonomously with progress
# reports saved to specified files for later review and integration
```

## How do you want to work?

These examples give a flavour, I would recommend exploring and adapting the features to the way you want to work.

## Quick Start

- **Installation**: [See Installation Guide](docs/installation.md)
- **First Steps**: [See Workflow Examples](docs/workflow-examples.md)
- **Agent System**: [See Agent Orchestration](docs/agents.md)

---

## Detailed Documentation

- [Installation Guide](docs/installation.md) - Setup and configuration
- [Agent Orchestration System](docs/agents.md) - Multi-agent workflows
- [Language Support](docs/analysis-scripts.md) - Supported languages and analysis types
- [Workflow Examples](docs/workflow-examples.md) - Common usage patterns

## License

MIT License - See LICENSE file for details.
