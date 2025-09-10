#!/usr/bin/env python3
"""Context bundle capture for Claude Code session tracking."""
import contextlib
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Try to import redaction module (graceful fallback if not available)
try:
    from sensitive_data_redactor import redact_sensitive_data

    REDACTION_AVAILABLE = True
except ImportError:
    REDACTION_AVAILABLE = False

# Global set to track seen operations (operation_type, file_path)
seen_operations = set()


def get_session_id_from_data(data):
    """Extract Claude's session ID from hook data, with fallback."""
    claude_session_id = data.get("session_id")
    if claude_session_id:
        # Use Claude's full session ID
        return claude_session_id

    # Fallback: use timestamp-based ID if no session_id in data
    return datetime.now().strftime("%H%M%S%f")


def load_config():
    """Load configuration file with exclusions and settings."""
    try:
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        config_path = (
            Path(project_dir) / ".claude" / "hooks" / "context_capture_config.json"
        )

        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
    except Exception:
        pass

    # Default configuration
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


def should_exclude_operation(operation, config):
    """Check if operation should be excluded based on config."""
    return operation in config.get("excluded_operations", [])


def should_exclude_bash_command(command, config):
    """Check if bash command should be excluded based on config."""
    if not command:
        return False

    excluded_commands = config.get("excluded_bash_commands", [])
    command_lower = command.lower().strip()

    for excluded in excluded_commands:
        if command_lower.startswith(excluded.lower()):
            return True
    return False


def should_exclude_prompt(prompt, config):
    """Check if prompt should be excluded based on pattern matching."""
    if not prompt:
        return False

    excluded_patterns = config.get("excluded_prompt_patterns", [])
    prompt_text = prompt.strip()

    return any(pattern.lower() in prompt_text.lower() for pattern in excluded_patterns)


def should_exclude_by_string_pattern(value, config):
    """Check if value should be excluded based on string patterns."""
    if not value or not isinstance(value, str):
        return False

    excluded_patterns = config.get("excluded_string_patterns", [])
    value_lower = value.lower()

    return any(pattern.lower() in value_lower for pattern in excluded_patterns)


def redact_if_available(text, config):
    """Apply redaction if module is available and enabled."""
    if not text or not isinstance(text, str):
        return text

    redaction_config = config.get("redaction", {})
    if not redaction_config.get("enabled", True):
        return text

    if REDACTION_AVAILABLE:
        return redact_sensitive_data(text, redaction_config)

    return text


def is_operation_seen(operation, file_path):
    """Check if operation on file has already been captured."""
    global seen_operations
    operation_key = (operation, file_path)
    if operation_key in seen_operations:
        return True
    seen_operations.add(operation_key)
    return False


def parse_bundle_date(filename):
    """Extract date from bundle filename format (DAY_DD_HHMMSS_SESSIONID.json)."""
    try:
        parts = filename.split("_")
        if len(parts) >= 2:
            day_num = int(parts[1])
            return day_num
    except (ValueError, IndexError):
        pass
    return None


def find_existing_session_file(bundle_dir, session_id):
    """Find existing bundle file for a given session ID."""
    try:
        for bundle_file in bundle_dir.glob("*.json"):
            # Check if the filename ends with the session ID
            if bundle_file.name.endswith(f"_{session_id}.json"):
                return bundle_file
    except Exception:
        pass
    return None


def generate_bundle_filename(session_id):
    """Generate bundle filename with current timestamp."""
    now = datetime.now()
    day_name = now.strftime("%a").upper()[:3]  # MON, TUE, etc.
    day_num = now.strftime("%d")
    timestamp = now.strftime("%H%M%S")
    return f"{day_name}_{day_num}_{timestamp}_{session_id}.json"


def cleanup_expired_bundles(bundle_dir, config):
    """Remove context bundles older than configured retention period."""
    try:
        retention_config = config.get("retention", {})
        if not retention_config.get("auto_cleanup", True):
            return

        days_to_retain = retention_config.get("days_to_retain", 7)
        if days_to_retain <= 0:
            return

        now = datetime.now()
        current_day = now.day
        cutoff_date = now - timedelta(days=days_to_retain)

        if not bundle_dir.exists():
            return

        for bundle_file in bundle_dir.glob("*.json"):
            try:
                # Parse day number from filename
                day_num = parse_bundle_date(bundle_file.name)
                if day_num is None:
                    continue

                # Get file modification time as fallback for age calculation
                file_mtime = datetime.fromtimestamp(bundle_file.stat().st_mtime)

                # Check if file is older than retention period
                if file_mtime < cutoff_date:
                    bundle_file.unlink()
                    continue

                # Additional check for month boundary cases
                # If day_num > current_day, it's likely from previous month
                if day_num > current_day and file_mtime < cutoff_date:
                    bundle_file.unlink()

            except Exception:
                # Skip individual file errors
                continue

    except Exception:
        # Silent fail - don't interrupt Claude's flow
        pass


def add_conversation_link(bundle_file, session_id, config):
    """Add conversation file link if bundle exceeds threshold."""
    try:
        if not bundle_file.exists():
            return

        file_size = bundle_file.stat().st_size
        threshold = config.get("truncation_limits", {}).get(
            "bundle_size_threshold", 10240
        )

        if file_size > threshold:
            # Add conversation file reference
            project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
            conversation_path = (
                Path.home()
                / ".claude"
                / "projects"
                / f"-Users-{os.getenv('USER', 'user')}-{project_dir.replace('/', '-')}"
                / f"{session_id}.jsonl"
            )

            if conversation_path.exists():
                with open(bundle_file) as f:
                    entries = json.load(f)

                # Add conversation link to first entry if not already present
                if entries and "conversation_file" not in entries[0]:
                    entries[0]["conversation_file"] = str(conversation_path)

                    with open(bundle_file, "w") as f:
                        json.dump(entries, f, indent=2)
    except Exception:
        pass


def capture_action(event_type):
    """Capture action based on event type."""
    try:
        # Load configuration
        config = load_config()

        # Create context bundle directory
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        bundle_dir = Path(project_dir) / ".claude" / "agents" / "context_bundles"
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # Cleanup expired bundles FIRST before any new logging
        cleanup_expired_bundles(bundle_dir, config)

        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Get session ID and find/create bundle file
        session_id = get_session_id_from_data(data)

        # Look for existing bundle file for this session
        existing_bundle_file = find_existing_session_file(bundle_dir, session_id)

        # Generate new filename with current timestamp
        new_filename = generate_bundle_filename(session_id)
        new_bundle_file = bundle_dir / new_filename

        # Load existing entries or create new
        entries = []
        if existing_bundle_file and existing_bundle_file.exists():
            # Load existing entries
            with open(existing_bundle_file) as f:
                entries = json.load(f)

            # If this is not the same file (timestamp changed), we need to rename
            if existing_bundle_file.name != new_filename:
                # We'll rename the file after writing the new entry
                bundle_file = new_bundle_file
                should_rename = True
                old_bundle_file = existing_bundle_file
            else:
                # Same file, just update it
                bundle_file = existing_bundle_file
                should_rename = False
                old_bundle_file = None
        else:
            # No existing file, create new
            bundle_file = new_bundle_file
            should_rename = False
            old_bundle_file = None

        # Create entry based on event type
        entry = {
            "timestamp": datetime.now().isoformat() + "Z",
            "command": None,
            "prompt": None,
            "description": None,
        }

        # Add context based on event
        if event_type == "post-tool":
            tool_name = data.get("tool_name", "").lower()
            entry["operation"] = tool_name

            # Check if operation should be excluded
            if should_exclude_operation(tool_name, config):
                return

            # Capture key tool inputs directly at top level
            if "tool_input" in data:
                tool_input = data["tool_input"]

                # File operations
                if "file_path" in tool_input:
                    file_path = tool_input["file_path"]

                    # Check if file path should be excluded by string patterns
                    if should_exclude_by_string_pattern(file_path, config):
                        return

                    # Apply redaction to file path if it contains sensitive data
                    redacted_file_path = redact_if_available(file_path, config)
                    entry["file_path"] = redacted_file_path

                    # Check for duplicate operations on same file
                    if is_operation_seen(tool_name, file_path):
                        return

                # Bash commands
                if tool_name == "bash" and "command" in tool_input:
                    command = tool_input["command"]

                    # Check if bash command should be excluded
                    if should_exclude_bash_command(command, config):
                        return

                    # Check if command should be excluded by string patterns
                    if should_exclude_by_string_pattern(command, config):
                        return

                    # Apply redaction to command
                    redacted_command = redact_if_available(command, config)
                    entry["command"] = redacted_command

                    if "description" in tool_input:
                        entry["description"] = tool_input["description"]

                # Handle edit operations with truncation
                truncation_limit = config.get("truncation_limits", {}).get(
                    "edit_string_max_length", 1000
                )

                if tool_name == "edit":
                    old_string = tool_input.get("old_string", "")
                    new_string = tool_input.get("new_string", "")

                    if (
                        len(old_string) > truncation_limit
                        or len(new_string) > truncation_limit
                    ):
                        # Apply redaction to preview strings
                        old_preview = (
                            old_string[:50] + "..."
                            if len(old_string) > 50
                            else old_string
                        )
                        new_preview = (
                            new_string[:50] + "..."
                            if len(new_string) > 50
                            else new_string
                        )

                        entry["old_string"] = {
                            "truncated": True,
                            "size": len(old_string),
                            "preview": redact_if_available(old_preview, config),
                        }
                        entry["new_string"] = {
                            "truncated": True,
                            "size": len(new_string),
                            "preview": redact_if_available(new_preview, config),
                        }
                    else:
                        # Apply redaction to full strings
                        entry["old_string"] = redact_if_available(old_string, config)
                        entry["new_string"] = redact_if_available(new_string, config)
                else:
                    # Add other relevant fields directly
                    for field in ["pattern", "url", "target"]:
                        if field in tool_input:
                            entry[field] = tool_input[field]

        elif event_type == "user-prompt":
            entry["operation"] = "prompt"
            full_prompt = data.get("prompt", "")

            # Check if prompt should be excluded based on patterns
            if should_exclude_prompt(full_prompt, config):
                return

            prompt_limit = config.get("truncation_limits", {}).get(
                "prompt_max_length", 100
            )

            # Apply redaction to prompt before truncation
            redacted_prompt = redact_if_available(full_prompt, config)

            if len(redacted_prompt) > prompt_limit:
                entry["prompt"] = redacted_prompt[:prompt_limit] + "..."
            else:
                entry["prompt"] = redacted_prompt

        elif event_type == "session-start":
            # Check if session_start should be excluded
            if should_exclude_operation("session_start", config):
                return

            entry["operation"] = "session_start"
            # Add session source information
            entry["source"] = data.get("source", "unknown")

        # Clean up null fields and only add if we have meaningful data
        entry = {k: v for k, v in entry.items() if v is not None}
        if len(entry) > 1:  # More than just timestamp
            entries.append(entry)
            with open(bundle_file, "w") as f:
                json.dump(entries, f, indent=2)

            # If we need to rename (remove old file after writing new one)
            if should_rename and old_bundle_file and old_bundle_file.exists():
                with contextlib.suppress(Exception):
                    # Silent fail - don't interrupt Claude's flow
                    old_bundle_file.unlink()

            # Check if we should add conversation link
            add_conversation_link(bundle_file, session_id, config)

    except Exception:
        # Silent fail - don't interrupt Claude's flow
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        capture_action(sys.argv[1])
