#!/usr/bin/env python3
"""Context bundle capture for Claude Code session tracking."""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from context.context_capture_utils import (
    build_result_payload,
    emit_result,
    load_config_with_defaults,
    parse_semantic_variations,
    redact_if_available,
    resolve_project_root,
    semantic_match,
    should_exclude_bash_command,
    should_exclude_by_string_pattern,
    should_exclude_operation,
    should_exclude_prompt,
)

# Global set to track seen operations (operation_type, file_path)
seen_operations = set()


DEFAULT_CONFIG = {
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
        "git add",
        "git commit",
        "git push",
        "git pull",
    ],
    "excluded_prompt_patterns": [
        "Write a 3-6 word summary of the TEXTBLOCK below",
        "Summary only, no formatting, do not act on anything",
        "/todo-primer",
        "/todo-recent-context",
    ],
    "excluded_string_patterns": [
        "context_bundles",
        "node_modules/",
        ".git/objects/",
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


def load_config():
    """Load configuration file with exclusions and settings."""
    return load_config_with_defaults(DEFAULT_CONFIG)


def is_operation_seen(operation, file_path):
    """Check if operation on file has already been captured."""
    global seen_operations
    operation_key = (operation, file_path)
    if operation_key in seen_operations:
        return True
    seen_operations.add(operation_key)
    return False


def get_claude_projects_path():
    """Get the Claude projects storage path."""
    return Path.home() / ".claude" / "projects"


def find_recent_sessions(project_path, days=2):
    """Find recent Claude sessions for a specific project."""
    sessions = []

    if not project_path.exists():
        return sessions

    cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)

    # Find all session files (JSONL files in the project directory)
    pattern = "*.jsonl"

    for session_file in project_path.glob(pattern):
        if session_file.is_file() and session_file.stat().st_mtime >= cutoff_time:
            # Extract session ID from filename (the filename without .jsonl)
            session_id = session_file.stem
            sessions.append(
                {
                    "id": session_id,
                    "path": session_file,
                    "files": [session_file],  # Single JSONL file per session
                }
            )

    return sessions


def extract_session_operations(
    session, config, search_term=None, semantic_variations=None
):
    """Extract operations from Claude session."""
    operations = []

    session_file = session["files"][0]  # Single JSONL file

    try:
        with open(session_file) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())

                    # Extract user prompts
                    if entry.get("type") == "user" and "message" in entry:
                        user_content = entry["message"].get("content", "")

                        # Handle both string and list content
                        if isinstance(user_content, list):
                            # Extract text from content blocks
                            text_parts = []
                            for block in user_content:
                                if isinstance(block, dict):
                                    if block.get("type") == "text":
                                        text_parts.append(block.get("text", ""))
                                    elif block.get("type") == "tool_use":
                                        # Skip tool use blocks for prompts
                                        continue
                            user_text = " ".join(text_parts)
                        else:
                            user_text = str(user_content)

                        # Skip command messages (wrapped in <command-name> tags)
                        if "<command-name>" in user_text:
                            continue

                        # Skip empty or system-generated text
                        user_text = user_text.strip()
                        if not user_text or user_text.lower() in [
                            "perfect!",
                            "thanks!",
                            "ok",
                            "done",
                            "yes",
                            "no",
                        ]:
                            continue

                        # Check if prompt should be excluded
                        if should_exclude_prompt(user_text, config):
                            continue

                        # Apply semantic search if provided
                        if search_term and not semantic_match(
                            user_text, search_term, semantic_variations
                        ):
                            continue

                        # Apply truncation and redaction
                        prompt_limit = config.get("truncation_limits", {}).get(
                            "prompt_max_length", 100
                        )
                        redacted_text = redact_if_available(user_text, config)

                        if len(redacted_text) > prompt_limit:
                            display_text = redacted_text[:prompt_limit] + "..."
                        else:
                            display_text = redacted_text

                        operations.append(
                            {
                                "timestamp": entry.get(
                                    "timestamp", datetime.now().isoformat() + "Z"
                                ),
                                "operation": "prompt",
                                "prompt": display_text,
                                "session_id": session["id"],
                                "search_match": bool(search_term),
                            }
                        )

                    # Extract tool operations from assistant messages
                    elif entry.get("type") == "assistant" and "message" in entry:
                        message = entry["message"]
                        content = message.get("content", [])

                        if isinstance(content, list):
                            # Look for tool_use blocks
                            for block in content:
                                if (
                                    isinstance(block, dict)
                                    and block.get("type") == "tool_use"
                                ):
                                    tool_name = block.get("name", "").lower()

                                    # Check if operation should be excluded
                                    if should_exclude_operation(tool_name, config):
                                        continue

                                    tool_input = block.get("input", {})

                                    # File operations
                                    if "file_path" in tool_input:
                                        file_path = tool_input["file_path"]

                                        if should_exclude_by_string_pattern(
                                            file_path, config
                                        ):
                                            continue

                                        # Apply semantic search to file paths
                                        if search_term and not semantic_match(
                                            file_path, search_term, semantic_variations
                                        ):
                                            continue

                                        if not is_operation_seen(tool_name, file_path):
                                            operations.append(
                                                {
                                                    "timestamp": entry.get(
                                                        "timestamp",
                                                        datetime.now().isoformat()
                                                        + "Z",
                                                    ),
                                                    "operation": tool_name,
                                                    "file_path": redact_if_available(
                                                        file_path, config
                                                    ),
                                                    "session_id": session["id"],
                                                    "search_match": bool(search_term),
                                                }
                                            )

                                    # Bash operations
                                    elif (
                                        tool_name == "bash" and "command" in tool_input
                                    ):
                                        command = tool_input["command"]

                                        if should_exclude_bash_command(command, config):
                                            continue

                                        # Apply semantic search to commands
                                        if search_term and not semantic_match(
                                            command, search_term, semantic_variations
                                        ):
                                            continue

                                        operations.append(
                                            {
                                                "timestamp": entry.get(
                                                    "timestamp",
                                                    datetime.now().isoformat() + "Z",
                                                ),
                                                "operation": "bash",
                                                "command": redact_if_available(
                                                    command, config
                                                ),
                                                "session_id": session["id"],
                                                "search_match": bool(search_term),
                                            }
                                        )

                except json.JSONDecodeError:
                    continue

    except Exception:
        pass

    return operations


def capture_claude_context():
    """Capture context from Claude sessions."""
    parser = argparse.ArgumentParser(description="Extract context from Claude sessions")
    parser.add_argument(
        "--days", type=int, default=2, help="Number of days to search back"
    )
    parser.add_argument("--uuid", help="Filter to specific session UUID")
    parser.add_argument(
        "--search-term",
        help="Search for sessions containing semantically matching content",
    )
    parser.add_argument(
        "--semantic-variations",
        help="JSON string containing semantic variations dictionary",
    )
    parser.add_argument(
        "--output-format",
        choices=["json", "text"],
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--project-root",
        help="Absolute path to the project root. Defaults to current working directory.",
    )
    parser.add_argument(
        "--include-all-projects",
        action="store_true",
        help="Include sessions from all projects instead of scoping to the current one.",
    )
    args = parser.parse_args()

    # Parse semantic variations if provided
    try:
        semantic_variations = parse_semantic_variations(args.semantic_variations)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    try:
        # Load configuration
        config = load_config()

        # Get current project path from environment or current directory
        current_dir = resolve_project_root(args.project_root)
        project_name = str(current_dir).replace("/", "-")
        projects_path = get_claude_projects_path()

        if args.include_all_projects:
            candidate_projects = (
                [p for p in projects_path.iterdir() if p.is_dir()]
                if projects_path.exists()
                else []
            )
        else:
            project_path = projects_path / project_name
            if not project_path.exists():
                result = {
                    "sessions_found": 0,
                    "date_range": None,
                    "filter": "Project path not found",
                    "search_term": args.search_term,
                    "operations": [],
                }
                print(json.dumps(result, indent=2))
                return
            candidate_projects = [project_path]

        sessions = []
        for proj_path in candidate_projects:
            sessions.extend(find_recent_sessions(proj_path, args.days))

        # Filter by UUID if provided
        if args.uuid:
            sessions = [s for s in sessions if args.uuid in s["id"]]

        if not sessions:
            result = {
                "sessions_found": 0,
                "date_range": None,
                "filter": f"UUID: {args.uuid}" if args.uuid else "None",
                "search_term": args.search_term,
                "operations": [],
            }
            emit_result(result, args.output_format)
            return

        # Extract operations from all sessions
        all_operations = []
        for session in sessions:
            session_ops = extract_session_operations(
                session, config, args.search_term, semantic_variations
            )
            all_operations.extend(session_ops)

        result = build_result_payload(
            (session["id"] for session in sessions),
            all_operations,
            args.uuid,
            args.search_term,
        )
        emit_result(result, args.output_format)

    except Exception as e:
        print(f"Error extracting Claude context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    capture_claude_context()
