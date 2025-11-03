"""End-to-end smoke tests for OpenCode-managed prompts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import pytest

from .tools.opencode_prompt_runner import (
    PromptEntry,
    compute_prompt_hash,
    load_manifest,
    run_opencode_prompt,
)

# Opt-in: avoid consuming tokens unless explicitly requested.
pytestmark = pytest.mark.skipif(
    not os.getenv("ENABLE_OPENCODE_E2E"),
    reason="Set ENABLE_OPENCODE_E2E=1 to run OpenCode prompt integration tests.",
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_MANIFEST_META, _PROMPT_ENTRIES = load_manifest(_REPO_ROOT)
_PROMPT_IDS = [entry.prompt_id for entry in _PROMPT_ENTRIES]
_TEMPLATE_FILES = _MANIFEST_META.get("template_files", ())
_DEFAULT_MODEL = _MANIFEST_META.get("default_model") or "github-copilot/gpt-5-mini"
_FORCE_RUN = os.getenv("PROMPT_E2E_FORCE") == "1"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return _REPO_ROOT


@pytest.fixture(scope="session")
def fixtures_root(repo_root: Path) -> Path:
    return repo_root / "shared" / "tests" / "integration" / "fixtures" / "prompt-e2e"


@pytest.fixture(scope="session")
def _ensure_dependencies() -> None:
    missing = [cmd for cmd in ("tmux", "opencode") if shutil.which(cmd) is None]
    if missing:
        pytest.skip(f"Missing required CLI(s): {', '.join(missing)}")


@pytest.fixture(scope="session")
def _auth_preflight(repo_root: Path) -> None:
    script = (
        repo_root
        / "shared"
        / "tests"
        / "integration"
        / "fixtures"
        / "check-ai-cli-auth.sh"
    )
    result = subprocess.run(
        [str(script), "opencode"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(
            "OpenCode auth check failed:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )


@pytest.fixture(scope="session")
def opencode_install_root(tmp_path_factory: pytest.TempPathFactory) -> Path:
    workdir = tmp_path_factory.mktemp("opencode-install")
    cmd = [
        "uv",
        "run",
        "--project",
        "tools/enaible",
        "enaible",
        "install",
        "opencode",
        "--mode",
        "sync",
        "--scope",
        "project",
        "--target",
        str(workdir),
        "--no-backup",
    ]
    result = subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            "Failed to install OpenCode assets:\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )

    config_path = workdir / ".opencode" / "opencode.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    ce = config.setdefault("agent", {}).setdefault("command-executor", {})
    ce.setdefault("tools", {}).update(
        {
            "write": True,
            "edit": True,
            "bash": True,
            "read": True,
            "grep": True,
            "glob": True,
            "list": True,
            "patch": True,
        }
    )
    ce.setdefault("permission", {}).update(
        {
            "bash": "allow",
            "edit": "allow",
            "write": "allow",
            "read": "allow",
        }
    )
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    return workdir


@pytest.fixture(scope="session")
def prompt_cache(repo_root: Path):
    cache_path = repo_root / ".enaible" / "prompt-e2e" / "opencode.json"
    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    else:
        cache = {}
    updates: dict[str, dict[str, object]] = {}
    yield cache, updates
    if updates:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache.update(updates)
        cache_path.write_text(
            json.dumps(cache, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


@pytest.mark.usefixtures("_ensure_dependencies", "_auth_preflight")
@pytest.mark.parametrize("entry", _PROMPT_ENTRIES, ids=_PROMPT_IDS)
def test_opencode_prompt(
    entry: PromptEntry,
    opencode_install_root: Path,
    fixtures_root: Path,
    prompt_cache,
):
    cache, updates = prompt_cache
    prompt_hash = compute_prompt_hash(_REPO_ROOT, entry, _TEMPLATE_FILES)
    cache_entry = cache.get(entry.prompt_id)
    if (
        not _FORCE_RUN
        and cache_entry
        and cache_entry.get("hash") == prompt_hash
        and cache_entry.get("version") == entry.version
    ):
        pytest.skip("Prompt unchanged; cached run is still valid")

    artifacts_root = (
        _REPO_ROOT / ".enaible" / "artifacts" / "prompt-e2e" / entry.prompt_id
    )
    base_model = entry.model or _DEFAULT_MODEL
    model = cache_entry.get("model", base_model) if cache_entry else base_model

    log_path = run_opencode_prompt(
        entry=entry,
        install_root=opencode_install_root,
        fixtures_root=fixtures_root,
        artifacts_root=artifacts_root,
        model=model,
    )

    updates[entry.prompt_id] = {
        "hash": prompt_hash,
        "version": entry.version,
        "model": model,
        "last_run": datetime.now(UTC).isoformat(),
        "last_log": str(log_path.relative_to(_REPO_ROOT)),
    }
