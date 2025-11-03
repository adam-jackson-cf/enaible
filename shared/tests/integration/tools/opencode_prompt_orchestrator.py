"""Parallel OpenCode prompt orchestrator.

This script reads the OpenCode prompt manifest, launches each prompt inside a
dedicated tmux session, and verifies the resulting output for expected success
markers. Prompts run concurrently up to the configured limit so long-running
plans do not block the entire suite.
"""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
import time
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class PromptJob:
    prompt_id: str
    command: str
    args: Sequence[str]
    success_markers: Sequence[str]
    timeout_sec: int
    source_files: Sequence[str]


@dataclass
class RunningSession:
    session: str
    prompt: PromptJob
    log_path: Path
    start_ts: float


@dataclass
class PromptResult:
    prompt_id: str
    status: str
    duration_sec: float
    log_path: Path
    missing_markers: Sequence[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run OpenCode prompts in parallel via tmux"
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("systems/opencode/prompt-manifest.json"),
        help="Path to the OpenCode prompt manifest JSON.",
    )
    parser.add_argument(
        "--fixtures-root",
        type=Path,
        default=Path("shared/tests/integration/fixtures/prompt-e2e"),
        help="Fixture root used to substitute {fixture_root} placeholders.",
    )
    parser.add_argument(
        "--max-parallel",
        type=int,
        default=5,
        help="Maximum number of prompts to run concurrently.",
    )
    parser.add_argument(
        "--prompt",
        action="append",
        dest="prompt_filter",
        default=None,
        help="Prompt id(s) to run (defaults to all prompts in the manifest).",
    )
    parser.add_argument(
        "--sleep-interval",
        type=float,
        default=2.0,
        help="Polling interval (seconds) for tmux session completion.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> list[PromptJob]:
    data = json.loads(path.read_text(encoding="utf-8"))
    prompts: list[PromptJob] = []
    for raw in data.get("prompts", []):
        prompts.append(
            PromptJob(
                prompt_id=raw["prompt_id"],
                command=raw["command"],
                args=tuple(raw.get("args", [])),
                success_markers=tuple(raw.get("success_markers", [])),
                timeout_sec=int(raw.get("timeout_sec", 180)),
                source_files=tuple(raw.get("source_files", [])),
            )
        )
    return prompts


def filter_prompts(
    prompts: Iterable[PromptJob], selected: Iterable[str] | None
) -> list[PromptJob]:
    if selected is None:
        return list(prompts)
    selected_set = {s.strip() for s in selected}
    invalid = selected_set - {p.prompt_id for p in prompts}
    if invalid:
        raise ValueError(f"Unknown prompt id(s): {', '.join(sorted(invalid))}")
    return [p for p in prompts if p.prompt_id in selected_set]


def ensure_dirs(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def tmux_session_exists(session: str) -> bool:
    result = subprocess.run(
        ["tmux", "has-session", "-t", session],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def kill_tmux_session(session: str) -> None:
    subprocess.run(
        ["tmux", "kill-session", "-t", session],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def shell_quote_args(args: Sequence[str]) -> str:
    return shlex.join(args)


def build_command_message(prompt: PromptJob, fixtures_root: Path) -> str:
    resolved_args: list[str] = []
    for arg in prompt.args:
        resolved_args.append(arg.replace("{fixture_root}", str(fixtures_root)))
    message = "/" + prompt.command
    if resolved_args:
        message += " " + shell_quote_args(resolved_args)
    return message


def start_prompt_session(
    prompt: PromptJob,
    fixtures_root: Path,
    repo_root: Path,
) -> RunningSession:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    session = f"oc-{prompt.prompt_id[:12]}-{timestamp}"
    command_message = build_command_message(prompt, fixtures_root)
    log_dir = repo_root / ".enaible" / "artifacts" / "prompt-e2e" / prompt.prompt_id
    ensure_dirs(log_dir)
    log_path = log_dir / f"opencode-{prompt.prompt_id}-{timestamp}.log"
    ensure_dirs(log_path)

    # Compose shell command executed inside tmux
    shell_command = (
        f"cd {shlex.quote(str(repo_root))} && "
        f"opencode run {shlex.quote(command_message)} ; "
        "printf '__ENAIBLE_EXIT:%s\\n' $?"
    )

    subprocess.run(
        [
            "tmux",
            "new-session",
            "-d",
            "-s",
            session,
            "bash",
            "-lc",
            shell_command,
        ],
        check=True,
    )

    subprocess.run(
        [
            "tmux",
            "pipe-pane",
            "-t",
            session,
            "-o",
            f"cat >> {shlex.quote(str(log_path))}",
        ],
        check=True,
    )

    return RunningSession(
        session=session, prompt=prompt, log_path=log_path, start_ts=time.time()
    )


def read_log(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""


_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
_EXIT_PATTERN = re.compile(r"__ENAIBLE_EXIT:(\d+)")


def strip_ansi(text: str) -> str:
    return _ANSI_PATTERN.sub("", text)


def evaluate_prompt(prompt: PromptJob, log_path: Path, duration: float) -> PromptResult:
    content = strip_ansi(read_log(log_path))
    exit_match = _EXIT_PATTERN.search(content)
    missing = [marker for marker in prompt.success_markers if marker not in content]
    if exit_match is None:
        status = "failed"
    else:
        exit_code = int(exit_match.group(1))
        status = "passed" if exit_code == 0 and not missing else "failed"
    return PromptResult(prompt.prompt_id, status, duration, log_path, tuple(missing))


def summarize(results: Iterable[PromptResult]) -> None:
    passed = [r for r in results if r.status == "passed"]
    failed = [r for r in results if r.status != "passed"]
    print("\n=== OpenCode Prompt Results ===")
    for res in results:
        print(
            f"- {res.prompt_id}: {res.status.upper()} in {res.duration_sec:.1f}s (log: {res.log_path})"
        )
        if res.missing_markers:
            print(f"  Missing markers: {', '.join(res.missing_markers)}")
    print("\nSummary:")
    print(f"  Passed: {len(passed)}")
    print(f"  Failed: {len(failed)}")
    if failed:
        sys.exit(1)


def main() -> None:
    args = parse_args()
    repo_root = Path.cwd()
    manifests = load_manifest(args.manifest)
    prompts = filter_prompts(manifests, args.prompt_filter)
    if not prompts:
        print("No prompts selected.")
        return

    pending = prompts.copy()
    running: dict[str, RunningSession] = {}
    results: list[PromptResult] = []

    try:
        while pending or running:
            # Launch new sessions up to max parallelism
            while pending and len(running) < args.max_parallel:
                prompt = pending.pop(0)
                session_info = start_prompt_session(
                    prompt, args.fixtures_root, repo_root
                )
                running[session_info.session] = session_info

            finished_sessions: list[str] = []
            for session, info in running.items():
                if not tmux_session_exists(session):
                    duration = time.time() - info.start_ts
                    result = evaluate_prompt(info.prompt, info.log_path, duration)
                    results.append(result)
                    finished_sessions.append(session)
            for session in finished_sessions:
                running.pop(session, None)
                kill_tmux_session(session)

            if running:
                time.sleep(args.sleep_interval)

    finally:
        # Ensure stray sessions are terminated
        for session in list(running):
            kill_tmux_session(session)

    summarize(results)


if __name__ == "__main__":
    main()
