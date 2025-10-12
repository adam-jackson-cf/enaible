# Programming Language Support and Analysis Capabilities

## Platform Support

- Installation copies shared analyzers to your editor’s scripts folder.
  - Claude Code
    - Project: `./.claude/scripts/analyzers/`
    - User: `~/.claude/scripts/analyzers/`
  - OpenCode
    - Project: `./.opencode/scripts/analyzers/`
    - User: `~/.config/opencode/scripts/analyzers/`
- Resolution order: project scope, then user scope.
- Invocation

  - Use editor commands (recommended): `/analyze-security`, `/analyze-code-quality`, `/analyze-architecture`, `/analyze-performance`, `/analyze-root-cause`.
  - Programmatic runner (both platforms):

    ```bash
    # Set PYTHONPATH to your platform scripts root, then run analyzer by key
    PYTHONPATH=~/.claude/scripts \
      python -m core.cli.run_analyzer --analyzer security:semgrep --target . --output-format json

    PYTHONPATH=~/.config/opencode/scripts \
      python -m core.cli.run_analyzer --analyzer quality:lizard --target . --output-format json
    ```

## Supported Languages

**Core Support:** Python, JavaScript, TypeScript, Java, C#, Go, Rust, PHP, Ruby, C/C++, Swift, Kotlin, SQL, and more

| Language            | Test Coverage            | Performance Baseline          | Import Analysis         | Bottleneck Detection    |
| :------------------ | :----------------------- | :---------------------------- | :---------------------- | :---------------------- |
| **Python**          | ✅ pytest, coverage      | ✅ cProfile, memory-profiler  | ✅ import patterns      | ✅ AST analysis         |
| **JavaScript**      | ✅ jest, nyc, c8         | ✅ npm scripts, profiling     | ✅ import/require       | ✅ performance patterns |
| **TypeScript**      | ✅ jest, nyc, c8         | ✅ npm scripts, profiling     | ✅ import patterns      | ✅ performance patterns |
| **Java**            | ✅ junit, jacoco         | ✅ maven/gradle, JFR          | ✅ import statements    | ✅ performance patterns |
| **Go**              | ✅ go test, coverage     | ✅ go build, benchmarks       | ✅ import patterns      | ✅ performance patterns |
| **Rust**            | ✅ cargo test, tarpaulin | ✅ cargo bench, flamegraph    | ✅ use statements       | ✅ performance patterns |
| **C#**              | ✅ dotnet test, coverlet | ✅ dotnet build, profiling    | ✅ using statements     | ✅ performance patterns |
| **SQL**             | ✅ SQLGlot parsing       | ✅ Query performance analysis | ✅ Schema dependencies  | ✅ Query optimization   |
| **Other Languages** | ✅ Framework detection   | ✅ Language-specific patterns | ✅ Full import analysis | ✅ Performance patterns |

## Base & Deferred Dependencies

### Python (installed by installer)

- `lizard` — Cross-language complexity metrics
- `ruff` — Python linting + performance rules (PERF/C4/B)
- `sqlglot` — SQL parsing and rule-based analysis
- `detect-secrets` — Hardcoded secrets detection
- Lightweight infra: `pyyaml`, `jinja2`, `click`, `rich`, `platformdirs`, `filelock`, `watchdog`

### Node (installed by installer)

- `eslint` + plugins — Frontend/JS/TS analysis
- `jscpd` — Universal copy/paste detection

### Deferred Tools (installed on demand or detected if present)

- `semgrep` — Universal performance/security heuristics
- Language add‑ons (opt-in): `clang-tidy` (C/C++), PMD (Java), detekt (Kotlin), `golangci-lint` (Go), `cargo clippy` (Rust), Roslyn/.NET analyzers (C#)

## Analysis Scripts Architecture

The analysis system is organized under `shared/` with the following structure:

```
shared/
├── analyzers/               # 22 Analysis Tools by Category
│   ├── security/           # Security vulnerability detection
│   │   ├── semgrep_analyzer.py
│   │   └── detect_secrets_analyzer.py
│   ├── performance/        # Performance analysis and optimization
│   │   ├── profile_code.py
│   │   ├── performance_baseline.py
│   │   ├── analyze_frontend.py
│   │   ├── ruff_analyzer.py
│   │   ├── sqlglot_analyzer.py
│   │   └── semgrep_analyzer.py
│   ├── architecture/       # Design and architectural analysis
│   │   ├── dependency_analysis.py
│   │   ├── coupling_analysis.py
│   │   ├── scalability_check.py
│   │   └── pattern_evaluation.py
│   ├── quality/           # Code quality and complexity metrics
│   │   ├── complexity_lizard.py
│   │   ├── jscpd_analyzer.py
│   │   ├── coverage_analysis.py
│   │   ├── pattern_classifier.py
│   │   └── result_aggregator.py
│   └── root_cause/        # Debugging and error analysis
│       ├── error_patterns.py
│       ├── recent_changes.py
│       └── trace_execution.py
├── core/base/             # BaseAnalyzer framework
├── ci/                    # Continuous improvement framework
├── setup/                 # Installation and dependency management
├── generators/            # Code generation utilities
├── tests/                 # Integration tests
└── utils/                 # Shared utilities
```

### Security Analysis (2 Analyzers)

**`semgrep_analyzer.py`** - Semantic Static Analysis Security Scanner

- OWASP Top 10 vulnerability detection using Semgrep's semantic analysis
- Multi-language support with native language parsers
- Real-time rule updates from security community
- Replaces bespoke regex patterns with established semantic analysis

**`detect_secrets_analyzer.py`** - Hardcoded Secrets Detection

- Identifies API keys, passwords, tokens in source code
- Uses entropy-based detection and known patterns
- Supports multiple secret types and custom patterns
- Replaces manual regex-based secret scanning

### Performance Analysis (5 Analyzers)

**`profile_code.py`** - Code Profiling and Bottleneck Detection

- Performance profiling using cProfile and memory-profiler
- Identifies CPU and memory bottlenecks
- Generates performance reports with hotspot analysis
- Cross-platform profiling support

**`performance_baseline.py`** - Performance Baseline Establishment

- Establishes performance baselines for critical code paths
- Tracks performance regression over time
- Supports custom performance metrics and thresholds
- Integration with CI/CD pipelines

**`analyze_frontend.py`** - Frontend Performance Analysis

- JavaScript/TypeScript performance analysis
- Bundle size analysis and optimization suggestions
- React/Vue/Angular specific performance patterns
- Integration with ESLint performance plugins

**`ruff_analyzer.py`** - Python Performance Anti-patterns

- Uses Ruff (PERF/C4/B) for performance/efficiency rules
- Identifies inefficient comprehensions, loops, and constructs
- Maps codes to actionable recommendations

**`sqlglot_analyzer.py`** - SQL Performance Analysis

- SQL parsing and config-driven anti-pattern detection via SQLGlot
- Identifies inefficient queries, missing pagination, and N+1 indicators
- Multi-dialect SQL support with parser-driven heuristics

**`semgrep_analyzer.py`** - Universal Performance Heuristics

- Multi-language performance/best-practice rules via Semgrep
- Deferred installation; runs when available or auto‑installs if enabled

### Architecture Analysis (4 Analyzers)

**`dependency_analysis.py`** - Dependency Graph Analysis

- Analyzes import dependencies and circular references
- Generates dependency graphs using NetworkX
- Identifies architectural violations and tight coupling
- Supports multiple languages and module systems

**`coupling_analysis.py`** - Module Coupling Metrics

- Measures coupling between modules and classes
- Identifies high coupling that affects maintainability
- Provides refactoring suggestions for decoupling
- Generates coupling heat maps and reports

**`scalability_check.py`** - Scalability Assessment

- Analyzes code patterns for scalability issues
- Identifies performance bottlenecks under load
- Database query analysis for scalability
- Concurrent programming pattern analysis

**`pattern_evaluation.py`** - Architecture Pattern Evaluation

- Evaluates adherence to architectural patterns (MVC, DDD, etc.)
- Identifies anti-patterns and code smells
- Suggests architectural improvements
- Pattern compliance scoring and reporting

### Quality Analysis (5 Analyzers)

**`complexity_lizard.py`** - Code Complexity Analysis

- Uses Lizard for multi-language complexity analysis
- Cyclomatic complexity, Halstead metrics, and NLOC
- Identifies overly complex functions and classes
- Supports Python, JavaScript, Java, C++, and more

**`jscpd_analyzer.py`** - Duplicate Code Detection

- Universal copy/paste detection using jscpd (Node)
- Deterministic token-based detection across many languages

**`coverage_analysis.py`** - Test Coverage Analysis

- Multi-language test coverage analysis
- Integration with pytest, jest, junit, and other frameworks
- Coverage gap identification and recommendations
- Historical coverage trend analysis

**`pattern_classifier.py`** - Code Pattern Classification

- Classifies code patterns and architectural elements
- Identifies design patterns in use
- Anti-pattern detection and remediation suggestions
- Machine learning-based pattern recognition

**`result_aggregator.py`** - Analysis Result Aggregator

- Aggregates results from multiple quality analyzers
- Provides unified scoring and reporting
- Consolidates analysis data into standardized formats
- Supports customizable aggregation rules and thresholds

### Root Cause Analysis (3 Analyzers)

**`error_patterns.py`** - Error Pattern Analysis

- Analyzes error logs and stack traces for patterns
- Identifies common failure modes and root causes
- Correlation analysis between errors and code changes
- Automated error categorization and prioritization

**`recent_changes.py`** - Recent Change Impact Analysis

- Analyzes git history for potential error causes
- Correlates recent changes with system failures
- Identifies high-risk changes and contributors
- Change impact assessment and blast radius analysis

**`trace_execution.py`** - Execution Trace Analysis

- Analyzes execution traces for performance and correctness
- Identifies execution paths leading to errors
- Performance bottleneck identification in traces
- Distributed tracing support for microservices

## Security Analysis Details

### OWASP Top 10 Coverage

The security analysis provides comprehensive OWASP testing criteria coverage through automated vulnerability detection using Semgrep's semantic analysis engine.

**Example with included test_codebase:**

```bash
/analyze-security
```

**Detected Issues:**

- **A01: Injection** → SQL injection in authentication (detected by Semgrep semantic analysis)
- **A02: Cryptographic Failures** → Hardcoded JWT secrets (detected by detect-secrets)
- **A03: Injection** → Command injection via eval() (detected by Semgrep patterns)
- **A07: Identity Failures** → Weak authentication patterns (detected by Semgrep rules)

## Programming Language Support

### Universal Analysis (All Languages)

**Security:** Vulnerability scanning via Semgrep, secret detection, authentication analysis
**Architecture:** Dependency analysis, coupling detection, scalability assessment
**Code Quality:** Complexity metrics via Lizard, dead code detection

### Established Tools Integration

The analysis system leverages proven, established tools rather than bespoke implementations:

| Category        | Tool                        | Languages Supported           | Analysis Type                    |
| --------------- | --------------------------- | ----------------------------- | -------------------------------- |
| **Security**    | Semgrep                     | 30+ languages                 | Semantic vulnerability detection |
| **Security**    | detect-secrets              | All text files                | Hardcoded secrets detection      |
| **Quality**     | Lizard                      | 20+ languages                 | Complexity analysis              |
| **Performance** | Language-specific profilers | Python, JS/TS, Java, Go, Rust | Performance profiling            |
| **SQL**         | SQLGlot                     | All SQL dialects              | SQL quality and performance      |
| **Frontend**    | ESLint ecosystem            | JavaScript, TypeScript        | Performance and quality          |

### Language-Specific Analysis

**Supported Languages:** Python, JavaScript, TypeScript, Java, C#, Go, Rust, PHP, Ruby, C/C++, Swift, Kotlin, SQL, and more

| Language            | Test Coverage            | Performance Baseline          | Import Analysis         | Bottleneck Detection    |
| ------------------- | ------------------------ | ----------------------------- | ----------------------- | ----------------------- |
| **Python**          | ✅ pytest, coverage      | ✅ cProfile, memory-profiler  | ✅ import patterns      | ✅ AST analysis         |
| **JavaScript**      | ✅ jest, nyc, c8         | ✅ npm scripts, profiling     | ✅ import/require       | ✅ performance patterns |
| **TypeScript**      | ✅ jest, nyc, c8         | ✅ npm scripts, profiling     | ✅ import patterns      | ✅ performance patterns |
| **Java**            | ✅ junit, jacoco         | ✅ maven/gradle, JFR          | ✅ import statements    | ✅ performance patterns |
| **Go**              | ✅ go test, coverage     | ✅ go build, benchmarks       | ✅ import patterns      | ✅ performance patterns |
| **Rust**            | ✅ cargo test, tarpaulin | ✅ cargo bench, flamegraph    | ✅ use statements       | ✅ performance patterns |
| **C#**              | ✅ dotnet test, coverlet | ✅ dotnet build, profiling    | ✅ using statements     | ✅ performance patterns |
| **SQL**             | ✅ SQLGlot parsing       | ✅ Query performance analysis | ✅ Schema dependencies  | ✅ Query optimization   |
| **Other Languages** | ✅ Framework detection   | ✅ Language-specific patterns | ✅ Full import analysis | ✅ Performance patterns |
