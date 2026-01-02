"""Skill rendering engine."""

from __future__ import annotations

import difflib
import shutil
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..constants import MANAGED_SENTINEL
from ..runtime.context import WorkspaceContext
from .catalog import CATALOG, SkillDefinition, SystemSkillConfig
from .utils import parse_simple_frontmatter, split_frontmatter, validate_skill_metadata


@dataclass(frozen=True)
class ResourceCopy:
    source: Path
    destination: Path


@dataclass(frozen=True)
class RenderResult:
    skill_id: str
    system: str
    content: str
    output_path: Path
    resources: Sequence[ResourceCopy]

    def write(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self.content, encoding="utf-8")

        for resource in self.resources:
            if resource.source.is_dir():
                _copy_resource_dir(resource.source, resource.destination, self.system)
            else:
                resource.destination.parent.mkdir(parents=True, exist_ok=True)
                _copy_resource_file(resource.source, resource.destination, self.system)

    def diff(self) -> str:
        if not self.output_path.exists():
            return ""
        current = self.output_path.read_text(encoding="utf-8").splitlines(keepends=True)
        updated = self.content.splitlines(keepends=True)
        diff_lines = list(
            difflib.unified_diff(
                current,
                updated,
                fromfile=str(self.output_path),
                tofile=f"{self.output_path} (generated)",
            )
        )
        return "".join(diff_lines)


class SkillRenderer:
    def __init__(self, context: WorkspaceContext):
        self.context = context
        self.env = Environment(
            loader=FileSystemLoader(str(context.repo_root)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
            undefined=StrictUndefined,
        )

    def list_skills(self) -> Sequence[SkillDefinition]:
        return list(CATALOG.values())

    def render(
        self,
        skill_ids: Iterable[str],
        systems: Iterable[str],
        output_override: dict[str, Path | None] | None = None,
    ) -> list[RenderResult]:
        results: list[RenderResult] = []
        for skill_id in skill_ids:
            definition = self._get_skill(skill_id)
            for system in systems:
                try:
                    config = self._get_system_config(definition, system)
                except ValueError:
                    continue
                content = self._render_skill(definition, config, system)
                output_path = self._resolve_output_path(config, system, output_override)
                resources = self._collect_resources(definition, output_path.parent)
                results.append(
                    RenderResult(
                        skill_id=skill_id,
                        system=system,
                        content=self._ensure_trailing_newline(content),
                        output_path=output_path,
                        resources=resources,
                    )
                )
        return results

    def _get_skill(self, skill_id: str) -> SkillDefinition:
        try:
            return CATALOG[skill_id]
        except KeyError as exc:
            available = ", ".join(sorted(CATALOG.keys()))
            raise ValueError(
                f"Unknown skill '{skill_id}'. Available: {available}"
            ) from exc

    def _get_system_config(
        self, definition: SkillDefinition, system: str
    ) -> SystemSkillConfig:
        try:
            return definition.systems[system]
        except KeyError as exc:
            available = ", ".join(sorted(definition.systems.keys()))
            raise ValueError(
                f"Skill '{definition.skill_id}' does not support system '{system}'. Available: {available}"
            ) from exc

    def _render_skill(
        self, definition: SkillDefinition, config: SystemSkillConfig, system: str
    ) -> str:
        source_path = (self.context.repo_root / definition.source_path).resolve()
        raw = source_path.read_text(encoding="utf-8")
        frontmatter, body = split_frontmatter(raw)
        frontmatter = _apply_system_tokens(frontmatter, system)
        body = _apply_system_tokens(body, system)
        fields = parse_simple_frontmatter(frontmatter)
        validate_skill_metadata(fields, definition.skill_id)

        template_path = (
            (self.context.repo_root / Path(config.template))
            .resolve()
            .relative_to(self.context.repo_root)
            .as_posix()
        )
        template = self.env.get_template(template_path)
        return template.render(
            frontmatter=frontmatter,
            body=body.rstrip() + "\n" if body.strip() else "",
            managed_sentinel=MANAGED_SENTINEL,
            skill=definition,
        )

    def _collect_resources(
        self, definition: SkillDefinition, output_root: Path
    ) -> list[ResourceCopy]:
        resources: list[ResourceCopy] = []
        source_root = (self.context.repo_root / definition.source_path).resolve().parent
        for folder in ("references", "resources", "scripts", "assets", "config"):
            src = source_root / folder
            if not src.exists():
                continue
            dest = output_root / folder
            resources.append(ResourceCopy(source=src, destination=dest))
        return resources

    def _resolve_output_path(
        self,
        config: SystemSkillConfig,
        system: str,
        overrides: dict[str, Path | None] | None,
    ) -> Path:
        base = None
        if overrides is not None:
            base = overrides.get(system)
        if base is None:
            return self.context.repo_root / config.output_path
        relative = self._system_relative_output_path(config.output_path, system)
        return base / relative

    @staticmethod
    def _system_relative_output_path(path: Path, system: str) -> Path:
        system_root = Path("systems") / system
        try:
            return path.relative_to(system_root)
        except ValueError:
            pass

        rendered_root = Path(".build") / "rendered" / system
        try:
            return path.relative_to(rendered_root)
        except ValueError:
            pass

        try:
            return path.relative_to(Path("systems"))
        except ValueError:
            return Path(path.name)

    @staticmethod
    def _ensure_trailing_newline(value: str) -> str:
        return value if value.endswith("\n") else f"{value}\n"


def _ignore_cache_files(_dir: str, names: list[str]) -> set[str]:
    ignored = {"__pycache__", ".pytest_cache", ".DS_Store"}
    ignored.update({name for name in names if name.endswith((".pyc", ".pyo"))})
    return ignored


_ASK_USER_MARKERS = {
    "claude-code": "request user confirmation using AskUserQuestion, then wait for the response",
    "codex": "ask the user for confirmation and wait for the response",
}

_TOOL_TOKEN_MAP = {
    "@BASH": {"default": "Bash"},
    "@BASH_OUTPUT": {"default": "BashOutput"},
    "@KILL_SHELL": {"default": "KillShell"},
    "@READ": {"default": "Read"},
    "@WRITE": {"default": "Write"},
    "@EDIT": {"default": "Edit"},
    "@MULTI_EDIT": {"default": "MultiEdit"},
    "@NOTEBOOK_READ": {"default": "NotebookRead"},
    "@NOTEBOOK_EDIT": {"default": "NotebookEdit"},
    "@GREP": {"default": "Grep"},
    "@GLOB": {"default": "Glob"},
    "@WEB_SEARCH": {"default": "WebSearch"},
    "@WEB_FETCH": {"default": "WebFetch"},
    "@TASK": {"default": "Task"},
    "@TODO_WRITE": {"default": "TodoWrite"},
}


def _apply_system_tokens(content: str, system: str) -> str:
    replacements: dict[str, str] = {}
    ask_marker = _ASK_USER_MARKERS.get(system)
    if ask_marker:
        replacements["@ASK_USER_CONFIRMATION"] = ask_marker

    for token, mapping in _TOOL_TOKEN_MAP.items():
        replacement = mapping.get(system, mapping.get("default"))
        if replacement:
            replacements[token] = replacement

    # Replace tokens longest-first to prevent partial matches (e.g., @BASH before @BASH_OUTPUT)
    for token in sorted(replacements.keys(), key=len, reverse=True):
        content = content.replace(token, replacements[token])
    return content


def _copy_resource_dir(source: Path, destination: Path, system: str) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob("*"):
        if path.is_dir():
            continue
        if path.name in {"__pycache__", ".pytest_cache", ".DS_Store"}:
            continue
        rel = path.relative_to(source)
        target = destination / rel
        _copy_resource_file(path, target, system)


def _copy_resource_file(source: Path, destination: Path, system: str) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix.lower() == ".md":
        content = source.read_text(encoding="utf-8")
        content = _apply_system_tokens(content, system)
        destination.write_text(content, encoding="utf-8")
    else:
        shutil.copy2(source, destination)
