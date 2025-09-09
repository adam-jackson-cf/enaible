# Tech Stack Breakdown

## Core Languages

- **Python 3.11+** (primary language, specified in .python-version)
- **JavaScript/TypeScript** (frontend analysis and Node.js tools)
- **Bash/Shell** (installation scripts and automation)
- **SQL** (SQLFluff for SQL analysis)

## Python Development Stack

### Core Dependencies

- **python-dotenv**: Environment variable management
- **requests**: HTTP requests for external APIs
- **pathlib2**: Path handling for older Python versions
- **pyyaml**: YAML configuration parsing
- **jinja2**: Template rendering for dynamic commands
- **click**: CLI framework for command processing
- **rich**: Rich terminal output and progress bars

### Security Analysis Tools

- **bandit**: Python security linting
- **safety**: Vulnerability scanning
- **semgrep**: Semantic static analysis security scanner
- **detect-secrets**: Hardcoded secrets detection
- **sqlfluff**: SQL linting and security analysis

### Performance Analysis Tools

- **psutil**: System and process utilities
- **memory-profiler**: Memory usage profiling
- **py-spy**: Python profiler (Unix only)
- **perflint**: Performance anti-pattern detection
- **flake8-comprehensions**: List/dict comprehension performance rules
- **flake8-bugbear**: Bug and performance issue detection

### Code Quality Analysis

- **flake8**: Style guide enforcement
- **pylint**: Code analysis
- **radon**: Complexity metrics
- **lizard**: Advanced complexity analysis
- **vulture**: Dead code finder
- **mccabe**: Complexity checker

### Architecture Analysis

- **pydeps**: Dependency analysis
- **networkx**: Graph analysis for dependencies

### Development Tools

- **pytest**: Testing framework
- **pytest-cov**: Coverage testing
- **pytest-timeout**: Test timeout handling
- **pytest-xdist**: Parallel test execution
- **black**: Code formatting
- **isort**: Import sorting
- **ruff**: Modern Python linter and formatter
- **mypy**: Static type checking

## Frontend/JavaScript Stack

- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Karma**: JavaScript test runner (mentioned in project docs)
- **Jasmine**: JavaScript testing framework

## Cross-Platform Support

- **platformdirs**: Cross-platform directory detection
- **filelock**: File-based locking for task coordination
- **watchdog**: File system monitoring

## CI/CD and Quality Gates

- **GitHub Actions**: Automated CI/CD workflows
- **Pre-commit hooks**: Quality gates before commits
- **xenon**: Complexity analysis (currently disabled in CI)

## Build and Package Management

- **pip**: Python package management
- **npm/yarn**: JavaScript package management (for frontend analysis)
- **pyproject.toml**: Not used (requirements.txt approach)

## Development Environment

- **Python 3.11** (specified in pyproject, .python-version, and CI)
- **Cross-platform**: Linux, macOS, Windows support
- **Virtual environments**: Standard Python venv approach
