#!/usr/bin/env python3

import core.base.registry_bootstrap  # noqa: F401 - side-effect imports register analyzers
from core.base import AnalyzerRegistry


def test_bootstrap_registers_some_analyzers():
    # Spot-check a few keys across categories
    for key in [
        "security:detect_secrets",
        "security:semgrep",
        "security:osv",
        "quality:lizard",
        "architecture:dependency",
        "performance:frontend",
        "performance:golangci-lint",
        "performance:clippy",
        "performance:dotnet",
        "root_cause:error_patterns",
    ]:
        cls = AnalyzerRegistry.get(key)
        assert cls is not None
