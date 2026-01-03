#!/usr/bin/env python3
"""Integration test covering the docs-scraper skill entrypoint.

Prereqs (run once in the pyenv/uv Python 3.12 environment):

    uv pip install --python "$(pyenv which python3.12 || pyenv which python)" \
        "crawl4ai>=0.7,<0.8" playwright
    uv run --python "$(pyenv which python3.12 || pyenv which python)" \
        python -m playwright install chromium
"""

from __future__ import annotations

import argparse
import importlib
import os
import shutil
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

SENTINEL_PATH = Path(".enaible") / "artifacts" / ".docs_scraper_test_bootstrap"


def _ensure_scraper_runtime_ready() -> None:
    """Install Crawl4AI + Playwright if they are missing."""

    def _has_runtime() -> bool:
        try:
            importlib.import_module("crawl4ai")
            return True
        except ModuleNotFoundError:
            return False

    if _has_runtime():
        return

    uv_path = shutil.which("uv")
    if not uv_path:
        pytest.skip("uv CLI is required to bootstrap docs scraper dependencies.")

    python_cmd = os.environ.get("PYTHON_CMD", "python3")
    env = os.environ.copy()

    install_cmd = [
        uv_path,
        "pip",
        "install",
        "--python",
        python_cmd,
        "crawl4ai>=0.7,<0.8",
        "playwright",
    ]

    try:
        subprocess.run(install_cmd, check=True, env=env)
        subprocess.run(
            [python_cmd, "-m", "playwright", "install", "chromium"],
            check=True,
            env=env,
        )
    except subprocess.CalledProcessError as exc:  # pragma: no cover - setup guard
        pytest.skip(f"Unable to install docs scraper deps: {exc}")

    SENTINEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    SENTINEL_PATH.touch(exist_ok=True)

    if not _has_runtime():  # pragma: no cover - defensive
        pytest.skip("crawl4ai still missing after attempted install")


_ensure_scraper_runtime_ready()
pytest.importorskip("crawl4ai")


class _FixtureHandler(BaseHTTPRequestHandler):
    """Serve a static HTML page for scraper tests."""

    _BODY = (
        "<html><head><title>Fixture Page</title></head>"
        "<body><h1>Docs Fixture</h1><p>Example content.</p></body></html>"
    )

    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler interface)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self._BODY)))
        self.end_headers()
        self.wfile.write(self._BODY.encode("utf-8"))

    def log_message(self, *args, **kwargs):  # type: ignore[override]
        """Silence BaseHTTPRequestHandler logging during tests."""
        return


@pytest.fixture(scope="module")
def docs_server():
    """Yield a local HTTP URL hosting the fixture HTML."""
    server = ThreadingHTTPServer(("127.0.0.1", 0), _FixtureHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def _load_skill_modules():
    """Dynamically load the docs scraper modules for testing."""
    scripts_dir = (
        Path(__file__).resolve().parents[3]
        / "shared"
        / "skills"
        / "docs-scraper"
        / "scripts"
    )
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    scraper = importlib.import_module("scraper")
    session_manager = importlib.import_module("session_manager")
    run_docs_scraper = importlib.import_module("run_docs_scraper")
    return scraper, session_manager, run_docs_scraper


@pytest.mark.asyncio
@pytest.mark.integration
async def test_docs_scraper_cli_writes_markdown_and_cleans_up(tmp_path, docs_server):
    scraper, session_manager, run_docs_scraper = _load_skill_modules()

    output_path = tmp_path / "fixture.md"
    args = argparse.Namespace(
        url=docs_server,
        output_path=str(output_path),
        title="Docs Scraper Fixture",
    )

    try:
        await run_docs_scraper.main_async(args)
    except RuntimeError as exc:
        message = str(exc).lower()
        if "playwright" in message or "chromium" in message:
            pytest.skip(f"Playwright runtime not installed: {exc}")
        raise

    result_text = output_path.read_text(encoding="utf-8")
    assert "# Docs Scraper Fixture" in result_text
    assert f"Source: {docs_server}" in result_text
    assert "Scraped: " in result_text
    assert "Docs Fixture" in result_text
    assert not session_manager.has_active_crawler()
    await session_manager.shutdown()
