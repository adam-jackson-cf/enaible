"""Tests for prompt utilities."""

from __future__ import annotations

from enaible.prompts.utils import extract_variables


def test_extract_variables_parses_table_and_strips_section() -> None:
    markdown = """Intro text

## Variables
| Token | Type | Description |
| ----- | ---- | ----------- |
| `@TARGET_PATH` | positional #1 (REQUIRED) | Path to analyze. |
| `@VERBOSE` | flag --verbose (OPTIONAL) | Enable verbose output. |

## Remaining
Body continues.
"""

    variables, body = extract_variables(markdown)

    assert [var.token for var in variables] == ["@TARGET_PATH", "@VERBOSE"]
    assert variables[0].kind == "positional"
    assert variables[0].required is True
    assert variables[0].positional_index == 1
    assert variables[1].kind == "flag"
    assert variables[1].flag_name == "--verbose"
    assert "## Variables" in body
    assert "### Required" in body
    assert "## Remaining" in body
