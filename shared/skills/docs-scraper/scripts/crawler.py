"""
Simplified web crawler without LLM features.

Provides basic website crawling functionality using Crawl4AI.
"""

import logging
from typing import Any

from session_manager import session_manager
from utils import validate_and_normalize_url

logger = logging.getLogger(__name__)


async def crawl_website(
    url: str, crawl_depth: int = 1, max_pages: int = 5, query: str = ""
) -> list[dict[str, Any]]:
    """
    Crawl a website with basic keyword filtering.

    Args:
        url: Starting URL to crawl
        crawl_depth: Maximum depth to crawl (default: 1)
        max_pages: Maximum number of pages to crawl (default: 5)
        query: Optional search query for basic keyword filtering

    Returns
    -------
        List of dictionaries containing scraped page data
    """
    session_id = None
    try:
        # Validate and normalize URL
        url = validate_and_normalize_url(url)

        # Get crawler and session config
        crawler = await session_manager.get_crawler()
        config = await session_manager.get_session_config("crawl")
        session_id = config.session_id

        # Configure for crawling
        config.word_threshold = 10
        config.only_text = True
        config.page_timeout = 30000

        crawled_pages: list[dict[str, Any]] = []
        crawled_urls: set[str] = set()

        logger.info(
            f"Starting crawl of {url} with depth {crawl_depth} and max pages {max_pages}"
        )
        if query:
            logger.info(f"Using keyword filtering with query: '{query}'")
        await _crawl_loop(
            crawler,
            url,
            query,
            crawl_depth,
            max_pages,
            crawled_urls,
            crawled_pages,
        )

        # Clean up main session
        if session_id:
            await session_manager.cleanup_session(session_id)

        # Clean up old sessions periodically
        await session_manager.cleanup_old_sessions()

        logger.info(f"Completed crawl of {url}. Crawled {len(crawled_pages)} pages")
        return crawled_pages

    except Exception as e:
        logger.error(f"Error in crawl_website: {str(e)}")
        if session_id:
            await session_manager.handle_session_error(session_id)

        return [
            {
                "success": False,
                "url": url,
                "error": f"Crawling failed: {str(e)}",
                "error_type": type(e).__name__,
            }
        ]


async def _crawl_loop(
    crawler,
    start_url: str,
    query: str,
    crawl_depth: int,
    max_pages: int,
    crawled_urls: set[str],
    crawled_pages: list[dict[str, Any]],
) -> None:
    urls_to_crawl = [start_url]
    current_depth = 0
    while (
        urls_to_crawl
        and len(crawled_pages) < max_pages
        and current_depth <= crawl_depth
    ):
        current_level_urls = urls_to_crawl.copy()
        urls_to_crawl = []
        for current_url in current_level_urls:
            if len(crawled_pages) >= max_pages:
                break
            if current_url in crawled_urls:
                continue
            new_links = await _process_crawl_url(
                crawler,
                current_url,
                query,
                current_depth,
                crawl_depth,
                crawled_urls,
                crawled_pages,
            )
            for link in new_links:
                if link not in urls_to_crawl:
                    urls_to_crawl.append(link)
        current_depth += 1


async def _process_crawl_url(
    crawler,
    current_url: str,
    query: str,
    current_depth: int,
    crawl_depth: int,
    crawled_urls: set[str],
    crawled_pages: list[dict[str, Any]],
) -> list[str]:
    try:
        fresh_config = await session_manager.get_session_config("crawl_page")
        fresh_config.word_threshold = 10
        fresh_config.only_text = True
        fresh_config.page_timeout = 30000

        result = await crawler.arun(url=current_url, config=fresh_config)
        crawled_urls.add(current_url)
        if result.success:
            page_data = _build_success_page(
                result, current_depth, query, fresh_config.session_id
            )
            crawled_pages.append(page_data)
            logger.info(f"Successfully crawled {current_url} (depth {current_depth})")
            new_links = _extract_internal_links(
                result, current_depth, crawl_depth, query, crawled_urls
            )
            await session_manager.cleanup_session(fresh_config.session_id)
            return new_links
        logger.warning(f"Failed to crawl {current_url}: {result.error_message}")
        crawled_pages.append(
            {
                "success": False,
                "url": current_url,
                "error": result.error_message or "Unknown error",
                "depth": current_depth,
                "session_id": fresh_config.session_id,
            }
        )
        return []
    except Exception as e:
        logger.error(f"Error crawling {current_url}: {str(e)}")
        crawled_pages.append(
            {
                "success": False,
                "url": current_url,
                "error": f"Crawling failed: {str(e)}",
                "error_type": type(e).__name__,
                "depth": current_depth,
            }
        )
        return []


def _build_success_page(
    result, current_depth: int, query: str, session_id: str
) -> dict:
    matches_query = True
    if query:
        content = result.markdown.raw_markdown if result.markdown else ""
        title = result.metadata.get("title", "") if result.metadata else ""
        matches_query = _matches_keywords(content + " " + title, query)
    return {
        "success": True,
        "url": result.url,
        "title": result.metadata.get("title", "") if result.metadata else "",
        "status_code": result.status_code,
        "markdown": result.markdown.raw_markdown if result.markdown else "",
        "cleaned_html": result.cleaned_html[:3000] if result.cleaned_html else "",
        "depth": current_depth,
        "links_found": len(result.links.get("internal", [])) if result.links else 0,
        "metadata": result.metadata if result.metadata else {},
        "matches_query": matches_query,
        "session_id": session_id,
    }


def _extract_internal_links(
    result,
    current_depth: int,
    crawl_depth: int,
    query: str,
    crawled_urls: set[str],
) -> list[str]:
    if current_depth >= crawl_depth:
        return []
    if not result.links or "internal" not in result.links:
        return []
    internal_links = result.links["internal"][:10]
    links: list[str] = []
    for link in internal_links:
        if link in crawled_urls:
            continue
        if query and not _matches_keywords(link, query):
            continue
        links.append(link)
    return links


def _matches_keywords(text: str, query: str) -> bool:
    """Match keywords in text with case-insensitive search.

    Args:
        text: Text to search in
        query: Space-separated keywords

    Returns
    -------
        True if any keywords match (case-insensitive)
    """
    if not query or not text:
        return True

    # Split query into keywords
    keywords = [kw.strip().lower() for kw in query.split() if kw.strip()]
    if not keywords:
        return True

    text_lower = text.lower()

    # Check if any keyword is found in the text
    return any(keyword in text_lower for keyword in keywords)
