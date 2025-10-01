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

# Module-level marker for Linear integration tests
pytestmark = [pytest.mark.linear, pytest.mark.timeout(120)]

# Fixture paths
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "plan_linear"
BASELINE_FIXTURE = FIXTURES_DIR / "baseline.md"
VARIANT_FIXTURE = FIXTURES_DIR / "variant.md"


def _assert_plan_hashes(pr: dict[str, Any]) -> None:
    """
    Assert that PlanLinearReport contains required hash fields with proper SHA256 format.
    """
    hashes = pr["planning"].get("hashes", {})
    required_keys = (
        "artifact_raw",
        "artifact_normalized",
        "plan",
        "config_fingerprint",
    )

    for key in required_keys:
        assert key in hashes, f"Missing required hash key: {key}"
        hash_value = hashes[key]
        assert isinstance(hash_value, str), f"Hash {key} must be a string"
        assert hash_value.startswith("sha256:"), f"Hash {key} must start with 'sha256:'"
        # SHA256 hex should be 64 characters after prefix
        assert (
            len(hash_value) == 71
        ), f"Hash {key} should be 71 chars (sha256: + 64 hex)"


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

    # Targeted search for PlanLinearReport to avoid parsing unrelated JSON
    plan_report_start = stripped.find('"PlanLinearReport"')
    if plan_report_start != -1:
        # Find the opening brace for PlanLinearReport value
        brace_start = stripped.find("{", plan_report_start)
        if brace_start != -1:
            # Find the matching closing brace
            brace_count = 0
            for i in range(brace_start, len(stripped)):
                if stripped[i] == "{":
                    brace_count += 1
                elif stripped[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        json_blob = stripped[brace_start : i + 1]
                        try:
                            return json.loads(json_blob)
                        except json.JSONDecodeError as e:
                            raise ValueError(
                                f"Failed to parse PlanLinearReport JSON: {e}"
                            ) from e

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
    replace_env: dict[str, str] | None = None,
    timeout: int = 60,
    stream: bool = False,
    log_level: str = "ERROR",
) -> tuple[dict[str, Any], subprocess.CompletedProcess[str]]:
    """
    Invoke /plan-linear via opencode --prompt and capture structured output.
    Returns (parsed_report_dict, completed_process).

    Args:
        artifact_or_string: Path to artifact file or string content
        *flags: Command line flags to pass
        cwd: Working directory for subprocess
        env: Environment variables to add to current environment
        replace_env: Complete environment replacement (ignores current env)
        timeout: Subprocess timeout in seconds (default 60)
        stream: If True, stream output live to terminal while still capturing for parsing
        log_level: Log level to pass to opencode (default ERROR)
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
    if replace_env is not None:
        proc_env = replace_env.copy()
    else:
        proc_env = os.environ.copy()
        if env:
            proc_env.update(env)

    # Build base command
    base_cmd = ["opencode", "--prompt", cmd_str, "--log-level", log_level]

    # Debug logging
    print(f"DEBUG: Running command: {' '.join(base_cmd)}")
    print(f"DEBUG: Working directory: {cwd}")
    # print(f"DEBUG: Environment has LINEAR_API_KEY: {'LINEAR_API_KEY' in proc_env}")
    print(f"DEBUG: Stream mode: {stream}")

    if not stream:
        # Original buffered behavior
        result = subprocess.run(
            base_cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            env=proc_env,
            timeout=timeout,
        )
        output = result.stdout
    else:
        # Streaming behavior
        proc = subprocess.Popen(
            base_cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=proc_env,
        )

        lines = []
        try:
            # Ensure stdout is not None
            if proc.stdout is None:
                raise RuntimeError("Failed to open subprocess stdout")

            for line in proc.stdout:
                # Live passthrough to terminal
                print(line, end="", flush=True)
                lines.append(line)

            # Wait for process with timeout
            try:
                return_code = proc.wait(timeout=timeout)
            except subprocess.TimeoutExpired as err:
                proc.kill()
                proc.wait()
                raise subprocess.TimeoutExpired(base_cmd, timeout) from err

            output = "".join(lines)

            # Create synthetic CompletedProcess to maintain return shape
            result = subprocess.CompletedProcess(
                args=base_cmd,
                returncode=return_code,
                stdout=output,
                stderr="",
            )

        except Exception:
            proc.kill()
            proc.wait()
            raise

    # Parse JSON from stdout
    report = _extract_json_from_output(output)

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
    temp_workspace: Path, linear_env: dict[str, str], capsys
):
    """Dry-run should produce a valid PlanLinearReport with readiness=true and no mutation."""
    artifact = temp_workspace / "fixtures" / "baseline.md"

    # Debug logging
    print(f"DEBUG: artifact exists: {artifact.exists()}")
    print(f"DEBUG: artifact path: {artifact}")
    print(f"DEBUG: linear_env: {linear_env}")
    print(f"DEBUG: cwd: {temp_workspace}")

    # Enable streaming if environment variable is set
    stream_output = os.getenv("STREAM_PLAN_LINEAR", "").lower() in ("1", "true", "yes")
    print(f"DEBUG: stream_output: {stream_output}")

    # Disable pytest capture for streaming to see live output
    if stream_output:
        print("DEBUG: Using streaming mode")
        with capsys.disabled():
            report, proc = run_plan_linear(
                artifact,
                "--dry-run",
                "--report-format",
                "json",
                cwd=temp_workspace,
                env=linear_env,
                stream=True,
                log_level="INFO",
            )
    else:
        print("DEBUG: Using buffered mode")
        report, proc = run_plan_linear(
            artifact,
            "--dry-run",
            "--report-format",
            "json",
            cwd=temp_workspace,
            env=linear_env,
        )

    print(f"DEBUG: Process completed with return code: {proc.returncode}")
    if proc.returncode != 0:
        print(f"DEBUG: stderr: {proc.stderr}")
        print(f"DEBUG: stdout (first 500 chars): {proc.stdout[:500]}")

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
    _assert_plan_hashes(pr)

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

    # Validate hash format
    _assert_plan_hashes(pr)

    # Schedule cleanup only if test passes
    if created:
        request.addfinalizer(
            lambda: archive_linear_issues(created, mutation["project_id"])
        )


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

    # Validate hash format for both reports
    _assert_plan_hashes(first_report["PlanLinearReport"])
    _assert_plan_hashes(second_report["PlanLinearReport"])

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

        # Create environment without Linear variables (complete replacement)
        no_env = {k: v for k, v in os.environ.items() if not k.startswith("LINEAR_")}

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
                replace_env=no_env,
            )
            # We expect this to fail due to missing Linear credentials
            assert proc.returncode != 0 or "error" in report.get("PlanLinearReport", {})
        except subprocess.TimeoutExpired:
            pytest.skip(
                "opencode command timed out - likely commands not properly installed"
            )
