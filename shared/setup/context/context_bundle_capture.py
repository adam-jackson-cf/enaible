#!/usr/bin/env python3
"""Context bundle capture for Claude Code session tracking."""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

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
        "truncation_limits": {
            "prompt_max_length": 100,
            "edit_string_max_length": 1000,
            "bundle_size_threshold": 10240,
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

    for pattern in excluded_patterns:
        if pattern.lower() in prompt_text.lower():
            return True
    return False


def is_operation_seen(operation, file_path):
    """Check if operation on file has already been captured."""
    global seen_operations
    operation_key = (operation, file_path)
    if operation_key in seen_operations:
        return True
    seen_operations.add(operation_key)
    return False


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

        # Read hook data from stdin
        data = json.load(sys.stdin)

        # Create context bundle directory
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
        bundle_dir = Path(project_dir) / ".claude" / "agents" / "context_bundles"
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename using Claude's session ID: DAY_DD_SESSIONID.json
        now = datetime.now()
        day_name = now.strftime("%a").upper()[:3]  # MON, TUE, etc.
        day_num = now.strftime("%d")
        session_id = get_session_id_from_data(data)
        filename = f"{day_name}_{day_num}_{session_id}.json"
        bundle_file = bundle_dir / filename

        # Load existing or create new
        if bundle_file.exists():
            with open(bundle_file) as f:
                entries = json.load(f)
        else:
            entries = []

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
                    entry["file_path"] = tool_input["file_path"]

                    # Check for duplicate operations on same file
                    if is_operation_seen(tool_name, tool_input["file_path"]):
                        return

                # Bash commands
                if tool_name == "bash" and "command" in tool_input:
                    command = tool_input["command"]

                    # Check if bash command should be excluded
                    if should_exclude_bash_command(command, config):
                        return

                    entry["command"] = command
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
                        entry["old_string"] = {
                            "truncated": True,
                            "size": len(old_string),
                            "preview": old_string[:50] + "..."
                            if len(old_string) > 50
                            else old_string,
                        }
                        entry["new_string"] = {
                            "truncated": True,
                            "size": len(new_string),
                            "preview": new_string[:50] + "..."
                            if len(new_string) > 50
                            else new_string,
                        }
                    else:
                        entry["old_string"] = old_string
                        entry["new_string"] = new_string
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

            if len(full_prompt) > prompt_limit:
                entry["prompt"] = full_prompt[:prompt_limit] + "..."
            else:
                entry["prompt"] = full_prompt

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

            # Check if we should add conversation link
            session_id = get_session_id_from_data(data)
            add_conversation_link(bundle_file, session_id, config)

    except Exception:
        # Silent fail - don't interrupt Claude's flow
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        capture_action(sys.argv[1])
