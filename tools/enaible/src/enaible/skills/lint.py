from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .utils import (
    SkillFormatError,
    parse_simple_frontmatter,
    split_frontmatter,
    validate_skill_metadata,
)


@dataclass(frozen=True)
class LintIssue:
    path: Path
    line: int
    message: str


def lint_content(path: Path, content: str) -> list[LintIssue]:
    issues: list[LintIssue] = []
    try:
        frontmatter, _body = split_frontmatter(content)
        fields = parse_simple_frontmatter(frontmatter)
        skill_id = path.parent.name
        validate_skill_metadata(fields, skill_id)
    except SkillFormatError as exc:
        issues.append(LintIssue(path, 1, str(exc)))
    except Exception as exc:  # pragma: no cover
        issues.append(LintIssue(path, 1, f"Unable to lint file: {exc}"))
    return issues


def lint_files(files: Iterable[Path]) -> list[LintIssue]:
    issues: list[LintIssue] = []
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            issues.append(LintIssue(path, 1, f"Unable to read file: {exc}"))
            continue
        issues.extend(lint_content(path, content))
    return issues
