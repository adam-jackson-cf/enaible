"""Context bundle capture for OpenCode session tracking."""
import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from context.context_capture_utils import (
    build_result_payload,
    emit_result,
    load_config_with_defaults,
    normalize_path,
    parse_semantic_variations,
    redact_if_available,
    resolve_project_root,
    semantic_match,
    should_exclude_bash_command,
    should_exclude_by_string_pattern,
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
        # Silent fail - don't interrupt flow
        pass


def get_opencode_storage_path():
    """Get the OpenCode storage path."""
    return Path.home() / ".local" / "share" / "opencode" / "storage"


def resolve_project_id(storage_path: Path, project_root: Path) -> str | None:
    project_dir = storage_path / "project"
    if not project_dir.exists():
        return None
    for project_file in project_dir.glob("*.json"):
        try:
            with open(project_file) as pf:
                data = json.load(pf)
        except Exception:
            continue
        worktree = normalize_path(data.get("worktree"))
        if worktree and worktree == project_root:
            return data.get("id")
    return None


def find_recent_sessions(storage_path, project_id, project_root, days=2):
    """Find recent OpenCode sessions for the active project."""
    sessions = []
    if not project_id:
        return sessions

    session_dir = storage_path / "session" / project_id
    message_root = storage_path / "message"
    if not session_dir.exists() or not message_root.exists():
        return sessions

    cutoff_time = datetime.now().timestamp() - (days * 24 * 3600)

    for session_meta in session_dir.glob("ses_*.json"):
        try:
            with open(session_meta) as sm:
                meta = json.load(sm)
        except Exception:
            continue

        session_directory = normalize_path(meta.get("directory"))
        if session_directory != project_root:
            continue

        updated_ms = meta.get("time", {}).get("updated")
        created_ms = meta.get("time", {}).get("created")
        latest_ms = updated_ms or created_ms
        if latest_ms is not None:
            latest_ts = latest_ms / 1000
        else:
            latest_ts = session_meta.stat().st_mtime

        if latest_ts < cutoff_time:
            continue

        session_id = meta.get("id") or session_meta.stem
        message_dir = message_root / session_id
        if not message_dir.exists():
            continue

        recent_files = [
            f for f in message_dir.glob("*.json") if f.stat().st_mtime >= cutoff_time
        ]
        if not recent_files:
            continue

        sessions.append(
            {
                "id": session_id,
                "path": message_dir,
                "files": recent_files,
                "cwd": session_directory,
            }
        )

    return sessions


def extract_session_operations(
    session, config, search_term=None, semantic_variations=None
):
    """Extract operations from OpenCode session."""
    operations = []

    # Process message files
    for msg_file in session["files"]:
        try:
            with open(msg_file) as f:
                msg_data = json.load(f)

            # Extract user prompts from text parts
            if msg_data.get("role") == "user":
                # Look for corresponding text parts
                part_path = get_opencode_storage_path() / "part" / msg_data["id"]
                if part_path.exists():
                    for part_file in part_path.glob("prt_*.json"):
                        try:
                            with open(part_file) as pf:
                                part_data = json.load(pf)

                            if part_data.get("type") == "text":
                                text = part_data.get("text", "")

                                # Skip empty or system-generated text
                                text = text.strip()
                                if not text or text.lower() in [
                                    "perfect!",
                                    "thanks!",
                                    "ok",
                                    "done",
                                    "yes",
                                    "no",
                                ]:
                                    continue

                                # Check if prompt should be excluded
                                if should_exclude_prompt(text, config):
                                    continue

                                # Apply semantic search if provided
                                if search_term and not semantic_match(
                                    text, search_term, semantic_variations
                                ):
                                    continue

                                # Apply truncation and redaction
                                prompt_limit = config.get("truncation_limits", {}).get(
                                    "prompt_max_length", 100
                                )
                                redacted_text = redact_if_available(text, config)

                                if len(redacted_text) > prompt_limit:
                                    display_text = redacted_text[:prompt_limit] + "..."
                                else:
                                    display_text = redacted_text

                                operations.append(
                                    {
                                        "timestamp": datetime.fromtimestamp(
                                            part_data.get("time", {}).get(
                                                "start", time.time()
                                            )
                                        ).isoformat()
                                        + "Z",
                                        "operation": "prompt",
                                        "prompt": display_text,
                                        "session_id": session["id"],
                                        "search_match": bool(search_term),
                                    }
                                )
                        except Exception:
                            continue

            # Extract file operations from assistant messages
            elif msg_data.get("role") == "assistant":
                # Look for tool calls in the message
                content = json.dumps(msg_data).lower()

                # Skip system messages and large content (mostly system prompts)
                if len(content) > 10000 and "system" in content:
                    continue

                # Look for file operation patterns in the JSON content
                import re

                # Check for semantic match in assistant messages if search term provided
                if search_term and not semantic_match(
                    content, search_term, semantic_variations
                ):
                    continue

                # Read operations
                if '"read"' in content and '"file_path"' in content:
                    # Extract file paths using regex
                    file_path_matches = re.findall(
                        r'"file_path"\s*:\s*"([^"]+)"', msg_data.get("content", "")
                    )
                    for file_path in file_path_matches:
                        if should_exclude_by_string_pattern(file_path, config):
                            continue

                        # Apply semantic search to file paths
                        if search_term and not semantic_match(
                            file_path, search_term, semantic_variations
                        ):
                            continue

                        if not is_operation_seen("read", file_path):
                            operations.append(
                                {
                                    "timestamp": datetime.fromtimestamp(
                                        msg_data.get("time", {}).get("created", 0)
                                    ).isoformat()
                                    + "Z",
                                    "operation": "read",
                                    "file_path": redact_if_available(file_path, config),
                                    "session_id": session["id"],
                                    "search_match": bool(search_term),
                                }
                            )

                # Write operations
                if '"write"' in content or '"edit"' in content:
                    file_path_matches = re.findall(
                        r'"file_path"\s*:\s*"([^"]+)"', msg_data.get("content", "")
                    )
                    for file_path in file_path_matches:
                        if should_exclude_by_string_pattern(file_path, config):
                            continue

                        # Apply semantic search to file paths
                        if search_term and not semantic_match(
                            file_path, search_term, semantic_variations
                        ):
                            continue

                        if not is_operation_seen("write", file_path):
                            operations.append(
                                {
                                    "timestamp": datetime.fromtimestamp(
                                        msg_data.get("time", {}).get("created", 0)
                                    ).isoformat()
                                    + "Z",
                                    "operation": "write",
                                    "file_path": redact_if_available(file_path, config),
                                    "session_id": session["id"],
                                    "search_match": bool(search_term),
                                }
                            )

                # Bash operations
                if '"bash"' in content and '"command"' in content:
                    command_matches = re.findall(
                        r'"command"\s*:\s*"([^"]+)"', msg_data.get("content", "")
                    )
                    for command in command_matches:
                        if should_exclude_bash_command(command, config):
                            continue

                        # Apply semantic search to commands
                        if search_term and not semantic_match(
                            command, search_term, semantic_variations
                        ):
                            continue

                        operations.append(
                            {
                                "timestamp": datetime.fromtimestamp(
                                    msg_data.get("time", {}).get("created", 0)
                                ).isoformat()
                                + "Z",
                                "operation": "bash",
                                "command": redact_if_available(command, config),
                                "session_id": session["id"],
                                "search_match": bool(search_term),
                            }
                        )

        except Exception:
            continue

    return operations


def capture_opencode_context():
    """Capture context from OpenCode sessions."""
    parser = argparse.ArgumentParser(
        description="Extract context from OpenCode sessions"
    )
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
        help="Include sessions from every registered project.",
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
        seen_operations.clear()

        # Get OpenCode storage path
        storage_path = get_opencode_storage_path()

        project_root = resolve_project_root(args.project_root)

        project_ids: list[tuple[str, Path]]
        if args.include_all_projects:
            project_ids = []
            project_dir = storage_path / "project"
            if project_dir.exists():
                for project_file in project_dir.glob("*.json"):
                    try:
                        with open(project_file) as pf:
                            data = json.load(pf)
                    except Exception:
                        continue
                    worktree = normalize_path(data.get("worktree"))
                    if not worktree:
                        continue
                    project_ids.append((data.get("id"), worktree))
        else:
            project_id = resolve_project_id(storage_path, project_root)
            if project_id is None:
                result = {
                    "sessions_found": 0,
                    "date_range": None,
                    "filter": "Project root not registered",
                    "search_term": args.search_term,
                    "operations": [],
                }
                print(json.dumps(result, indent=2))
                return
            project_ids = [(project_id, project_root)]

        sessions = []
        for pid, root_path in project_ids:
            if not pid:
                continue
            sessions.extend(
                find_recent_sessions(storage_path, pid, root_path, args.days)
            )

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

        # Build base payload
        result = build_result_payload(
            (session["id"] for session in sessions),
            all_operations,
            args.uuid,
            args.search_term,
        )

        # Enrich with per-session summaries (parity with Codex capture)
        try:
            from collections import Counter, defaultdict

            ops_by_sid: dict[str | None, list[dict]] = defaultdict(list)
            for op in all_operations:
                ops_by_sid[op.get("session_id")].append(op)

            sessions_out: list[dict] = []
            for s in sessions:
                sid = s.get("id")
                s_ops = ops_by_sid.get(sid, [])
                c = Counter(o.get("operation") for o in s_ops)
                ts_vals = [o.get("timestamp") for o in s_ops if o.get("timestamp")]
                date_range = {
                    "earliest": min(ts_vals) if ts_vals else None,
                    "latest": max(ts_vals) if ts_vals else None,
                }
                user_msgs = [
                    {"timestamp": o.get("timestamp"), "text": o.get("prompt")}
                    for o in s_ops
                    if o.get("operation") == "prompt" and o.get("prompt")
                ]
                sessions_out.append(
                    {
                        "id": sid,
                        "cwd": str(s.get("cwd")) if s.get("cwd") else None,
                        "date_range": date_range,
                        "counts": {
                            "user_messages": len(user_msgs),
                            "operations": len(s_ops),
                            **{k: v for k, v in c.items() if k},
                        },
                        "user_messages": user_msgs,
                    }
                )
            result["sessions"] = sessions_out
        except Exception:
            # If aggregation fails, continue with base payload
            pass

        emit_result(result, args.output_format)

    except Exception as e:
        print(f"Error extracting OpenCode context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    capture_opencode_context()
