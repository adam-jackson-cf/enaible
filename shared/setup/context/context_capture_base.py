"""Shared logic for context bundle capture across IDE integrations."""
from __future__ import annotations

import contextlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

try:
    from sensitive_data_redactor import redact_sensitive_data as _redact_sensitive_data
except ImportError:  # pragma: no cover - optional dependency at runtime
    _redact_sensitive_data = None  # type: ignore[assignment]


@dataclass(frozen=True)
class ContextCapturePaths:
    """Environment-specific path configuration."""

    project_dir_env: str
    context_dir_name: str


class ContextCaptureRunner:
    """Context bundle capture implementation shared between Claude and Opencode."""

    def __init__(self, paths: ContextCapturePaths) -> None:
        self.paths = paths
        self.seen_operations: set[tuple[str, str]] = set()

    def capture_action(
        self, event_type: str, data: dict[str, Any] | None = None
    ) -> None:
        """Capture action for the specified event type using the provided payload."""
        try:
            config = self.load_config()
            bundle_dir = self.get_bundle_dir()
            bundle_dir.mkdir(parents=True, exist_ok=True)
            self.cleanup_expired_bundles(bundle_dir, config)

            payload = data or json.load(sys.stdin)
            session_id = self.get_session_id_from_data(payload)
            existing_bundle_file = self.find_existing_session_file(
                bundle_dir, session_id
            )
            new_filename = self.generate_bundle_filename(session_id)
            new_bundle_file = bundle_dir / new_filename

            if existing_bundle_file and existing_bundle_file.exists():
                with open(existing_bundle_file) as file_handle:
                    entries = json.load(file_handle)

                if existing_bundle_file.name != new_filename:
                    bundle_file = new_bundle_file
                    should_rename = True
                    old_bundle_file = existing_bundle_file
                else:
                    bundle_file = existing_bundle_file
                    should_rename = False
                    old_bundle_file = None
            else:
                bundle_file = new_bundle_file
                entries = []
                should_rename = False
                old_bundle_file = None

            entry = {
                "timestamp": datetime.now().isoformat() + "Z",
                "command": None,
                "prompt": None,
                "description": None,
            }

            if event_type == "post-tool":
                if not self.apply_post_tool(entry, payload, config):
                    return
            elif event_type == "user-prompt":
                if not self.apply_user_prompt(entry, payload, config):
                    return
            elif event_type == "session-start":
                if not self.apply_session(entry, payload, config):
                    return
            else:
                return

            cleaned_entry = {
                key: value for key, value in entry.items() if value is not None
            }
            if len(cleaned_entry) <= 1:
                return

            entries.append(cleaned_entry)
            with open(bundle_file, "w") as file_handle:
                json.dump(entries, file_handle, indent=2)

            if should_rename and old_bundle_file and old_bundle_file.exists():
                with contextlib.suppress(Exception):
                    old_bundle_file.unlink()

            self.add_conversation_link(bundle_file, session_id, config)
        except Exception:
            # Silent fail - do not interrupt IDE flow
            pass

    def apply_post_tool(
        self,
        entry: dict[str, Any],
        payload: dict[str, Any],
        config: dict[str, Any],
    ) -> bool:
        tool_name = payload.get("tool_name", "").lower()
        entry["operation"] = tool_name

        if self.should_exclude_operation(tool_name, config):
            return False

        tool_input = payload.get("tool_input")
        if not isinstance(tool_input, dict):
            return True

        file_path = tool_input.get("file_path")
        if isinstance(file_path, str):
            if self.should_exclude_by_string_pattern(file_path, config):
                return False

            entry["file_path"] = self.redact_if_available(file_path, config)
            if self.is_operation_seen(tool_name, file_path):
                return False

        if tool_name == "bash":
            command = tool_input.get("command")
            if isinstance(command, str):
                if self.should_exclude_bash_command(command, config):
                    return False

                if self.should_exclude_by_string_pattern(command, config):
                    return False

                entry["command"] = self.redact_if_available(command, config)

            description = tool_input.get("description")
            if isinstance(description, str):
                entry["description"] = description

        truncation_limit = config.get("truncation_limits", {}).get(
            "edit_string_max_length", 1000
        )
        if tool_name == "edit":
            old_string = tool_input.get("old_string", "")
            new_string = tool_input.get("new_string", "")
            if not isinstance(old_string, str) or not isinstance(new_string, str):
                return True

            if len(old_string) > truncation_limit or len(new_string) > truncation_limit:
                entry["old_string"] = self._build_truncated_preview(old_string, config)
                entry["new_string"] = self._build_truncated_preview(new_string, config)
            else:
                entry["old_string"] = self.redact_if_available(old_string, config)
                entry["new_string"] = self.redact_if_available(new_string, config)
        else:
            for field in ["pattern", "url", "target"]:
                value = tool_input.get(field)
                if isinstance(value, str):
                    entry[field] = value

        return True

    def apply_user_prompt(
        self,
        entry: dict[str, Any],
        payload: dict[str, Any],
        config: dict[str, Any],
    ) -> bool:
        full_prompt = payload.get("prompt", "")
        if not isinstance(full_prompt, str):
            return False

        if self.should_exclude_prompt(full_prompt, config):
            return False

        prompt_limit = config.get("truncation_limits", {}).get("prompt_max_length", 100)
        redacted_prompt = self.redact_if_available(full_prompt, config)

        if len(redacted_prompt) > prompt_limit:
            entry["prompt"] = redacted_prompt[:prompt_limit] + "..."
        else:
            entry["prompt"] = redacted_prompt

        entry["operation"] = "prompt"
        return True

    def apply_session(
        self,
        entry: dict[str, Any],
        payload: dict[str, Any],
        config: dict[str, Any],
    ) -> bool:
        if self.should_exclude_operation("session_start", config):
            return False

        entry["operation"] = "session_start"
        entry["source"] = payload.get("source", "unknown")
        return True

    def _build_truncated_preview(
        self, value: str, config: dict[str, Any]
    ) -> dict[str, Any]:
        preview = value[:50] + "..." if len(value) > 50 else value
        return {
            "truncated": True,
            "size": len(value),
            "preview": self.redact_if_available(preview, config),
        }

    def load_config(self) -> dict[str, Any]:
        try:
            project_dir = self.get_project_dir()
            config_path = (
                Path(project_dir)
                / self.paths.context_dir_name
                / "hooks"
                / "context_capture_config.json"
            )
            if config_path.exists():
                with open(config_path) as file_handle:
                    return json.load(file_handle)
        except Exception:
            pass

        return {
            "excluded_operations": ["session_start", "task", "glob"],
            "excluded_bash_commands": [
                "ls",
                "pwd",
                "cd",
                "git status",
                "git log",
                "git diff",
                "git show",
                "git branch",
            ],
            "excluded_prompt_patterns": [],
            "excluded_string_patterns": [
                "__pycache__",
                ".pyc",
                "node_modules/",
                ".git/objects/",
                "/tmp/",
                ".cache/",
            ],
            "redaction": {
                "enabled": True,
                "patterns": {
                    "env_vars": True,
                    "api_keys": True,
                    "passwords": True,
                    "urls_with_auth": True,
                    "json_secrets": True,
                },
                "preserve_structure": True,
                "custom_patterns": [],
            },
            "truncation_limits": {
                "prompt_max_length": 100,
                "edit_string_max_length": 1000,
                "bundle_size_threshold": 10240,
            },
            "retention": {
                "days_to_retain": 7,
                "auto_cleanup": True,
            },
        }

    def should_exclude_operation(self, operation: str, config: dict[str, Any]) -> bool:
        return operation in config.get("excluded_operations", [])

    def should_exclude_bash_command(self, command: str, config: dict[str, Any]) -> bool:
        excluded_commands = config.get("excluded_bash_commands", [])
        command_lower = command.lower().strip()
        for excluded in excluded_commands:
            if command_lower.startswith(str(excluded).lower()):
                return True
        return False

    def should_exclude_prompt(self, prompt: str, config: dict[str, Any]) -> bool:
        excluded_patterns = config.get("excluded_prompt_patterns", [])
        prompt_text = prompt.strip()
        for pattern in excluded_patterns:
            if str(pattern).lower() in prompt_text.lower():
                return True
        return False

    def should_exclude_by_string_pattern(
        self, value: str, config: dict[str, Any]
    ) -> bool:
        if not value or not isinstance(value, str):
            return False
        excluded_patterns = config.get("excluded_string_patterns", [])
        value_lower = value.lower()
        return any(str(pattern).lower() in value_lower for pattern in excluded_patterns)

    def redact_if_available(self, text: str, config: dict[str, Any]) -> str:
        if not text or not isinstance(text, str):
            return text

        redaction_config = config.get("redaction", {})
        if not redaction_config.get("enabled", True):
            return text

        if _redact_sensitive_data is not None:
            return _redact_sensitive_data(text, redaction_config)
        return text

    def is_operation_seen(self, operation: str, file_path: str) -> bool:
        key = (operation, file_path)
        if key in self.seen_operations:
            return True
        self.seen_operations.add(key)
        return False

    def cleanup_expired_bundles(self, bundle_dir: Path, config: dict[str, Any]) -> None:
        try:
            retention_config = config.get("retention", {})
            if not retention_config.get("auto_cleanup", True):
                return

            days_to_retain = retention_config.get("days_to_retain", 7)
            if days_to_retain <= 0:
                return

            now = datetime.now()
            cutoff_date = now - timedelta(days=days_to_retain)
            if not bundle_dir.exists():
                return

            for bundle_file in bundle_dir.glob("*.json"):
                try:
                    day_num = self.parse_bundle_date(bundle_file.name)
                    if day_num is None:
                        continue

                    file_mtime = datetime.fromtimestamp(bundle_file.stat().st_mtime)
                    if file_mtime < cutoff_date:
                        bundle_file.unlink()
                        continue

                    # Remove the day_num check - rely on mtime only
                    # The previous condition already handles expired files
                except Exception:
                    continue
        except Exception:
            pass

    def add_conversation_link(
        self,
        bundle_file: Path,
        session_id: str,
        config: dict[str, Any],
    ) -> None:
        try:
            if not bundle_file.exists():
                return

            file_size = bundle_file.stat().st_size
            threshold = config.get("truncation_limits", {}).get(
                "bundle_size_threshold", 10240
            )
            if file_size <= threshold:
                return

            project_dir = self.get_project_dir()
            conversation_path = (
                Path.home()
                / self.paths.context_dir_name
                / "projects"
                / f"-Users-{os.getenv('USER', 'user')}-{project_dir.replace('/', '-')}"
                / f"{session_id}.jsonl"
            )

            if not conversation_path.exists():
                return

            with open(bundle_file) as file_handle:
                entries = json.load(file_handle)

            if entries and "conversation_file" not in entries[0]:
                entries[0]["conversation_file"] = str(conversation_path)
                with open(bundle_file, "w") as file_handle:
                    json.dump(entries, file_handle, indent=2)
        except Exception:
            pass

    def parse_bundle_date(self, filename: str) -> int | None:
        try:
            parts = filename.split("_")
            if len(parts) >= 2:
                return int(parts[1])
        except (ValueError, IndexError):
            return None
        return None

    def find_existing_session_file(
        self, bundle_dir: Path, session_id: str
    ) -> Path | None:
        try:
            for bundle_file in bundle_dir.glob("*.json"):
                if bundle_file.name.endswith(f"_{session_id}.json"):
                    return bundle_file
        except Exception:
            pass
        return None

    def generate_bundle_filename(self, session_id: str) -> str:
        now = datetime.now()
        day_name = now.strftime("%a").upper()[:3]
        day_num = now.strftime("%d")
        timestamp = now.strftime("%H%M%S")
        return f"{day_name}_{day_num}_{timestamp}_{session_id}.json"

    def get_session_id_from_data(self, data: dict[str, Any]) -> str:
        session_id = data.get("session_id")
        if isinstance(session_id, str) and session_id:
            return session_id
        return datetime.now().strftime("%H%M%S%f")

    def get_bundle_dir(self) -> Path:
        return (
            Path(self.get_project_dir())
            / self.paths.context_dir_name
            / "agents"
            / "context_bundles"
        )

    def get_project_dir(self) -> str:
        return os.environ.get(self.paths.project_dir_env, ".")


def capture_from_stdin(
    project_dir_env: str, context_dir_name: str, event_type: str
) -> None:
    """Wrap CLI scripts for convenience."""
    runner = ContextCaptureRunner(
        ContextCapturePaths(
            project_dir_env=project_dir_env,
            context_dir_name=context_dir_name,
        )
    )
    runner.capture_action(event_type)
