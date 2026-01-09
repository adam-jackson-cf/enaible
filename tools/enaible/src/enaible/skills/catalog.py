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
                template="docs/reference/system/claude-code/templates/skill.md.j2",
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
                template="docs/reference/system/codex/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "skills",
                    "codify-pr-reviews",
                    "SKILL.md",
                ),
            ),
            "copilot": SystemSkillConfig(
                template="docs/reference/system/copilot/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "skills",
                    "codify-pr-reviews",
                    "SKILL.md",
                ),
            ),
            "pi": SystemSkillConfig(
                template="docs/reference/system/pi/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "pi",
                    "skills",
                    "codify-pr-reviews",
                    "SKILL.md",
                ),
            ),
        },
    ),
    "docs-scraper": SkillDefinition(
        skill_id="docs-scraper",
        source_path=_repo_path("shared", "skills", "docs-scraper", "SKILL.md"),
        systems={
            "claude-code": SystemSkillConfig(
                template="docs/reference/system/claude-code/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "skills",
                    "docs-scraper",
                    "SKILL.md",
                ),
            ),
            "codex": SystemSkillConfig(
                template="docs/reference/system/codex/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "skills",
                    "docs-scraper",
                    "SKILL.md",
                ),
            ),
            "copilot": SystemSkillConfig(
                template="docs/reference/system/copilot/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "skills",
                    "docs-scraper",
                    "SKILL.md",
                ),
            ),
            "pi": SystemSkillConfig(
                template="docs/reference/system/pi/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "pi",
                    "skills",
                    "docs-scraper",
                    "SKILL.md",
                ),
            ),
        },
    ),
    "research": SkillDefinition(
        skill_id="research",
        source_path=_repo_path("shared", "skills", "research", "SKILL.md"),
        systems={
            "claude-code": SystemSkillConfig(
                template="docs/reference/system/claude-code/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "claude-code",
                    "skills",
                    "research",
                    "SKILL.md",
                ),
            ),
            "codex": SystemSkillConfig(
                template="docs/reference/system/codex/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "codex",
                    "skills",
                    "research",
                    "SKILL.md",
                ),
            ),
            "copilot": SystemSkillConfig(
                template="docs/reference/system/copilot/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "copilot",
                    "skills",
                    "research",
                    "SKILL.md",
                ),
            ),
            "pi": SystemSkillConfig(
                template="docs/reference/system/pi/templates/skill.md.j2",
                output_path=_repo_path(
                    ".build",
                    "rendered",
                    "pi",
                    "skills",
                    "research",
                    "SKILL.md",
                ),
            ),
        },
    ),
}
