#!/usr/bin/env python
"""Generate rule drafts from approved patterns."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from schema_utils import validate_coverage, validate_doc_patterns


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def detect_language(path: str | None) -> str:
    if not path:
        return "text"
    suffix = Path(path).suffix.lower()
    if suffix in {".ts", ".tsx"}:
        return "typescript"
    if suffix in {".js", ".jsx"}:
        return "javascript"
    if suffix in {".py"}:
        return "python"
    if suffix in {".go"}:
        return "go"
    if suffix in {".rb"}:
        return "ruby"
    return "text"


def resolve_instruction_files(
    instruction_arg: str, defaults: dict[str, Any]
) -> dict[str, str]:
    instruction_files = defaults.get("instructionFiles", {})
    if not instruction_arg:
        return instruction_files
    try:
        return json.loads(instruction_arg)
    except json.JSONDecodeError as e:
        raise SystemExit(
            "Error: --instruction-files must be valid JSON.\n"
            f"Got: {instruction_arg}\n"
            f"Parse error: {e}"
        ) from None


def read_snippet(path: Path, line: int | None) -> str | None:
    if not path.exists() or line is None:
        return None
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    idx = max(0, line - 3)
    snippet = lines[idx : idx + 6]
    if not snippet:
        return None
    return "\n".join(snippet)


def default_good_example(category: str, language: str) -> str | None:
    if category == "security" and language in {"typescript", "javascript"}:
        return """const query = "SELECT * FROM users WHERE id = ?";
const rows = await db.query(query, [userId]);"""
    if category == "security" and language == "python":
        return """cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))"""
    if category == "error-handling" and language in {"typescript", "javascript"}:
        return """try {
  const result = await doWork();
  return result;
} catch (error) {
  logger.error(error);
  throw error;
}"""
    if category == "type-safety" and language in {"typescript", "javascript"}:
        return """type User = { id: string; name: string };
const user: User = { id, name };"""
    if category == "react-patterns" and language in {"typescript", "javascript"}:
        return """{items.map(item => (
  <Row key={item.id} item={item} />
))}"""
    if category == "accessibility" and language in {"typescript", "javascript"}:
        return """<button aria-label="Close dialog">Close</button>"""
    return None


def pick_target(category: str, instruction_files: dict[str, str]) -> tuple[str, str]:
    if category == "security" and "vsCodeSecurity" in instruction_files:
        return "vsCodeSecurity", instruction_files["vsCodeSecurity"]
    if category in {"database", "api-design"} and "backend" in instruction_files:
        return "backend", instruction_files["backend"]
    if (
        category in {"react-patterns", "accessibility"}
        and "frontend" in instruction_files
    ):
        return "frontend", instruction_files["frontend"]
    return "repository", instruction_files.get(
        "repository", ".github/copilot-instructions.md"
    )


def load_patterns(patterns_path: Path) -> list[dict[str, Any]]:
    payload = read_json(patterns_path)
    validate_doc_patterns(payload)
    return payload.get("approvedPatterns") or payload.get("patterns") or []


def load_coverage_map(coverage_path: Path) -> dict[str, dict[str, Any]]:
    payload = read_json(coverage_path)
    validate_coverage(payload)
    return {item.get("id"): item for item in payload.get("patterns", [])}


def select_action(pattern: dict[str, Any]) -> str | None:
    action = pattern.get("action")
    if not action:
        action = (
            "strengthen" if pattern.get("triage") == "needs-strengthening" else "create"
        )
    if action in {"create", "strengthen"}:
        return action
    return None


def build_draft_content(
    pattern: dict[str, Any],
    coverage_info: dict[str, Any] | None,
    repo_root: Path,
) -> tuple[str, str]:
    category = pattern.get("category", "general")
    title = pattern.get("title", "Pattern")
    rule_id = slugify(pattern.get("id") or title)
    examples = pattern.get("examples", [])
    example = examples[0] if examples else {}
    file_path = example.get("path") or example.get("file")
    line = example.get("line")
    language = detect_language(file_path)
    bad_snippet = None
    if file_path:
        bad_snippet = read_snippet(repo_root / file_path, line)
    good_snippet = default_good_example(category, language)

    content_lines = [f"## {title}"]
    if pattern.get("id"):
        content_lines.append(f"Rule-ID: {pattern.get('id')}")
    content_lines.extend(["", f"{pattern.get('description', title)}", ""])
    content_lines.append(f"- ALWAYS address {title.lower()} findings promptly.")
    content_lines.append(f"- NEVER ignore recurring {category} review feedback.")

    if bad_snippet:
        content_lines.extend(["", "❌ BAD:", f"```{language}", bad_snippet, "```"])
    if good_snippet:
        content_lines.extend(["", "✅ GOOD:", f"```{language}", good_snippet, "```"])
    if not bad_snippet and not good_snippet:
        content_lines.extend(
            ["", "Example from reviews:", f"> {pattern.get('description', title)}"]
        )

    content_lines.append("")
    content_lines.append("### Deterministic enforcement?")
    if coverage_info and coverage_info.get("deterministicOptions"):
        content_lines.append("- Tooling recommendation(s):")
        for option in coverage_info["deterministicOptions"]:
            content_lines.append(
                f"  - {option['action']} ({option['tool']}; {option['reason']})"
            )
        content_lines.append(
            "- When adopting tooling, update relevant configs and rerun reviews."
        )
    else:
        content_lines.append(
            "- No deterministic tooling match. See `coverage.json` for evaluation."
        )

    return "\n".join(content_lines).rstrip() + "\n", rule_id


def write_draft(
    out_dir: Path,
    pattern: dict[str, Any],
    instruction_files: dict[str, str],
    coverage_map: dict[str, dict[str, Any]],
    repo_root: Path,
) -> dict[str, Any] | None:
    action = select_action(pattern)
    if not action:
        return None
    category = pattern.get("category", "general")
    target_key, target_path = pick_target(category, instruction_files)
    content, rule_id = build_draft_content(
        pattern, coverage_map.get(pattern.get("id")), repo_root
    )
    filename = f"draft-{target_key}-{action.upper()}-{rule_id}.md"
    (out_dir / filename).write_text(content, encoding="utf-8")
    return {
        "ruleId": rule_id,
        "action": action,
        "target": target_key,
        "targetFile": target_path,
        "draftFile": filename,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate rule drafts from approved patterns."
    )
    parser.add_argument("--patterns-path", required=True)
    parser.add_argument("--coverage-path", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--instruction-files", default="")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
    instruction_files = resolve_instruction_files(args.instruction_files, defaults)
    patterns = load_patterns(Path(args.patterns_path))
    coverage_map = load_coverage_map(Path(args.coverage_path))

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    generated = []
    for pattern in patterns:
        entry = write_draft(
            out_dir, pattern, instruction_files, coverage_map, Path(args.repo_root)
        )
        if entry:
            generated.append(entry)

    summary = {
        "generatedAt": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "totalRules": len(generated),
        "rules": generated,
    }

    summary_path = out_dir / "generated-rules.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Wrote drafts to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
