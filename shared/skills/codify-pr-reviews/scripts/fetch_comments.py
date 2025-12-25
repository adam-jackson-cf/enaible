#!/usr/bin/env python3
"""Fetch PR review comments via gh CLI."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


def run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Command failed")
    return result.stdout


def parse_repo() -> str:
    output = run(["git", "remote", "get-url", "origin"]).strip()
    if output.endswith(".git"):
        output = output[:-4]
    if output.startswith("git@github.com:"):
        return output.replace("git@github.com:", "")
    if "github.com/" in output:
        return output.split("github.com/")[-1]
    raise RuntimeError("Unable to parse GitHub repo from git remote origin")


def load_defaults(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        return {}
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_prs(repo: str, start_date: str, limit: int = 1000) -> list[dict[str, Any]]:
    output = run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--search",
            f"created:>={start_date}",
            "--json",
            "number,title,author,createdAt,state,mergedAt",
            "--limit",
            str(limit),
        ]
    )
    return json.loads(output or "[]")


def fetch_comments(
    repo: str, pr_number: int, comment_type: str
) -> list[dict[str, Any]]:
    endpoint = f"repos/{repo}/pulls/{pr_number}/comments"
    if comment_type == "issue":
        endpoint = f"repos/{repo}/issues/{pr_number}/comments"
    output = run(["gh", "api", endpoint])
    return json.loads(output or "[]")


def normalize_author(author: str | None) -> str:
    return (author or "").lower().strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch PR review comments via gh CLI.")
    parser.add_argument("--repo", default="")
    parser.add_argument("--days-back", type=int, default=None)
    parser.add_argument("--exclude-authors", default="")
    parser.add_argument("--min-comment-length", type=int, default=None)
    parser.add_argument("--output-path", default="")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--sample-prs", type=int, default=5)
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "defaults.json"),
    )
    args = parser.parse_args()

    defaults = load_defaults(Path(args.config))
    days_back = args.days_back or defaults.get("defaultDaysBack", 90)
    exclude_authors = (
        args.exclude_authors.split(",")
        if args.exclude_authors
        else defaults.get("defaultExcludeAuthors", [])
    )
    exclude_set = {normalize_author(a) for a in exclude_authors}
    min_length = args.min_comment_length or defaults.get("defaultMinCommentLength", 20)

    repo = args.repo or parse_repo()
    start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")

    prs = load_prs(repo, start_date)
    if args.preflight:
        sample = prs[: args.sample_prs]
        sample_count = len(sample)
        sample_comments = 0
        if sample:
            comments = fetch_comments(repo, sample[0]["number"], "review")
            sample_comments = len(comments)
        summary = {
            "repo": repo,
            "startDate": start_date,
            "samplePRs": sample_count,
            "sampleComments": sample_comments,
        }
        print(json.dumps(summary, indent=2))
        return 0

    pull_requests: list[dict[str, Any]] = []
    total_comments = 0
    review_count = 0
    issue_count = 0

    for pr in prs:
        pr_number = pr["number"]
        review_comments = fetch_comments(repo, pr_number, "review")
        issue_comments = fetch_comments(repo, pr_number, "issue")

        comments: list[dict[str, Any]] = []
        for comment in review_comments:
            author = normalize_author(comment.get("user", {}).get("login"))
            body = (comment.get("body") or "").strip()
            if author in exclude_set or len(body) < min_length:
                continue
            review_count += 1
            comments.append(
                {
                    "id": comment.get("id"),
                    "type": "review",
                    "author": author,
                    "body": body,
                    "path": comment.get("path"),
                    "line": comment.get("line"),
                    "createdAt": comment.get("created_at"),
                }
            )

        for comment in issue_comments:
            author = normalize_author(comment.get("user", {}).get("login"))
            body = (comment.get("body") or "").strip()
            if author in exclude_set or len(body) < min_length:
                continue
            issue_count += 1
            comments.append(
                {
                    "id": comment.get("id"),
                    "type": "issue",
                    "author": author,
                    "body": body,
                    "createdAt": comment.get("created_at"),
                }
            )

        if comments:
            pull_requests.append(
                {
                    "number": pr_number,
                    "title": pr.get("title"),
                    "author": pr.get("author", {}).get("login"),
                    "createdAt": pr.get("createdAt"),
                    "state": pr.get("state"),
                    "comments": comments,
                }
            )
            total_comments += len(comments)

    payload = {
        "fetchedAt": datetime.utcnow().isoformat() + "Z",
        "repository": repo,
        "dateRange": {
            "start": start_date,
            "end": datetime.utcnow().strftime("%Y-%m-%d"),
        },
        "totalPRs": len(prs),
        "totalComments": total_comments,
        "reviewComments": review_count,
        "issueComments": issue_count,
        "pullRequests": pull_requests,
    }

    if args.output_path:
        output_path = Path(args.output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Wrote comments to {output_path}")
    else:
        print(json.dumps(payload, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
