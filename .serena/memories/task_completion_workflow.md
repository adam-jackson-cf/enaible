# Task Completion Workflow

## Quality Gates (Must Pass)

### 1. Unit Tests with Coverage

```bash
PYTHONPATH=shared pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
  --cov=core.base.analyzer_registry \
  --cov=core.base.validation_rules \
  --cov=core.config.loader \
  --cov=core.utils.architectural_pattern_detector \
  --cov=core.utils.tech_stack_detector \
  --cov-report=term-missing \
  --cov-fail-under=85
```

**Requirement**: 85% minimum coverage on core modules

### 2. Code Linting

```bash
ruff check . --config shared/config/formatters/ruff.toml
```

**Requirement**: No linting errors (warnings acceptable with justification)

### 3. Type Checking

```bash
PYTHONPATH=shared mypy --config-file mypy.ini
```

**Requirement**: No type checking errors in covered modules

### 4. Integration Tests (if applicable)

```bash
PYTHONPATH=shared pytest shared/tests/integration/
```

**Requirement**: All integration tests pass

## Pre-commit Hook Validation

### Automatic Validation

```bash
# Run all pre-commit hooks
pre-commit run --all-files
```

### Manual Validation Steps

1. **Trailing Whitespace**: Automatically removed
2. **File Endings**: Newline at EOF enforced
3. **JSON/YAML**: Syntax validation passes
4. **Python Syntax**: AST validation passes
5. **Docstring Position**: Correctly placed

## Code Quality Checklist

### Before Committing

- [ ] All tests pass locally
- [ ] Code coverage meets 85% threshold
- [ ] No linting errors from Ruff
- [ ] MyPy type checking passes (if applicable)
- [ ] Pre-commit hooks pass
- [ ] Code follows naming conventions
- [ ] Functions/classes have appropriate docstrings
- [ ] Import statements properly organized

### Code Review Preparation

- [ ] Meaningful commit messages
- [ ] Changes are focused and atomic
- [ ] No commented-out code or debug statements
- [ ] No hardcoded values or secrets
- [ ] Error handling appropriate for context
- [ ] Performance considerations addressed

## Continuous Integration Alignment

### CI Pipeline Commands (for local validation)

```bash
# Exactly match CI pipeline locally
PYTHONPATH=shared pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 --cov-fail-under=85
ruff check . --config shared/config/formatters/ruff.toml
PYTHONPATH=shared mypy --config-file mypy.ini
```

### Environment Setup

```bash
# Ensure Python 3.11
python --version  # Should show 3.11.x

# Install exact dev dependencies
pip install -r requirements-dev.txt

# Set Python path
export PYTHONPATH=shared
```

## Common Issues and Solutions

### Import Errors

- **Problem**: Module not found errors in tests
- **Solution**: Ensure `PYTHONPATH=shared` is set
- **Verification**: Check `conftest.py` files are present

### Coverage Failures

- **Problem**: Coverage below 85%
- **Solution**: Add tests for uncovered lines (use --cov-report=term-missing)
- **Note**: Only core modules require coverage

### Type Checking Failures

- **Problem**: MyPy errors
- **Solution**: Add type hints or use type: ignore comments sparingly
- **Scope**: Limited to specific modules in mypy.ini

### Linting Failures

- **Problem**: Ruff errors
- **Solution**: Use `ruff check --fix` for auto-fixable issues
- **Manual**: Address remaining issues following style guide

## Performance Validation

### Complexity Gates (Currently Disabled)

```bash
# When re-enabled, should pass:
xenon --max-absolute B --max-modules A --max-average A shared
```

### Performance Testing

- Integration tests should complete within timeout limits
- Memory usage should be reasonable for target systems
- No obvious performance regressions

## Documentation Requirements

### Code Documentation

- Public functions require docstrings (NumPy style)
- Complex algorithms need explanatory comments
- Configuration changes need documentation updates

### Change Documentation

- Update relevant README sections if behavior changes
- Document new dependencies or requirements
- Update installation instructions if needed

## Final Checklist

- [ ] All quality gates pass locally
- [ ] Pre-commit hooks configured and passing
- [ ] CI pipeline commands execute successfully
- [ ] Code follows project conventions
- [ ] Tests provide adequate coverage
- [ ] Documentation updated if necessary
- [ ] No security vulnerabilities introduced
- [ ] Performance impact considered
