"""Skills command group for Enaible CLI."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path

import typer

from ..app import app
from ..runtime.context import load_workspace
from ..skills.catalog import SkillDefinition
from ..skills.lint import lint_files
from ..skills.renderer import SkillRenderer

_skills_app = typer.Typer(help="Render and validate managed skills.")
app.add_typer(_skills_app, name="skills")


def _resolve_skill_ids(
    catalog: dict[str, SkillDefinition], skills: Sequence[str]
) -> list[str]:
    if not skills or skills == ["all"]:
        return list(catalog.keys())

    catalog_ids = set(catalog.keys())
    unknown = [skill for skill in skills if skill not in catalog_ids]
    if unknown:
        available = ", ".join(sorted(catalog_ids))
        raise typer.BadParameter(
            f"Unknown skill(s): {', '.join(unknown)}. Available: {available}"
        )
    return list(skills)


def _resolve_systems(
    catalog: dict[str, SkillDefinition],
    skill_ids: Iterable[str],
    systems: Sequence[str],
) -> list[str]:
    if not systems or systems == ["all"]:
        supported: set[str] = set()
        for skill_id in skill_ids:
            definition = catalog[skill_id]
            supported.update(definition.systems.keys())
        return sorted(supported)
    return list(systems)


def _build_overrides(
    selected_systems: list[str], out: Path | None
) -> dict[str, Path | None]:
    if out is None:
        return dict.fromkeys(selected_systems)

    overrides: dict[str, Path | None] = {}
    if len(selected_systems) == 1:
        overrides[selected_systems[0]] = out
        return overrides

    for system in selected_systems:
        overrides[system] = out / system
    return overrides


def _split_csv(value: str) -> list[str]:
    if not value or value.lower() == "all":
        return ["all"]
    return [item.strip() for item in value.split(",") if item.strip()]


@_skills_app.command("list")
def skills_list() -> None:
    """List skills known to the catalog."""
    context = load_workspace()
    renderer = SkillRenderer(context)
    for definition in renderer.list_skills():
        systems = ", ".join(sorted(definition.systems.keys()))
        typer.echo(f"{definition.skill_id} [{systems}]")


@_skills_app.command("render")
def skills_render(
    skills: str = typer.Option(
        "all",
        "--skill",
        help="Comma-separated skill identifiers or 'all'.",
    ),
    systems: str = typer.Option(
        "all",
        "--system",
        help="Comma-separated system identifiers or 'all'.",
    ),
    out: Path | None = typer.Option(
        None,
        "--out",
        "-o",
        help="Optional override directory for rendered output.",
    ),
) -> None:
    """Render skills for the selected systems."""
    context = load_workspace()
    renderer = SkillRenderer(context)
    catalog = {definition.skill_id: definition for definition in renderer.list_skills()}

    skill_args = _split_csv(skills)
    system_args = _split_csv(systems)

    selected_skills = _resolve_skill_ids(catalog, skill_args)
    selected_systems = _resolve_systems(catalog, selected_skills, system_args)
    overrides = _build_overrides(selected_systems, out)

    results = renderer.render(selected_skills, selected_systems, overrides)

    for result in results:
        result.write()
        typer.echo(
            f"Rendered {result.skill_id} for {result.system} → {result.output_path}"
        )


@_skills_app.command("diff")
def skills_diff(
    skills: str = typer.Option("all", "--skill"),
    systems: str = typer.Option("all", "--system"),
) -> None:
    """Show diffs between catalog output and current files."""
    context = load_workspace()
    renderer = SkillRenderer(context)
    catalog = {definition.skill_id: definition for definition in renderer.list_skills()}

    skill_args = _split_csv(skills)
    system_args = _split_csv(systems)

    selected_skills = _resolve_skill_ids(catalog, skill_args)
    selected_systems = _resolve_systems(catalog, selected_skills, system_args)

    results = renderer.render(selected_skills, selected_systems)

    has_diff = False
    for result in results:
        diff_output = result.diff()
        if diff_output:
            has_diff = True
            typer.echo(diff_output)

    if has_diff:
        raise typer.Exit(code=1)


@_skills_app.command("validate")
def skills_validate(
    skills: str = typer.Option("all", "--skill"),
    systems: str = typer.Option("all", "--system"),
) -> None:
    """Validate that rendered skills match committed files."""
    try:
        skills_diff(skills=skills, systems=systems)
    except typer.Exit as exc:
        if exc.exit_code != 0:
            typer.echo("Skill drift detected. Run `enaible skills render` to update.")
        raise


@_skills_app.command("lint")
def skills_lint(
    skills: str = typer.Option("all", "--skill"),
) -> None:
    """Lint skill sources for frontmatter validity."""
    context = load_workspace()
    renderer = SkillRenderer(context)
    catalog = {definition.skill_id: definition for definition in renderer.list_skills()}

    selected_skills = _resolve_skill_ids(catalog, _split_csv(skills))
    files = {
        (context.repo_root / catalog[skill_id].source_path).resolve()
        for skill_id in selected_skills
    }

    issues = lint_files(files)
    if not issues:
        typer.echo("skills: lint passed")
        return
    for issue in issues:
        typer.echo(f"{issue.path}:{issue.line}: {issue.message}")
    raise typer.Exit(code=1)
