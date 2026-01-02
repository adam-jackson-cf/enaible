#!/usr/bin/env python3
"""Unit tests for Dotnet performance analyzer parsing."""

from pathlib import Path

from analyzers.performance.dotnet_analyzer import DotnetPerformanceAnalyzer


def test_parse_build_output_filters_perf_rules():
    analyzer = DotnetPerformanceAnalyzer()
    output = (
        "Program.cs(10,17): warning CA1822: Mark members as static [MyApp.csproj]\n"
        "Program.cs(12,5): warning CA2000: Dispose objects before losing scope [MyApp.csproj]"
    )

    findings = analyzer._parse_build_output(output, Path("MyApp.csproj"))

    assert len(findings) == 1
    assert findings[0]["title"] == "Dotnet Analyzer: CA1822"
    assert findings[0]["line_number"] == 10
