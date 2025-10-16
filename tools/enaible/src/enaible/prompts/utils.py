"""Utilities for parsing shared prompt metadata."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class VariableSpec:
    token: str
    type_text: str
    description: str
    kind: str
    required: bool
    flag_name: str | None = None
    positional_index: int | None = None


_VARIABLE_HEADER_PATTERN = re.compile(
    r"^\|\s*Token\s*\|\s*Type\s*\|\s*Description\s*\|$", re.IGNORECASE
)


def extract_variables(markdown: str) -> tuple[list[VariableSpec], str]:
    """Extract variable definitions from a markdown prompt body.

    Returns a tuple of (variables, body_without_variables_section).
    """
    lines = markdown.splitlines()
    variables: list[VariableSpec] = []
    new_lines: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip().lower() == "## variables":
            i += 1
            # skip blank lines after heading
            while i < len(lines) and not lines[i].strip():
                i += 1

            table_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1

            if table_lines:
                variables = _parse_variables_table(table_lines)

            # skip trailing blank lines after table
            while i < len(lines) and not lines[i].strip():
                i += 1
            continue

        new_lines.append(lines[i])
        i += 1

    body = "\n".join(new_lines).strip("\n")
    return variables, body + "\n" if body else ""


def _parse_variables_table(table_lines: Iterable[str]) -> list[VariableSpec]:
    """Parse markdown table lines into VariableSpec entries."""
    rows = [row.strip() for row in table_lines if row.strip()]
    if not rows:
        return []

    header = rows[0]
    if not _VARIABLE_HEADER_PATTERN.match(header):
        raise ValueError(
            "Variables table must have columns: Token | Type | Description"
        )

    # Skip header and alignment row if present
    start_idx = 1
    if start_idx < len(rows) and set(rows[start_idx].replace(" ", "")) <= {
        "|",
        ":",
        "-",
    }:
        start_idx += 1

    variables: list[VariableSpec] = []
    positional_counter = 0

    for row in rows[start_idx:]:
        cells = [cell.strip() for cell in row.split("|")][1:-1]
        if len(cells) != 3:
            continue
        token_cell, type_text, description = cells
        token_text = token_cell.strip()
        if token_text.startswith("`") and token_text.endswith("`"):
            token_text = token_text[1:-1].strip()
        if not token_text.startswith("$"):
            raise ValueError(f"Variable token must start with '$': {token_text}")

        kind, required, positional_index, flag_name = _interpret_type_cell(
            type_text, positional_counter
        )
        if kind == "positional" and positional_index is None:
            positional_counter += 1
            positional_index = positional_counter
        elif kind == "positional" and positional_index is not None:
            positional_counter = positional_index

        variables.append(
            VariableSpec(
                token=token_text,
                type_text=type_text,
                description=description,
                kind=kind,
                required=required,
                flag_name=flag_name,
                positional_index=positional_index,
            )
        )

    return variables


_POS_INDEX_RE = re.compile(r"#(\d+)")
_FLAG_RE = re.compile(r"--[a-z0-9][a-z0-9-]*", re.IGNORECASE)


def _interpret_type_cell(
    type_cell: str, current_positional_count: int
) -> tuple[str, bool, int | None, str | None]:
    text = type_cell.strip()
    lower = text.lower()

    required = "required" in lower
    optional = "optional" in lower
    if required and optional:
        required = not optional  # default to False if conflicting
    elif not required and not optional:
        required = False

    flag_name: str | None = None
    positional_index: int | None = None

    if lower.startswith("positional"):
        kind = "positional"
        match = _POS_INDEX_RE.search(lower)
        if match:
            positional_index = int(match.group(1))
    elif lower.startswith("flag"):
        kind = "flag"
        flag_match = _FLAG_RE.search(text)
        if flag_match:
            flag_name = flag_match.group(0)
    elif lower.startswith("named"):
        kind = "named"
        flag_match = _FLAG_RE.search(text)
        if flag_match:
            flag_name = flag_match.group(0)
    else:
        kind = "config"

    return kind, required, positional_index, flag_name
