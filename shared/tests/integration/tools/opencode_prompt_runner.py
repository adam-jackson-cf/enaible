"""Helpers for executing OpenCode prompts inside tmux sessions."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
import subprocess
import time
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "PromptEntry",
    "load_manifest",
    "compute_prompt_hash",
    "run_opencode_prompt",
]


@dataclass(frozen=True)
class PromptEntry:
    prompt_id: str
    command: str
    version: str
    model: str | None
    args: tuple[str, ...]
    success_markers: tuple[str, ...]
    timeout_sec: int
    source_files: tuple[Path, ...]


def load_manifest(repo_root: Path) -> tuple[dict[str, object], list[PromptEntry]]:
    manifest_path = repo_root / "systems" / "opencode" / "prompt-manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    template_files = tuple(Path(p) for p in data.get("template_files", []))
    entries: list[PromptEntry] = []
    for raw in data["prompts"]:
        entries.append(
            PromptEntry(
                prompt_id=raw["prompt_id"],
                command=raw["command"],
                version=raw["version"],
                model=raw.get("model"),
                args=tuple(raw.get("args", [])),
                success_markers=tuple(raw.get("success_markers", [])),
                timeout_sec=int(raw.get("timeout_sec", 120)),
                source_files=tuple(Path(p) for p in raw.get("source_files", [])),
            )
        )
    meta = {
        "default_model": data.get("default_model"),
        "template_files": template_files,
    }
    return meta, entries


def compute_prompt_hash(
    repo_root: Path, entry: PromptEntry, template_files: Iterable[Path]
) -> str:
    sha = hashlib.sha256()
    for rel in list(entry.source_files) + list(template_files):
        path = repo_root / rel
        if path.exists():
            sha.update(path.read_bytes())
    return sha.hexdigest()


def _quote(value: str | Path) -> str:
    return shlex.quote(str(value))


def run_opencode_prompt(
    *,
    entry: PromptEntry,
    install_root: Path,
    fixtures_root: Path,
    artifacts_root: Path,
    model: str,
) -> Path:
    """Execute an OpenCode command inside tmux and return the log path."""
    timestamp = time.strftime("%Y%m%dT%H%M%S")
    session = f"enaible-opencode-{entry.prompt_id}-{timestamp}".replace("/", "-")
    artifacts_root.mkdir(parents=True, exist_ok=True)
    log_path = artifacts_root / f"opencode-{entry.prompt_id}-{timestamp}.log"
    log_path.write_text("", encoding="utf-8")

    args = [arg.replace("{fixture_root}", str(fixtures_root)) for arg in entry.args]
    command_message = "/" + entry.command
    if args:
        command_message += " " + " ".join(args)

    full_cmd = (
        f"cd {_quote(install_root)} && "
        f"opencode run {shlex.quote(command_message)} ; "
        "printf '__ENAIBLE_EXIT:%s\\n' $?; exit"
    )

    subprocess.run(
        ["tmux", "new-session", "-d", "-s", session, "bash"],
        check=True,
    )
    subprocess.run(
        ["tmux", "pipe-pane", "-t", session, "-o", f"cat >> {_quote(log_path)}"],
        check=True,
    )
    subprocess.run(
        ["tmux", "send-keys", "-t", session, full_cmd, "Enter"],
        check=True,
    )

    deadline = time.time() + entry.timeout_sec
    exit_code: int | None = None
    while time.time() < deadline:
        time.sleep(0.5)
        if log_path.exists():
            text = log_path.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"__ENAIBLE_EXIT:(\d+)", text)
            if match:
                exit_code = int(match.group(1))
                break
        if (
            subprocess.run(
                ["tmux", "has-session", "-t", session], check=False
            ).returncode
            != 0
        ):
            break
    subprocess.run(["tmux", "kill-session", "-t", session], check=False)

    if exit_code is None:
        raise TimeoutError(
            f"Prompt '{entry.prompt_id}' timed out after {entry.timeout_sec}s. Log: {log_path}"
        )

    log_text = log_path.read_text(encoding="utf-8", errors="ignore")
    log_clean = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", log_text)
    log_clean = re.sub(r"\x1b\].*?\x07", "", log_clean, flags=re.DOTALL)

    if exit_code != 0:
        raise RuntimeError(
            f"OpenCode command '{entry.command}' exited with {exit_code}.\n"
            f"Log file: {log_path}\n"
            f"Last 40 lines:\n" + "\n".join(log_clean.splitlines()[-40:])
        )

    missing = [marker for marker in entry.success_markers if marker not in log_clean]
    if missing:
        raise AssertionError(
            f"Prompt '{entry.prompt_id}' missing expected markers {missing}.\n"
            f"Log file: {log_path}\n"
            f"Last 40 lines:\n" + "\n".join(log_clean.splitlines()[-40:])
        )

    return log_path
