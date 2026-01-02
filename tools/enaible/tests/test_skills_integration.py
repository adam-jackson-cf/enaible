"""Integration-style tests for shared skills rendering."""

from __future__ import annotations

from pathlib import Path

from enaible.runtime.context import load_workspace
from enaible.skills.renderer import SkillRenderer


def test_codify_pr_reviews_render(tmp_path: Path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[3]
    monkeypatch.setenv("ENAIBLE_REPO_ROOT", str(repo_root))

    context = load_workspace()
    renderer = SkillRenderer(context)
    results = renderer.render(
        ["codify-pr-reviews"],
        ["claude-code"],
        {"claude-code": tmp_path},
    )
    assert results
    result = results[0]
    result.write()

    output_path = tmp_path / "skills" / "codify-pr-reviews" / "SKILL.md"
    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "<!-- generated: enaible -->" in content

    references_dir = tmp_path / "skills" / "codify-pr-reviews" / "references"
    scripts_dir = tmp_path / "skills" / "codify-pr-reviews" / "scripts"
    config_dir = tmp_path / "skills" / "codify-pr-reviews" / "config"

    assert references_dir.exists()
    assert scripts_dir.exists()
    assert config_dir.exists()

    fetching = references_dir / "fetching-workflow.md"
    assert fetching.exists()
    text = fetching.read_text(encoding="utf-8")
    assert "@ASK_USER_CONFIRMATION" not in text
    assert "AskUserQuestion" in text

    assert "@BASH" not in content
    assert not (references_dir / "interactive-review-workflow.md").exists()

    monkeypatch.delenv("ENAIBLE_REPO_ROOT", raising=False)
