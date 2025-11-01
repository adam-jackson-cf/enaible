"""Utilities for parsing shared prompt metadata.

Supports the unified bullet-style Variables section using @TOKENS.

Format:

## Variables

### Required
- @TARGET_PATH = $1 — description

### Optional (derived from $ARGUMENTS)
- @MIN_SEVERITY = --min-severity
- @EXCLUDE = --exclude [repeatable]

### Derived (internal)
- @MAX_CHARS = 150000
"""

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
    repeatable: bool = False


_VARIABLE_HEADER_PATTERN = re.compile(
    r"^\|\s*Token(?:/Flag)?\s*\|\s*Type\s*\|\s*Description\s*\|$",
    re.IGNORECASE,
)

_H2_HEADING = re.compile(r"^##\s+variables\s*$", re.IGNORECASE)
_H3_REQUIRED = re.compile(r"^###\s+required\s*$", re.IGNORECASE)
_H3_OPTIONAL = re.compile(r"^###\s+optional(\s*\(.*\))?\s*$", re.IGNORECASE)
_H3_DERIVED = re.compile(r"^###\s+derived(\s*\(.*\))?\s*$", re.IGNORECASE)
_BULLET = re.compile(r"^[-*]\s+(.+?)\s*$")
_TOKEN_RE = re.compile(r"@([A-Z][A-Z0-9_]*)$")
_MAPPING_SPLIT = re.compile(r"\s*=\s*")
_POS_VALUE = re.compile(r"^\$(\d+)\s*(?:\[.*?\])?$")
_FLAG_VALUE = re.compile(r"^(--[a-z0-9][a-z0-9-]*)\s*(?:\[.*?\])?$", re.IGNORECASE)


def extract_variables(markdown: str) -> tuple[list[VariableSpec], str]:
    """Extract variable definitions from a markdown prompt body.

    Returns a tuple of (variables, body_without_variables_section).
    Prefers the bullet-style parser; tables are only supported when they use @TOKENS.
    """
    lines = markdown.splitlines()
    variables: list[VariableSpec] = []
    new_lines: list[str] = []

    i = 0
    while i < len(lines):
        if _H2_HEADING.match(lines[i]):
            block: list[str] = []
            while i < len(lines):
                block.append(lines[i])
                i += 1
                if i < len(lines) and lines[i].startswith("## "):
                    break

            formatted_block: list[str] | None = None
            parsed = _parse_variables_bullets(block[1:])
            if parsed:
                variables = parsed
                formatted_block = _format_variables_block(parsed)
            else:
                table_lines = [ln for ln in block if ln.strip().startswith("|")]
                if table_lines:
                    variables = _parse_variables_table(table_lines)
                    formatted_block = _format_variables_block(variables)

            if formatted_block:
                new_lines.extend(formatted_block)
            else:
                new_lines.extend(block)
            continue

        new_lines.append(lines[i])
        i += 1

    body = "\n".join(new_lines).strip("\n")
    return variables, body + "\n" if body else ""


def _format_variables_block(variables: list[VariableSpec]) -> list[str]:
    required = [var for var in variables if var.kind == "positional"]
    optional = [var for var in variables if var.kind in {"flag", "named"}]
    derived = [var for var in variables if var.kind == "derived"]

    lines: list[str] = ["## Variables", ""]

    if required:
        lines.append("### Required")
        lines.append("")
        for var in required:
            desc = f" — {var.description}" if var.description else ""
            lines.append(f"- {var.token} = ${var.positional_index}{desc}")
        lines.append("")

    if optional:
        lines.append("### Optional (derived from @ARGUMENTS)")
        lines.append("")
        for var in optional:
            repeatable = " [repeatable]" if var.repeatable else ""
            desc = f" — {var.description}" if var.description else ""
            lines.append(f"- {var.token} = {var.flag_name}{repeatable}{desc}")
        lines.append("")

    if derived:
        lines.append("### Derived (internal)")
        lines.append("")
        for var in derived:
            detail = var.description or var.type_text.strip()
            suffix = f" — {detail}" if detail else ""
            lines.append(f"- {var.token}{suffix}")
        lines.append("")

    return lines


def _parse_variables_table(table_lines: Iterable[str]) -> list[VariableSpec]:
    """Parse legacy markdown table lines into VariableSpec entries.

    Only @TOKENS are allowed. $-prefixed tokens are rejected by design.
    """
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
        if not token_text.startswith("@"):
            raise ValueError(
                f"Variable token must start with '@' in tables: {token_text}"
            )

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
                repeatable="repeatable" in type_text.lower(),
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


def _parse_variables_bullets(block_lines: Iterable[str]) -> list[VariableSpec]:
    section = None  # 'required' | 'optional' | 'derived'
    variables: list[VariableSpec] = []
    positional_seen: set[int] = set()

    for raw in block_lines:
        line = raw.strip()
        if not line:
            continue
        if _H3_REQUIRED.match(line):
            section = "required"
            continue
        if _H3_OPTIONAL.match(line):
            section = "optional"
            continue
        if _H3_DERIVED.match(line):
            section = "derived"
            continue

        m = _BULLET.match(line)
        if not m or section is None:
            continue
        content = m.group(1)

        # Split description if provided using em dash or hyphen dash separation
        desc_split = re.split(r"\s+—\s+|\s+-\s+", content, maxsplit=1)
        mapping_part = desc_split[0].strip()
        description = desc_split[1].strip() if len(desc_split) > 1 else ""

        parts = _MAPPING_SPLIT.split(mapping_part)
        if len(parts) != 2:
            continue
        token_part, value_part = parts[0].strip(), parts[1].strip()

        tok_match = _TOKEN_RE.match(token_part)
        if not tok_match:
            raise ValueError(
                f"Invalid token '{token_part}'. Tokens must be @UPPER_SNAKE_CASE."
            )
        token = f"@{tok_match.group(1)}"

        repeatable = "[repeatable]" in value_part.lower()

        kind = "derived"
        required = section == "required"
        positional_index: int | None = None
        flag_name: str | None = None
        type_text: str

        if section == "required":
            pos_m = _POS_VALUE.match(value_part)
            if not pos_m:
                raise ValueError(
                    f"Required variable '{token}' must map to $N (e.g., $1)."
                )
            positional_index = int(pos_m.group(1))
            if positional_index in positional_seen:
                raise ValueError(
                    f"Duplicate positional index ${positional_index} for {token}."
                )
            positional_seen.add(positional_index)
            kind = "positional"
            type_text = f"positional ${positional_index} (REQUIRED)"
        elif section == "optional":
            flag_m = _FLAG_VALUE.match(value_part)
            if not flag_m:
                raise ValueError(f"Optional variable '{token}' must map to a --flag.")
            flag_name = flag_m.group(1)
            kind = "flag"
            repeatable_text = ", repeatable" if repeatable else ""
            type_text = (
                f"derived from @ARGUMENTS ({flag_name}) (optional{repeatable_text})"
            )
        else:  # derived internal
            kind = "derived"
            type_text = "derived (internal)"

        variables.append(
            VariableSpec(
                token=token,
                type_text=type_text,
                description=description,
                kind=kind,
                required=required,
                flag_name=flag_name,
                positional_index=positional_index,
                repeatable=repeatable,
            )
        )

    return variables
