# Code Style and Conventions

## Python Style Guidelines

### Formatting Standards

- **Line Length**: 88 characters (Black/Ruff standard)
- **Target Version**: Python 3.9+ syntax (pyupgrade --py311-plus in pre-commit)
- **Quote Style**: Double quotes preferred
- **Indentation**: 4 spaces (no tabs)
- **Line Endings**: Auto-detected by formatters

### Code Formatting Tools

- **Primary Formatter**: Black (version 23.12.1)
- **Secondary**: Ruff format (modern alternative)
- **Import Sorting**: isort (integrated with Ruff)
- **Automatic Fixing**: Ruff --fix for automatically fixable issues

### Linting Rules (Ruff Configuration)

**Enabled Rule Sets**:

- **E, W**: pycodestyle errors and warnings
- **F**: Pyflakes
- **I**: isort (import sorting)
- **B**: flake8-bugbear (bug detection)
- **C4**: flake8-comprehensions (performance)
- **UP**: pyupgrade (modern syntax)
- **SIM**: flake8-simplify
- **PT**: flake8-pytest-style
- **PGH**: pygrep-hooks
- **A**: flake8-builtins (builtin shadowing)
- **D**: pydocstyle (docstring conventions)

**Ignored Rules**:

- **E501**: Line too long (handled by formatter)
- **D100-D107**: Missing docstring rules (selectively ignored)
- **B006, B008**: Mutable/function call defaults (project-specific)

### Type Hints

- **MyPy Configuration**: Limited to core modules only
- **Target**: Python 3.11
- **Coverage**: `shared/core/base/`, `shared/core/config/`, selected utils
- **Strictness**: Moderate (allows missing imports, skips some checks)
- **Type Extensions**: typing-extensions for Python <3.9 compatibility

### Docstring Convention

- **Style**: NumPy convention (configured in Ruff)
- **Required**: Public classes and functions (with selective exceptions)
- **Format**: Triple double quotes with structured sections

## File and Directory Conventions

### Python Module Structure

```python
#!/usr/bin/env python3
"""Module docstring describing purpose.

Detailed description if needed.
"""

import standard_library
from pathlib import Path

import third_party_package
from third_party import SpecificClass

from core.module import LocalClass  # Project imports last
from .relative_module import RelativeImport
```

### Naming Conventions

- **Files**: snake_case.py
- **Classes**: PascalCase
- **Functions/Methods**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Private**: \_single_underscore prefix

### Directory Structure Patterns

- **Test Files**: `test_*.py` pattern
- **Configuration**: Centralized in `shared/config/`
- **Base Classes**: Abstract base classes in `shared/core/base/`
- **Utilities**: Helper functions in `shared/utils/` or `shared/core/utils/`

## JavaScript/TypeScript Style

### Formatting

- **Prettier**: Primary formatter (version 3.1.0)
- **ESLint**: Linting (version 8.56.0)
- **File Types**: .js, .jsx, .ts, .tsx, .json, .md, .yaml

### Configuration

- **Prettier Config**: `.prettierrc` in project root
- **ESLint**: Excludes test_codebase/ and node_modules/
- **TypeScript**: Additional ESLint dependency for TS support

## Pre-commit Hook Integration

### Automatic Checks

1. **Trailing Whitespace**: Removed automatically
2. **End of File**: Ensures newline at EOF
3. **JSON/YAML**: Syntax validation
4. **Merge Conflicts**: Detects conflict markers
5. **Python AST**: Validates Python syntax
6. **Docstring Position**: Ensures docstrings come first

### Quality Gates

- **pyupgrade**: Modernizes Python syntax to 3.11+
- **Black**: Code formatting
- **Ruff**: Linting with automatic fixes
- **MyPy**: Type checking (limited scope)
- **Prettier**: JavaScript/TypeScript formatting
- **ESLint**: JavaScript/TypeScript linting

## Error Handling Patterns

### Exception Handling

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

### Logging Standards

- **Rich**: Terminal output and progress bars
- **Structured Logging**: Consistent format across analyzers
- **Error Levels**: Appropriate severity levels

## Performance Conventions

### Code Optimization Rules

- **List Comprehensions**: Preferred over loops where readable
- **Generator Expressions**: For memory efficiency with large datasets
- **F-strings**: Preferred over % formatting or .format()
- **Pathlib**: Preferred over os.path

### Performance Linting

- **perflint**: PERF error codes for performance anti-patterns
- **flake8-comprehensions**: Optimized comprehension patterns
- **flake8-bugbear**: Performance and bug detection

## Testing Conventions

### Test Structure

```python
def test_component_behavior():
    """Test description following Given-When-Then pattern."""
    # Arrange (Given)
    component = ComponentUnderTest()

    # Act (When)
    result = component.method_under_test()

    # Assert (Then)
    assert result.expected_property
    assert result.is_valid
```

### Test File Organization

- **Unit Tests**: `shared/tests/unit/test_*.py`
- **Integration Tests**: `shared/tests/integration/test_integration_*.py`
- **Fixtures**: `conftest.py` files for shared test setup
- **Test Data**: Dedicated directories or files for test inputs
