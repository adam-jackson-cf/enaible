#!/usr/bin/env python3
"""
Version bump and changelog generator for enaible.

Analyzes conventional commits to determine version bump type:
- feat: -> minor bump (0.1.1 -> 0.2.0)
- fix: -> patch bump (0.1.1 -> 0.1.2)
- BREAKING CHANGE -> major bump (0.1.1 -> 1.0.0)
- chore:, docs:, refactor:, test: -> no bump

Usage:
    python scripts/bump-version.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PYPROJECT_PATH = REPO_ROOT / "tools" / "enaible" / "pyproject.toml"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
README_PATH = REPO_ROOT / "README.md"

VERSION_PATTERN = re.compile(r'^version\s*=\s*"(\d+\.\d+\.\d+)"', re.MULTILINE)
COMMIT_TYPE_PATTERN = re.compile(r"^(\w+)(?:\(.+\))?:\s*(.+)$")

# Commit types that trigger version bumps
BUMP_TYPES = {
    "feat": "minor",
    "fix": "patch",
    "perf": "patch",
}


def get_current_version() -> str:
    """Read current version from pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    match = VERSION_PATTERN.search(content)
    if not match:
        raise ValueError(f"Could not find version in {PYPROJECT_PATH}")
    return match.group(1)


def parse_version(version: str) -> tuple[int, int, int]:
    """Parse semantic version string to tuple."""
    parts = version.split(".")
    return int(parts[0]), int(parts[1]), int(parts[2])


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version tuple to string."""
    return f"{major}.{minor}.{patch}"


def get_commits_since_last_bump() -> list[str]:
    """Get commit messages since last version bump commit."""
    result = subprocess.run(
        [
            "git",
            "log",
            "--oneline",
            "--format=%s",
            "--no-merges",
            "-50",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=True,
    )
    commits = result.stdout.strip().split("\n")

    # Filter out version bump commits and stop at previous bump
    filtered = []
    for commit in commits:
        if commit.startswith("chore: bump version") or commit.startswith(
            "chore(release):"
        ):
            break
        if commit:
            filtered.append(commit)

    return filtered


def analyze_commits(commits: list[str]) -> tuple[str, list[dict[str, str]]]:
    """
    Analyze commits to determine bump type and categorize changes.

    Returns
    -------
        Tuple of (bump_type, categorized_commits)
        bump_type: "major", "minor", "patch", or "none"
    """
    bump_type = "none"
    categorized: list[dict[str, str]] = []

    for commit in commits:
        # Check for breaking changes
        if "BREAKING CHANGE" in commit.upper():
            bump_type = "major"

        match = COMMIT_TYPE_PATTERN.match(commit)
        if match:
            commit_type = match.group(1).lower()
            message = match.group(2)

            categorized.append({"type": commit_type, "message": message, "raw": commit})

            # Determine bump level (highest wins)
            if commit_type in BUMP_TYPES:
                commit_bump = BUMP_TYPES[commit_type]
                if bump_type == "none":
                    bump_type = commit_bump
                elif bump_type == "patch" and commit_bump == "minor":
                    bump_type = "minor"
        else:
            # Non-conventional commit, include as-is
            categorized.append({"type": "other", "message": commit, "raw": commit})

    return bump_type, categorized


def calculate_new_version(current: str, bump_type: str) -> str:
    """Calculate new version based on bump type."""
    major, minor, patch = parse_version(current)

    if bump_type == "major":
        return format_version(major + 1, 0, 0)
    elif bump_type == "minor":
        return format_version(major, minor + 1, 0)
    elif bump_type == "patch":
        return format_version(major, minor, patch + 1)
    else:
        return current


def update_pyproject(new_version: str) -> None:
    """Update version in pyproject.toml."""
    content = PYPROJECT_PATH.read_text()
    updated = VERSION_PATTERN.sub(f'version = "{new_version}"', content)
    PYPROJECT_PATH.write_text(updated)


def generate_changelog_entry(version: str, commits: list[dict[str, str]]) -> str:
    """Generate changelog entry for new version."""
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    lines = [f"## [{version}] - {today}", ""]

    # Group by type for cleaner output
    type_order = ["feat", "fix", "perf", "refactor", "docs", "chore", "test", "other"]
    by_type: dict[str, list[str]] = {}

    for commit in commits:
        t = commit["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append(commit["raw"])

    for t in type_order:
        if t in by_type:
            for raw in by_type[t]:
                lines.append(f"- {raw}")

    lines.append("")
    return "\n".join(lines)


def update_changelog(entry: str) -> None:
    """Prepend new entry to changelog."""
    content = CHANGELOG_PATH.read_text()

    # Find insertion point (after header)
    header_end = content.find("\n## ")
    if header_end == -1:
        # No existing entries, append after header
        header_end = content.find("\n\n") + 1

    updated = content[:header_end] + "\n" + entry + content[header_end:]
    CHANGELOG_PATH.write_text(updated)


def get_recent_changes(limit: int = 5) -> list[str]:
    """Extract recent changes from changelog."""
    content = CHANGELOG_PATH.read_text()
    lines = content.split("\n")

    changes = []
    in_version = False

    for line in lines:
        if line.startswith("## ["):
            in_version = True
            continue
        if in_version and line.startswith("- "):
            changes.append(line)
            if len(changes) >= limit:
                break

    return changes


def update_readme(version: str, changes: list[str]) -> None:
    """Update README with version and recent changes."""
    content = README_PATH.read_text()

    # Build the new recent changes section
    changes_text = "\n".join(changes[:5])
    new_section = f"""### v{version} | Recent Changes
{changes_text}

[Full Changelog](CHANGELOG.md)"""

    # Pattern to match existing recent changes section
    pattern = re.compile(
        r"### v[\d.]+ \| Recent Changes.*?\[Full Changelog\]\(CHANGELOG\.md\)",
        re.DOTALL,
    )

    if pattern.search(content):
        # Replace existing section
        updated = pattern.sub(new_section, content)
    else:
        # Insert after badges (before the first ---)
        insert_marker = "\n---\n"
        idx = content.find(insert_marker)
        if idx != -1:
            updated = content[:idx] + "\n\n" + new_section + "\n" + content[idx:]
        else:
            # Fallback: append after </div>
            div_end = content.find("</div>")
            if div_end != -1:
                insert_pos = div_end
                updated = (
                    content[:insert_pos]
                    + "\n\n"
                    + new_section
                    + "\n\n"
                    + content[insert_pos:]
                )
            else:
                updated = content

    README_PATH.write_text(updated)


def main() -> int:
    parser = argparse.ArgumentParser(description="Bump version based on commits")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would happen without changes"
    )
    args = parser.parse_args()

    current_version = get_current_version()
    print(f"Current version: {current_version}")

    commits = get_commits_since_last_bump()
    if not commits:
        print("No new commits since last version bump")
        return 0

    print(f"Analyzing {len(commits)} commits...")

    bump_type, categorized = analyze_commits(commits)
    print(f"Bump type: {bump_type}")

    if bump_type == "none":
        print("No version-bumping commits found (only chore/docs/etc)")
        # Still update changelog and readme with current version
        if not args.dry_run:
            entry = generate_changelog_entry(current_version, categorized)
            update_changelog(entry)
            changes = get_recent_changes()
            update_readme(current_version, changes)
            print("Updated changelog and README (no version bump)")
        return 0

    new_version = calculate_new_version(current_version, bump_type)
    print(f"New version: {new_version}")

    if args.dry_run:
        print("\nDry run - no changes made")
        print("\nChanges that would be included:")
        for commit in categorized:
            print(f"  - {commit['raw']}")
        return 0

    # Apply changes
    update_pyproject(new_version)
    print(f"Updated {PYPROJECT_PATH}")

    entry = generate_changelog_entry(new_version, categorized)
    update_changelog(entry)
    print(f"Updated {CHANGELOG_PATH}")

    changes = get_recent_changes()
    update_readme(new_version, changes)
    print(f"Updated {README_PATH}")

    print(f"\nVersion bumped: {current_version} -> {new_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
