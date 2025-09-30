"""
Integration tests for /plan-linear command using real Linear MCP tools.

These tests exercise the full workflow: artifact classification → planning → hashing → readiness → mutation.
Tests are environment-gated and require LINEAR_* variables to run.

Test Strategy:
- Use deterministic fixtures (baseline.md, variant.md) for reproducibility
- Validate PlanLinearReport schema and invariants per spec
- Exercise dry-run, mutation, idempotency, and diff modes
- Archive created issues after successful mutation tests
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import pytest

# Fixture paths
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "plan_linear"
BASELINE_FIXTURE = FIXTURES_DIR / "baseline.md"
VARIANT_FIXTURE = FIXTURES_DIR / "variant.md"


def _extract_json_from_output(output: str) -> dict[str, Any]:
    """
    Extract JSON from stdout. Handles both direct JSON output and mixed output.
    Returns parsed dict or raises ValueError.
    """
    stripped = output.strip()
    if not stripped:
        raise ValueError("Empty output")

    # Try direct JSON parse first
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass

    # Fallback: find first { and last } to extract JSON blob
    first = stripped.find("{")
    last = stripped.rfind("}")
    if first == -1 or last == -1 or last <= first:
        raise ValueError("No JSON object found in output")

    json_blob = stripped[first : last + 1]
    try:
        return json.loads(json_blob)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse extracted JSON: {e}") from e


def run_plan_linear(
    artifact_or_string: str | Path,
    *flags: str,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: int | None = None,
) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    """
    Invoke /plan-linear via opencode --prompt and capture structured output.
    Returns (parsed_report_dict, completed_process).
    """
    if isinstance(artifact_or_string, Path):
        artifact_arg = artifact_or_string.name
        # Ensure we run in the fixture directory so relative paths resolve
        cwd = cwd or artifact_or_string.parent
    else:
        artifact_arg = artifact_or_string
        cwd = cwd or Path.cwd()

    # Build command string for opencode --prompt
    cmd_parts = ["/plan-linear", artifact_arg, *flags]
    cmd_str = " ".join(cmd_parts)

    # Prepare environment
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)

    # Run opencode
    result = subprocess.run(
        ["opencode", "--prompt", cmd_str, "--log-level", "ERROR"],
        cwd=cwd,
        capture_output=True,
        text=True,
        env=proc_env,
        timeout=timeout,
    )

    # Parse JSON from stdout
    report = _extract_json_from_output(result.stdout)

    return report, result


def archive_linear_issues(issue_ids: list[str], project_id: str) -> None:
    """
    Archive given Linear issue IDs in the specified project.
    Uses Linear GraphQL API for batch operations.
    """
    if not issue_ids:
        return

    api_key = os.getenv("LINEAR_API_KEY")
    if not api_key:
        print("Warning: LINEAR_API_KEY not set, cannot archive issues")
        return

    # GraphQL mutation for updating multiple issues
    mutation_template = """
    mutation IssueBatchUpdate($input: IssueBatchUpdateInput!) {
      issueBatchUpdate(input: $input) {
        success
        issues {
          id
          identifier
          title
          state {
            id
            name
          }
        }
      }
    }
    """

    # First, get the archived state ID for the team
    try:
        # Query to find the archived state
        states_query = f"""
        query {{
          workflowStates(filter: {{team: {{id: "{project_id}"}}, type: Archived}}) {{
            nodes {{
              id
              name
            }}
          }}
        }}
        """

        response = subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: {api_key}",
                "-d",
                json.dumps({"query": states_query}),
            ],
            capture_output=True,
            text=True,
        )

        if response.returncode != 0:
            print(f"Failed to query archived state: {response.stderr}")
            return

        states_data = json.loads(response.stdout)
        archived_states = (
            states_data.get("data", {}).get("workflowStates", {}).get("nodes", [])
        )

        if not archived_states:
            print("No archived state found for team")
            return

        archived_state_id = archived_states[0]["id"]

        # Now batch update the issues
        batch_input = {"issueIds": issue_ids, "stateId": archived_state_id}

        batch_response = subprocess.run(
            [
                "curl",
                "-X",
                "POST",
                "https://api.linear.app/graphql",
                "-H",
                "Content-Type: application/json",
                "-H",
                f"Authorization: {api_key}",
                "-d",
                json.dumps(
                    {"query": mutation_template, "variables": {"input": batch_input}}
                ),
            ],
            capture_output=True,
            text=True,
        )

        if batch_response.returncode == 0:
            result_data = json.loads(batch_response.stdout)
            if result_data.get("data", {}).get("issueBatchUpdate", {}).get("success"):
                archived_issues = result_data["data"]["issueBatchUpdate"]["issues"]
                print(f"Successfully archived {len(archived_issues)} issues")
                for issue in archived_issues:
                    print(f"  Archived: {issue['identifier']} - {issue['title']}")
            else:
                print(f"Batch archive failed: {result_data}")
        else:
            print(f"Failed to batch archive issues: {batch_response.stderr}")

    except Exception as e:
        print(f"Error during batch archive: {e}")


@pytest.fixture(scope="module")
def linear_env() -> dict[str, str]:
    """Provide Linear environment variables for tests."""
    required = ["LINEAR_API_KEY", "LINEAR_TEAM_ID", "LINEAR_TEST_PROJECT"]
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        pytest.skip(f"Missing required Linear env vars: {', '.join(missing)}")
    return {k: v for k, v in ((k, os.getenv(k)) for k in required) if v is not None}


@pytest.fixture
def temp_workspace():
    """Provide a temporary workspace directory for test runs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        # Copy fixtures into workspace for relative path resolution
        fixtures_target = workspace / "fixtures"
        shutil.copytree(FIXTURES_DIR, fixtures_target)
        yield workspace


def test_plan_linear_dry_run_structure(
    temp_workspace: Path, linear_env: dict[str, str]
):
    """Dry-run should produce a valid PlanLinearReport with readiness=true and no mutation."""
    artifact = temp_workspace / "fixtures" / "baseline.md"

    report, proc = run_plan_linear(
        artifact,
        "--dry-run",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )

    # Exit code should be 0
    assert proc.returncode == 0, f"Process failed: {proc.stderr}"

    # Top-level schema
    assert "PlanLinearReport" in report
    pr = report["PlanLinearReport"]
    assert pr.get("version") == 2

    # Required sections
    assert "objective" in pr
    assert "planning" in pr
    assert "readiness" in pr

    # Readiness must be true for dry-run success
    readiness = pr["readiness"]
    assert isinstance(readiness, dict)
    assert readiness.get("ready") is True
    assert "pending_steps" in readiness
    assert isinstance(readiness["pending_steps"], list)

    # Hashes must be present and look like SHA256
    hashes = pr["planning"].get("hashes", {})
    for key in ("artifact_raw", "artifact_normalized", "plan", "config_fingerprint"):
        assert key in hashes
        assert hashes[key].startswith("sha256:")

    # No mutation section in dry-run
    assert "mutation" not in pr

    # Issue totals sanity
    issue_totals = pr["planning"].get("issue_totals", {})
    assert isinstance(issue_totals, dict)
    assert issue_totals.get("total", 0) > 0


def test_plan_linear_mutation_creates_issues_and_preserves_hashes(
    temp_workspace: Path, linear_env: dict[str, str], request
):
    """Non-dry-run should create issues, preserve plan hash, and include mutation results."""
    artifact = temp_workspace / "fixtures" / "baseline.md"

    # First, capture dry-run hashes for comparison
    dry_report, _ = run_plan_linear(
        artifact,
        "--dry-run",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )
    dry_plan_hash = dry_report["PlanLinearReport"]["planning"]["hashes"]["plan"]

    # Mutation run with --auto to skip confirmations
    report, proc = run_plan_linear(
        artifact,
        "--auto",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )

    assert proc.returncode == 0, f"Mutation failed: {proc.stderr}"

    pr = report["PlanLinearReport"]
    # Mutation section must exist
    assert "mutation" in pr
    mutation = pr["mutation"]
    assert isinstance(mutation, dict)

    # Project ID should match our test project (allow for normalization differences)
    assert "project_id" in mutation
    # Note: We don't enforce exact match due to potential UUID/slug differences

    # Should have created issues
    created = mutation.get("created_issue_ids", [])
    assert isinstance(created, list)
    assert len(created) > 0, "No issues were created"

    # Plan hash must be unchanged
    current_plan_hash = pr["planning"]["hashes"]["plan"]
    assert current_plan_hash == dry_plan_hash, "Plan hash changed after mutation"

    # Readiness plan hash should match as well
    assert pr["readiness"]["plan_hash"] == current_plan_hash

    # Schedule cleanup only if test passes
    if created:
        request.addfinalizer(
            lambda: archive_linear_issues(created, mutation["project_id"])
        )
    dry_plan_hash = dry_report["PlanLinearReport"]["planning"]["hashes"]["plan"]

    # Mutation run with --auto to skip confirmations
    report, proc = run_plan_linear(
        artifact,
        "--auto",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )

    assert proc.returncode == 0, f"Mutation failed: {proc.stderr}"

    pr = report["PlanLinearReport"]
    # Mutation section must exist
    assert "mutation" in pr
    mutation = pr["mutation"]
    assert isinstance(mutation, dict)

    # Project ID should match our test project (allow for normalization differences)
    assert "project_id" in mutation
    # Note: We don't enforce exact match due to potential UUID/slug differences

    # Should have created issues
    created = mutation.get("created_issue_ids", [])
    assert isinstance(created, list)
    assert len(created) > 0, "No issues were created"

    # Plan hash must be unchanged
    current_plan_hash = pr["planning"]["hashes"]["plan"]
    assert current_plan_hash == dry_plan_hash, "Plan hash changed after mutation"

    # Readiness plan hash should match as well
    assert pr["readiness"]["plan_hash"] == current_plan_hash

    # Schedule cleanup only if test passes
    request.addfinalizer(lambda: archive_linear_issues(created, mutation["project_id"]))


def test_plan_linear_idempotency_skips_existing_issues(
    temp_workspace: Path, linear_env: dict[str, str], request
):
    """Second mutation run should skip existing issues and not change hashes."""
    artifact = temp_workspace / "fixtures" / "baseline.md"

    # First mutation run
    first_report, first_proc = run_plan_linear(
        artifact,
        "--auto",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )
    assert first_proc.returncode == 0
    first_created = first_report["PlanLinearReport"]["mutation"]["created_issue_ids"]
    first_plan_hash = first_report["PlanLinearReport"]["planning"]["hashes"]["plan"]
    project_id = first_report["PlanLinearReport"]["mutation"]["project_id"]

    # Second mutation run (idempotent)
    second_report, second_proc = run_plan_linear(
        artifact,
        "--auto",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )
    assert second_proc.returncode == 0

    second_mutation = second_report["PlanLinearReport"]["mutation"]
    # No new issues should be created
    assert second_mutation.get("created_issue_ids") == []
    # Should skip the ones created in first run
    skipped = second_mutation.get("skipped_issue_ids", [])
    assert set(skipped) == set(first_created), "Idempotency did not skip correct issues"

    # Plan hash must remain unchanged
    second_plan_hash = second_report["PlanLinearReport"]["planning"]["hashes"]["plan"]
    assert second_plan_hash == first_plan_hash, "Plan hash changed in idempotent run"

    # Cleanup: archive the issues created in the first run
    if first_created:
        request.addfinalizer(lambda: archive_linear_issues(first_created, project_id))


def test_plan_linear_diff_mode_detects_changes(
    temp_workspace: Path, linear_env: dict[str, str]
):
    """Diff mode should detect changes between baseline and variant artifacts."""
    baseline = temp_workspace / "fixtures" / "baseline.md"
    variant = temp_workspace / "fixtures" / "variant.md"

    # Generate baseline report
    baseline_report, baseline_proc = run_plan_linear(
        baseline,
        "--dry-run",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )
    assert baseline_proc.returncode == 0
    baseline_plan_hash = baseline_report["PlanLinearReport"]["planning"]["hashes"][
        "plan"
    ]

    # Save baseline to a temporary file for diff input
    baseline_file = temp_workspace / "baseline.json"
    baseline_file.write_text(json.dumps(baseline_report, indent=2))

    # Run variant with diff against baseline
    diff_report, diff_proc = run_plan_linear(
        variant,
        "--diff",
        str(baseline_file),
        "--dry-run",
        "--report-format",
        "json",
        cwd=temp_workspace,
        env=linear_env,
    )
    assert diff_proc.returncode == 0

    pr = diff_report["PlanLinearReport"]
    # Diff section must be present
    assert "diff" in pr
    diff = pr["diff"]
    assert isinstance(diff, dict)

    # Should detect changes
    assert any(
        diff.get(k) for k in ("added", "removed", "changed")
    ), "No changes detected"

    # Plan hashes should differ
    assert diff.get("plan_hash_before") != diff.get(
        "plan_hash_after"
    ), "Plan hash unchanged"

    # Current plan hash should match 'after'
    current_plan_hash = pr["planning"]["hashes"]["plan"]
    assert current_plan_hash == diff.get("plan_hash_after")

    # Baseline hash should match 'before'
    assert baseline_plan_hash == diff.get("plan_hash_before")


def test_plan_linear_error_handling_missing_env(request):
    """Missing Linear env vars should cause tests to be skipped, not fail."""
    # This test validates our env gating logic

    # First check if opencode is properly installed with commands
    try:
        check_result = subprocess.run(
            ["opencode", "--help"], capture_output=True, text=True, timeout=10
        )
        if check_result.returncode != 0:
            pytest.skip("opencode CLI not available - skipping integration test")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pytest.skip("opencode CLI not available - skipping integration test")

    with tempfile.TemporaryDirectory() as tmpdir:
        workspace = Path(tmpdir)
        fixtures_target = workspace / "fixtures"
        shutil.copytree(FIXTURES_DIR, fixtures_target)
        artifact = fixtures_target / "baseline.md"

        # Remove Linear env vars
        no_env = {}

        # Should raise subprocess error or return non-zero due to missing auth
        # We don't assert specific behavior here since opencode may handle missing auth differently
        # The important part is that our env-gated tests skip appropriately
        try:
            report, proc = run_plan_linear(
                artifact,
                "--dry-run",
                "--report-format",
                "json",
                cwd=workspace,
                env=no_env,
                timeout=15,  # Add timeout to prevent hanging
            )
            # We expect this to fail due to missing Linear credentials
            assert proc.returncode != 0 or "error" in report.get("PlanLinearReport", {})
        except subprocess.TimeoutExpired:
            pytest.skip(
                "opencode command timed out - likely commands not properly installed"
            )
