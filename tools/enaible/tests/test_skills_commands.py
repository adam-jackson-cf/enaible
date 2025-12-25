"""CLI tests for skills command group using stubs."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
from typer.testing import CliRunner

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(PACKAGE_ROOT))

from enaible import app  # noqa: E402

runner = CliRunner()


@dataclass
class _StubDefinition:
    skill_id: str
    systems: dict[str, object]


@dataclass
class _StubResult:
    skill_id: str
    system: str
    content: str
    output_path: Path
    resources: list[object]

    def write(self) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(self.content)

    def diff(self) -> str:
        return ""


class _StubRenderer:
    def __init__(self, context: object):
        self._definitions = [
            _StubDefinition(
                skill_id="demo-skill",
                systems={"claude-code": object()},
            )
        ]

    def list_skills(self) -> list[_StubDefinition]:
        return self._definitions

    def render(self, skill_ids, systems, overrides=None):
        base = overrides.get("claude-code") if overrides else Path.cwd()
        output_path = base / "skills" / "demo-skill" / "SKILL.md"
        return [
            _StubResult(
                skill_id="demo-skill",
                system="claude-code",
                content="demo content\n",
                output_path=output_path,
                resources=[],
            )
        ]


@pytest.fixture(autouse=True)
def _patch_renderer(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("enaible.commands.skills.SkillRenderer", _StubRenderer)
    monkeypatch.setattr("enaible.commands.skills.load_workspace", lambda: object())


def test_skills_list() -> None:
    result = runner.invoke(app, ["skills", "list"])
    assert result.exit_code == 0
    assert "demo-skill" in result.stdout


def test_skills_render(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "skills",
            "render",
            "--skill",
            "demo-skill",
            "--system",
            "claude-code",
            "--out",
            str(tmp_path),
        ],
    )
    assert result.exit_code == 0
    assert (tmp_path / "skills" / "demo-skill" / "SKILL.md").exists()


def test_skills_diff() -> None:
    result = runner.invoke(
        app, ["skills", "diff", "--skill", "demo-skill", "--system", "claude-code"]
    )
    assert result.exit_code == 0
