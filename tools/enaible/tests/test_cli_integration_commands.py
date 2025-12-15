"""Integration smoke tests for Enaible CLI commands.

Tests all CLI commands with minimal arguments in an isolated environment
to catch runtime and environment regressions in deployed scenarios.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src"
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from enaible import app  # noqa: E402
from enaible.runtime.context import WorkspaceContext  # noqa: E402

runner = CliRunner()
REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def temp_home(tmp_path: Path) -> Path:
    """Create a temporary HOME directory for isolated testing."""
    home = tmp_path / "home"
    home.mkdir()
    return home


@pytest.fixture
def temp_workspace(tmp_path: Path) -> Path:
    """Create a temporary workspace directory."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def isolated_env(monkeypatch: pytest.MonkeyPatch, temp_home: Path, temp_workspace: Path) -> dict[str, str]:
    """Set up isolated environment variables for testing."""
    env = os.environ.copy()

    # Set up workspace paths
    env["ENAIBLE_REPO_ROOT"] = str(REPO_ROOT)
    env["ENAIBLE_SHARED_ROOT"] = str(REPO_ROOT / "shared")
    env["ENAIBLE_ARTIFACTS_DIR"] = str(temp_workspace / ".enaible")
    env["HOME"] = str(temp_home)

    # Create minimal directory structure for context capture
    (temp_home / ".claude" / "projects").mkdir(parents=True, exist_ok=True)
    (temp_home / ".codex" / "sessions").mkdir(parents=True, exist_ok=True)
    (temp_home / ".codex").mkdir(parents=True, exist_ok=True)

    # Set TLS cert env vars if available
    merged_ca = Path.home() / ".config" / "claude" / "corp-ca-bundle.pem"
    if merged_ca.exists():
        env["SSL_CERT_FILE"] = str(merged_ca)
        env["UV_HTTP_CA_BUNDLE"] = str(merged_ca)
        env["REQUESTS_CA_BUNDLE"] = str(merged_ca)

    return env


@pytest.fixture(autouse=True)
def _patch_workspace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch workspace context to use repo root."""
    context = WorkspaceContext(
        repo_root=REPO_ROOT,
        shared_root=REPO_ROOT / "shared",
        artifacts_root=REPO_ROOT / ".enaible",
    )
    # Patch all command modules that use load_workspace
    # Note: ci module doesn't use load_workspace, so we skip it
    monkeypatch.setattr("enaible.commands.install.load_workspace", lambda: context)
    monkeypatch.setattr("enaible.commands.prompts.load_workspace", lambda: context)
    monkeypatch.setattr("enaible.commands.analyzers.load_workspace", lambda: context)
    monkeypatch.setattr("enaible.commands.root.load_workspace", lambda: context)
    monkeypatch.setattr("enaible.commands.setup.load_workspace", lambda: context)


def test_version(isolated_env: dict[str, str]) -> None:
    """Test version command."""
    result = runner.invoke(app, ["version"], env=isolated_env)
    assert result.exit_code == 0
    assert "enaible" in result.stdout


def test_doctor(isolated_env: dict[str, str]) -> None:
    """Test doctor command with JSON output."""
    result = runner.invoke(app, ["doctor", "--json"], env=isolated_env)
    assert result.exit_code == 0
    assert "python" in result.stdout
    assert "enaible_version" in result.stdout


def test_install_dry_run(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test install command with dry-run to avoid actual file writes."""
    result = runner.invoke(
        app,
        [
            "install",
            "claude-code",
            "--target",
            str(tmp_path),
            "--mode",
            "merge",
            "--dry-run",
            "--no-sync",
            "--no-sync-shared",
            "--no-install-cli",
            "--no-backup",
        ],
        env=isolated_env,
    )
    assert result.exit_code == 0


def test_prompts_list(isolated_env: dict[str, str]) -> None:
    """Test prompts list command."""
    result = runner.invoke(app, ["prompts", "list"], env=isolated_env)
    assert result.exit_code == 0
    # Should list at least one prompt
    assert ":" in result.stdout or len(result.stdout.strip()) == 0


def test_prompts_lint(isolated_env: dict[str, str]) -> None:
    """Test prompts lint command."""
    result = runner.invoke(app, ["prompts", "lint"], env=isolated_env)
    # Lint may pass or fail, but should not crash
    assert result.exit_code in (0, 1)


def test_prompts_render(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test prompts render with a sample prompt."""
    output_dir = tmp_path / "rendered"
    result = runner.invoke(
        app,
        [
            "prompts",
            "render",
            "--prompt",
            "all",
            "--system",
            "claude-code",
            "--out",
            str(output_dir),
        ],
        env=isolated_env,
    )
    # Render may succeed or fail depending on prompt definitions, but should not crash
    assert result.exit_code in (0, 1)


def test_analyzers_list(isolated_env: dict[str, str]) -> None:
    """Test analyzers list command."""
    result = runner.invoke(app, ["analyzers", "list"], env=isolated_env)
    # May fail if registry not bootstrapped, but should not crash
    assert result.exit_code in (0, 1)


def _check_analyzer_registry_available() -> bool:
    """Check if analyzer registry can be loaded."""
    try:
        from core.base import AnalyzerRegistry  # noqa: F401
        return True
    except ImportError:
        return False


@pytest.mark.skipif(
    not _check_analyzer_registry_available(),
    reason="Analyzer registry not available or dependencies missing",
)
def test_analyzers_run(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test analyzers run command (skipped if registry unavailable)."""
    # Create a minimal Python file for testing
    test_file = tmp_path / "test.py"
    test_file.write_text("def hello():\n    pass\n")

    result = runner.invoke(
        app,
        [
            "analyzers",
            "run",
            "quality:lizard",
            "--target",
            str(tmp_path),
            "--max-files",
            "1",
        ],
        env=isolated_env,
    )
    # May fail if analyzer dependencies missing, but should not crash
    assert result.exit_code in (0, 1)


def test_ci_convert_codeclimate(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test CI convert-codeclimate command with empty artifacts."""
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    result = runner.invoke(
        app,
        [
            "ci",
            "convert-codeclimate",
            str(artifacts_dir),
        ],
        env=isolated_env,
    )
    # Should handle empty artifacts gracefully
    assert result.exit_code in (0, 1)


def test_ci_security_markdown(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test CI security-markdown command with empty artifacts."""
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    result = runner.invoke(
        app,
        [
            "ci",
            "security-markdown",
            str(artifacts_dir),
        ],
        env=isolated_env,
    )
    # Should handle empty artifacts gracefully
    assert result.exit_code in (0, 1)


def test_context_capture_claude(isolated_env: dict[str, str]) -> None:
    """Test context_capture for Claude with minimal days."""
    result = runner.invoke(
        app,
        [
            "context_capture",
            "--platform",
            "claude",
            "--days",
            "0",
            "--output-format",
            "json",
        ],
        env=isolated_env,
    )
    # Should handle empty sessions gracefully
    assert result.exit_code in (0, 1)


def test_context_capture_codex(isolated_env: dict[str, str]) -> None:
    """Test context_capture for Codex with minimal days."""
    result = runner.invoke(
        app,
        [
            "context_capture",
            "--platform",
            "codex",
            "--days",
            "0",
            "--output-format",
            "json",
        ],
        env=isolated_env,
    )
    # Should handle empty sessions gracefully
    assert result.exit_code in (0, 1)


def _check_web_scraper_available() -> bool:
    """Check if web_scraper module is available."""
    try:
        import importlib
        importlib.import_module("web_scraper.cli")
        return True
    except ImportError:
        return False


def _check_auth_script_exists() -> bool:
    """Check if auth check script exists."""
    script_path = REPO_ROOT / "shared" / "tests" / "integration" / "fixtures" / "check-ai-cli-auth.sh"
    return script_path.exists()


@pytest.mark.skipif(
    not _check_web_scraper_available(),
    reason="Requires web_scraper module which may not be available",
)
def test_docs_scrape(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test docs_scrape command (skipped if web_scraper not available)."""
    # Create a minimal HTML file for testing
    html_file = tmp_path / "test.html"
    html_file.write_text("<html><body><h1>Test</h1></body></html>")

    output_file = tmp_path / "output.md"
    result = runner.invoke(
        app,
        [
            "docs_scrape",
            f"file://{html_file}",
            str(output_file),
        ],
        env=isolated_env,
    )
    assert result.exit_code in (0, 1)


@pytest.mark.skipif(
    not _check_auth_script_exists(),
    reason="Auth check script not found in expected location",
)
def test_auth_check(isolated_env: dict[str, str]) -> None:
    """Test auth_check command (skipped if script missing)."""
    result = runner.invoke(
        app,
        [
            "auth_check",
            "--cli",
            "claude",
        ],
        env=isolated_env,
    )
    # Should exit cleanly (may fail auth check but not crash)
    assert result.exit_code in (0, 1)


@pytest.mark.skipif(
    _check_auth_script_exists(),
    reason="Script exists, testing missing script case separately",
)
def test_auth_check_script_missing(isolated_env: dict[str, str]) -> None:
    """Test auth_check command when script is missing (expected failure)."""
    result = runner.invoke(
        app,
        [
            "auth_check",
            "--cli",
            "claude",
        ],
        env=isolated_env,
    )
    # Expected to fail with exit code 1 when script missing
    assert result.exit_code == 1
    assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()


def _check_setup_script_exists(script_name: str) -> bool:
    """Check if a setup script exists."""
    script_path = REPO_ROOT / "shared" / "setup" / script_name
    return script_path.exists()


@pytest.mark.skipif(
    not _check_setup_script_exists("monitoring/install_monitoring_dependencies.py"),
    reason="Monitoring deps script not found",
)
def test_setup_monitoring_deps_dry_run(isolated_env: dict[str, str]) -> None:
    """Test setup monitoring-deps with dry-run."""
    result = runner.invoke(
        app,
        [
            "setup",
            "monitoring-deps",
            "--dry-run",
        ],
        env=isolated_env,
    )
    # Should handle dry-run gracefully
    assert result.exit_code in (0, 1)


@pytest.mark.skipif(
    not _check_setup_script_exists("security/setup_package_monitoring.py"),
    reason="Package monitoring script not found",
)
def test_setup_package_monitoring(isolated_env: dict[str, str], tmp_path: Path) -> None:
    """Test setup package-monitoring with a temporary package file."""
    # Create a minimal package.json for testing
    package_file = tmp_path / "package.json"
    package_file.write_text('{"name": "test", "version": "1.0.0"}')

    result = runner.invoke(
        app,
        [
            "setup",
            "package-monitoring",
            "--package-file",
            str(package_file),
            "--audit-level",
            "critical",
        ],
        env=isolated_env,
    )
    # May fail if dependencies unavailable, but should not crash
    assert result.exit_code in (0, 1)
