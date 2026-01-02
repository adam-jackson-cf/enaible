#!/usr/bin/env python3
"""Unit tests for C# dependency parsing in DependencyAnalyzer."""

from pathlib import Path

from analyzers.architecture.dependency_analysis import DependencyAnalyzer

_FIXTURE_ROOT = (
    Path(__file__).resolve().parents[1]
    / "fixture"
    / "test_codebase"
    / "vulnerable-apps"
    / "test-csharp"
)


def test_parse_csproj_dependencies():
    analyzer = DependencyAnalyzer()
    deps = analyzer._parse_csproj(_FIXTURE_ROOT / "VulnerableWebApp.csproj")

    assert deps["Microsoft.EntityFrameworkCore.SqlServer"] == "6.0.0"
    assert deps["Newtonsoft.Json"] == "13.0.1"


def test_parse_packages_config_dependencies():
    analyzer = DependencyAnalyzer()
    deps = analyzer._parse_packages_config(_FIXTURE_ROOT / "packages.config")

    assert deps["Serilog"] == "2.12.0"
    assert deps["Dapper"] == "2.1.38"


def test_parse_directory_packages_props_dependencies():
    analyzer = DependencyAnalyzer()
    deps = analyzer._parse_directory_packages_props(
        _FIXTURE_ROOT / "Directory.Packages.props"
    )

    assert deps["NUnit"] == "3.14.0"
    assert deps["FluentAssertions"] == "6.12.0"
