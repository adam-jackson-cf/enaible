#!/usr/bin/env python
"""Minimal HTTP client for Parallel AI APIs."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_BASE = "https://api.parallel.ai"
SEARCH_EXTRACT_BETA_HEADER = "search-extract-2025-10-10"
FINDALL_BETA_HEADER = "findall-2025-09-15"


def get_api_key() -> str:
    key = os.environ.get("PARALLEL_API_KEY")
    if not key:
        raise RuntimeError(
            "PARALLEL_API_KEY not set. Get your key from https://platform.parallel.ai"
        )
    return key


def api_request(
    method: str,
    endpoint: str,
    payload: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
    beta_header: str | None = SEARCH_EXTRACT_BETA_HEADER,
) -> dict[str, Any]:
    headers = {
        "x-api-key": get_api_key(),
        "Content-Type": "application/json",
    }
    if beta_header:
        headers["parallel-beta"] = beta_header

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    url = f"{API_BASE}{endpoint}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"

    request = urllib.request.Request(
        url, data=data, headers=headers, method=method.upper()
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8")
        except Exception:
            body = ""
        raise RuntimeError(f"HTTP {exc.code}: {body or exc.reason}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from None
