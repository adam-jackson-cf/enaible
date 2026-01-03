#!/usr/bin/env python3
"""Self-contained docs scraper entrypoint for the docs-scraper skill."""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

# Ensure sibling modules are importable when executed directly
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from scraper import scrape_url  # noqa: E402
from session_manager import session_manager  # noqa: E402


async def _scrape_to_markdown(url: str, output_path: Path, title: str | None) -> None:
    result = await scrape_url(url)

    if not result.get("success"):
        raise RuntimeError(result.get("error", "Unknown scraping error"))

    doc_title = title or result.get("title") or "Scraped Page"
    scraped_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    source_url = result.get("url") or url

    frontmatter = [
        f"Source: {source_url}",
        f"Scraped: {scraped_at}",
    ]

    content_lines = [
        f"# {doc_title}",
        "",
        *frontmatter,
        "",
        result.get("markdown", "").rstrip(),
        "",
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(content_lines).strip() + "\n", encoding="utf-8")


async def main_async(args: argparse.Namespace) -> None:
    output = Path(args.output_path)
    try:
        await _scrape_to_markdown(args.url, output, args.title)
    finally:
        await session_manager.cleanup_all_sessions()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Docs scraper helper")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("output_path", help="Markdown destination path")
    parser.add_argument("--title", help="Optional document title", default=None)
    parser.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level))
    try:
        asyncio.run(main_async(args))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Docs scraper failed: {exc}") from exc


if __name__ == "__main__":
    main()
