# Testing Framework and Approach

## Testing Framework

- **Primary**: pytest (version 7.4+)
- **Coverage**: pytest-cov (version 4.1+) with 85% coverage requirement
- **Parallel Execution**: pytest-xdist for parallel test runs
- **Timeouts**: pytest-timeout for test timeout handling

## Test Organization

### Directory Structure

```
shared/tests/
├── conftest.py          # Global pytest configuration
├── unit/                # Unit tests for core components
│   ├── test_analyzer_registry.py
│   ├── test_config_loader.py
│   ├── test_duplicate_detection.py
│   ├── test_tech_stack_detector_core.py
│   ├── test_architectural_pattern_detector_*.py
│   └── test_validation_rules.py
├── integration/         # Integration and E2E tests
│   ├── test_integration_all_analyzers.py
│   ├── test_integration_security_cli.py
│   ├── test_integration_root_cause_cli.py
│   ├── security_expected_findings.json
│   └── test_powershell_installer.ps1
└── utils/
    └── builders.py      # Test utilities and builders
```

### Test Configuration

- **Global conftest.py**: Ensures 'shared' is on sys.path for imports
- **Session fixtures**: Provides config paths for patterns and tech stacks
- **Environment setup**: PYTHONPATH=shared for test execution

## Test Execution Commands

### Unit Tests

```bash
# Run unit tests with coverage (CI approach)
PYTHONPATH=shared pytest -q shared/tests/unit -n auto --dist=loadfile --timeout=60 \
  --cov=core.base.analyzer_registry \
  --cov=core.base.validation_rules \
  --cov=core.config.loader \
  --cov=core.utils.architectural_pattern_detector \
  --cov=core.utils.tech_stack_detector \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### Integration Tests

```bash
# Run integration tests
PYTHONPATH=shared pytest shared/tests/integration/
```

### All Tests

```bash
# Run all tests
PYTHONPATH=shared pytest shared/tests/
```

## Test Categories

### Unit Tests

- **Analyzer Registry**: Core analyzer registration and discovery
- **Config Loader**: Configuration file loading and validation
- **Validation Rules**: Input validation and error handling
- **Architectural Pattern Detector**: Pattern recognition algorithms
- **Tech Stack Detector**: Technology identification logic
- **Duplicate Detection**: Code duplication analysis

### Integration Tests

- **All Analyzers CLI**: Smoke test for the complete analysis pipeline
- **Security CLI**: End-to-end security analysis workflow
- **Root Cause CLI**: Error analysis and debugging workflows
- **PowerShell Installer**: Cross-platform installation testing

## Creating New Tests

### Unit Test Template

```python
#!/usr/bin/env python3
"""Test module for [component name]."""

import pytest
from pathlib import Path

# Import the module under test
from core.module_name import ClassName

def test_component_functionality():
    """Test basic functionality."""
    # Arrange
    component = ClassName()

    # Act
    result = component.method()

    # Assert
    assert result.is_valid
    assert result.data is not None

@pytest.fixture
def sample_data():
    """Provide test data."""
    return {"key": "value"}
```

### Integration Test Template

```python
#!/usr/bin/env python3
"""Integration test for [workflow name]."""

import os
from pathlib import Path

def test_workflow_integration():
    """Test end-to-end workflow."""
    # Skip external dependencies in CI
    os.environ["NO_EXTERNAL"] = "true"

    from integration.cli.workflow_runner import WorkflowRunner

    target = str(Path("test_codebase").resolve())
    runner = WorkflowRunner()
    result = runner.execute(target_path=target)

    assert result["success"] is True
```

## Test Data and Fixtures

- **Test Codebase**: Controlled applications in test_codebase/ for validation
- **Expected Results**: JSON files with expected findings (security_expected_findings.json)
- **Session Fixtures**: Config paths and shared resources
- **Environment Variables**: NO_EXTERNAL=true to skip external tools in CI

## Coverage Requirements

- **Minimum Coverage**: 85% (enforced in CI)
- **Coverage Targets**: Core modules only (base analyzers, config, utils)
- **Coverage Report**: term-missing format shows uncovered lines
- **Coverage Files**: Specific modules listed in CI configuration
