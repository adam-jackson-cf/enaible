"""Skill catalog metadata for Enaible render pipeline."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SystemSkillConfig:
    template: str
    output_path: Path


@dataclass(frozen=True)
class SkillDefinition:
    skill_id: str
    source_path: Path
    systems: Mapping[str, SystemSkillConfig]


def _repo_path(*parts: str) -> Path:
    return Path(*parts)


CATALOG: dict[str, SkillDefinition] = {
    "codify-pr-reviews": SkillDefinition(
        skill_id="codify-pr-reviews",
        source_path=_repo_path("shared", "skills", "codify-pr-reviews", "SKILL.md"),
        systems={
            "claude-code": SystemSkillConfig(
                template="docs/system/claude-code/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "skills",
                    "codify-pr-reviews",
                    "SKILL.md",
                ),
            ),
            "codex": SystemSkillConfig(
                template="docs/system/codex/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "skills",
                    "codify-pr-reviews",
                    "SKILL.md",
                ),
            ),
        },
    )
}
