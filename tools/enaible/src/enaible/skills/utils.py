"""Helpers for skill parsing and validation."""

from __future__ import annotations

import re

_FRONTMATTER_DELIM = "---"
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class SkillFormatError(ValueError):
    """Raised when a skill source file is malformed."""


def split_frontmatter(content: str) -> tuple[str, str]:
    """Return (frontmatter_text, body_text)."""
    if not content.startswith(_FRONTMATTER_DELIM):
        raise SkillFormatError("SKILL.md must start with YAML frontmatter.")

    lines = content.splitlines()
    if not lines or lines[0].strip() != _FRONTMATTER_DELIM:
        raise SkillFormatError("SKILL.md frontmatter must start with '---'.")

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == _FRONTMATTER_DELIM:
            end_idx = idx
            break

    if end_idx is None:
        raise SkillFormatError("SKILL.md frontmatter missing closing '---'.")

    frontmatter = "\n".join(lines[: end_idx + 1]).rstrip() + "\n"
    body = "\n".join(lines[end_idx + 1 :])
    return frontmatter, body.lstrip("\n")


def parse_simple_frontmatter(frontmatter: str) -> dict[str, str]:
    """Parse top-level key: value pairs from frontmatter."""
    fields: dict[str, str] = {}
    lines = frontmatter.splitlines()
    for line in lines[1:-1]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            fields[key] = value
    return fields


def validate_skill_metadata(fields: dict[str, str], skill_id: str) -> None:
    """Validate required frontmatter fields."""
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()

    if not name:
        raise SkillFormatError("SKILL.md frontmatter must include 'name'.")
    if not _NAME_RE.match(name) or len(name) > 64:
        raise SkillFormatError(
            "Skill name must be 1-64 chars, lowercase alphanumerics and hyphens only."
        )
    if name != skill_id:
        raise SkillFormatError(
            f"Skill name '{name}' must match directory name '{skill_id}'."
        )
    if not description:
        raise SkillFormatError("SKILL.md frontmatter must include 'description'.")
    if len(description) > 1024:
        raise SkillFormatError("Skill description must be <= 1024 characters.")
