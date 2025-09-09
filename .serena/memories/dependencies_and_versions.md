# Key Dependencies and Versions

## Core Python Dependencies

### Development Tools (requirements-dev.txt)

- **pytest**: >=7.4 (testing framework)
- **pytest-cov**: >=4.1 (coverage testing)
- **pytest-timeout**: >=2.3 (test timeout handling)
- **pytest-xdist**: >=3.6 (parallel test execution)
- **radon**: >=6.0 (complexity metrics)
- **xenon**: >=0.9 (complexity gate - currently disabled)
- **ruff**: >=0.5 (modern linter and formatter)
- **mypy**: >=1.10 (static type checking)

### Production Dependencies (shared/setup/requirements.txt)

#### Foundation Layer

- **python-dotenv**: >=0.19.0 (environment management)
- **requests**: >=2.25.0 (HTTP requests)
- **click**: >=8.0.0 (CLI framework)
- **rich**: >=12.0.0 (terminal output)
- **pyyaml**: >=6.0 (YAML parsing)
- **jinja2**: >=3.0.0 (template rendering)
- **typing-extensions**: >=4.0.0 (enhanced type hints)

#### Security Analysis Stack

- **bandit**: >=1.7.0 (Python security linting)
- **safety**: >=2.0.0 (vulnerability scanning)
- **semgrep**: >=1.45.0 (semantic security analysis)
- **detect-secrets**: >=1.4.0 (secrets detection)
- **sqlfluff**: >=2.3.0 (SQL security analysis)

#### Performance Analysis Stack

- **psutil**: >=5.8.0 (system utilities)
- **memory-profiler**: >=0.60.0 (memory profiling)
- **py-spy**: >=0.3.0 (Python profiler, Unix only)
- **perflint**: >=0.7.0 (performance anti-patterns)
- **flake8-comprehensions**: >=3.10.0 (performance rules)
- **flake8-bugbear**: >=23.3.0 (bug detection)

#### Code Quality Stack

- **flake8**: >=4.0.0 (style enforcement)
- **pylint**: >=2.12.0 (code analysis)
- **radon**: >=5.1.0 (complexity metrics)
- **lizard**: >=1.17.0 (advanced complexity)
- **vulture**: >=2.3 (dead code detection)
- **mccabe**: >=0.6.0 (complexity checker)

#### Architecture Analysis

- **pydeps**: >=1.10.0 (dependency analysis)
- **networkx**: >=2.6.0 (graph analysis)

#### Development Support

- **pytest**: >=6.2.0 (testing framework)
- **pytest-cov**: >=3.0.0 (coverage)
- **black**: >=22.0.0 (code formatting)
- **isort**: >=5.10.0 (import sorting)

#### Cross-Platform Support

- **platformdirs**: >=2.5.0 (directory detection)
- **filelock**: >=3.8.0 (file locking)
- **watchdog**: >=2.1.0 (file monitoring)

## Pre-commit Hook Versions

- **pre-commit-hooks**: v4.5.0
- **pyupgrade**: v3.15.0 (Python syntax modernization)
- **black**: 23.12.1 (code formatting)
- **ruff-pre-commit**: v0.6.2 (linting)
- **mypy**: v1.10.0 (type checking)
- **prettier**: v3.1.0 (JS/TS formatting)
- **eslint**: v8.56.0 (JS/TS linting)

## JavaScript/Node.js Dependencies (Optional)

These are installed separately via npm/yarn for frontend analysis:

- **eslint**: JavaScript/TypeScript linting
- **lighthouse**: Performance auditing
- **webpack-bundle-analyzer**: Bundle analysis

## Python Version Requirements

- **Target Version**: Python 3.11+ (specified in multiple configs)
- **Minimum Version**: Python 3.7+ (for backward compatibility in some tools)
- **pyenv Configuration**: .python-version specifies 3.11

## Version Management Strategy

- **Semantic Versioning**: All dependencies use semantic version constraints
- **Minimum Versions**: Specified with >= to allow updates
- **Stability**: Established, mature tools preferred over experimental ones
- **Security**: Regular updates for security-related dependencies
- **Compatibility**: Cross-platform support prioritized

## Critical Version Notes

- **py-spy**: Unix only (excluded on Windows)
- **pathlib2**: Only for Python <3.4 (backward compatibility)
- **shutil-backports**: Only for Python <3.8
- **subprocess32**: Only for Python <3.2
- **dataclasses**: Only for Python <3.7

## Upgrade Path

- **Python 3.11+**: Required for modern syntax features
- **pyupgrade**: Automatically modernizes code to Python 3.11+ syntax
- **ruff**: Modern replacement for multiple legacy tools
- **pytest**: Latest versions for improved performance and features
