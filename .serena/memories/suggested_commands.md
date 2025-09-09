# Essential Development Commands

## Testing Commands

### Unit Tests

```bash
# Run unit tests with coverage (recommended)
PYTHONPATH=shared pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
  --cov=core.base.analyzer_registry \
  --cov=core.base.validation_rules \
  --cov=core.config.loader \
  --cov=core.utils.architectural_pattern_detector \
  --cov=core.utils.tech_stack_detector \
  --cov-report=term-missing \
  --cov-fail-under=85

# Quick unit tests without coverage
PYTHONPATH=shared pytest shared/tests/unit/

# Run specific test file
PYTHONPATH=shared pytest shared/tests/unit/test_analyzer_registry.py -v
```

### Integration Tests

```bash
# Run integration tests
PYTHONPATH=shared pytest shared/tests/integration/

# Run all tests
PYTHONPATH=shared pytest shared/tests/
```

## Code Quality and Formatting

### Linting

```bash
# Ruff linting (primary linter)
ruff check . --config shared/config/formatters/ruff.toml

# Fix automatically fixable issues
ruff check . --fix --config shared/config/formatters/ruff.toml
```

### Type Checking

```bash
# MyPy type checking
PYTHONPATH=shared mypy --config-file mypy.ini
```

### Code Formatting

```bash
# Black formatting (via pre-commit)
black shared/

# Ruff formatting
ruff format . --config shared/config/formatters/ruff.toml
```

### Complexity Analysis

```bash
# Radon complexity metrics
radon cc shared/ -a -nc

# Xenon complexity gate (currently disabled in CI)
xenon --max-absolute B --max-modules A --max-average A shared
```

## Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run black --all-files
pre-commit run mypy --all-files
```

## Installation and Setup

### Python Environment

```bash
# Set Python version (pyenv)
pyenv local 3.11

# Install development dependencies
pip install -r requirements-dev.txt

# Install shared package dependencies
pip install -r shared/setup/requirements.txt
```

### Claude Code CLI

```bash
# Install Claude Code CLI (Linux/macOS)
./claude-code/install.sh

# Install Claude Code CLI (Windows PowerShell)
./claude-code/install.ps1
```

## Analysis Tools (Direct Execution)

### Security Analysis

```bash
# Run security analyzers
python shared/analyzers/security/bandit_analyzer.py <target_path>
python shared/analyzers/security/semgrep_analyzer.py <target_path>
python shared/analyzers/security/secrets_analyzer.py <target_path>
```

### Quality Analysis

```bash
# Run quality analyzers
python shared/analyzers/quality/complexity_analyzer.py <target_path>
python shared/analyzers/quality/duplication_analyzer.py <target_path>
```

### All Analyzers

```bash
# Run comprehensive analysis
PYTHONPATH=shared python shared/integration/cli/run_all_analyzers.py <target_path>
```

## Git and Version Control

```bash
# Standard git commands (Darwin/macOS)
git status
git add .
git commit -m "message"
git push origin main

# Check pre-commit hook status
git log --oneline -5
```

## File System Operations (Darwin/macOS)

```bash
# List directory contents
ls -la
find . -name "*.py" -type f
grep -r "pattern" shared/

# Directory navigation
cd shared/tests/
pwd
```

## Environment Variables

```bash
# Set Python path for imports
export PYTHONPATH=shared

# Skip external tools in testing
export NO_EXTERNAL=true

# Check Python version
python --version
which python
```

## CI/CD Commands (Local Testing)

```bash
# Simulate CI pipeline locally
PYTHONPATH=shared pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 --cov-fail-under=85
ruff check . --config shared/config/formatters/ruff.toml
PYTHONPATH=shared mypy --config-file mypy.ini
```
