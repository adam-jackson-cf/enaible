#!/usr/bin/env python3
"""Context bundle capture for Codex sessions.

Parses Codex JSONL session logs under ~/.codex/sessions/YYYY/MM/DD/*.jsonl
to extract a concise list of operations (shell commands, file changes, etc.)
from the last N days. Supports filtering by session UUID and semantic search.
"""

import argparse
import json
import sys
from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

# Optional redaction
try:
    from sensitive_data_redactor import redact_sensitive_data

    REDACTION_AVAILABLE = True
except Exception:
    REDACTION_AVAILABLE = False


def load_config() -> dict[str, Any]:
    try:
        cfg_path = Path(__file__).parent / "context_capture_config.json"
        if cfg_path.exists():
            return json.loads(cfg_path.read_text())
    except Exception:
        pass
    return {
        "excluded_operations": ["session_meta", "turn_context", "token_count"],
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
        "redaction": {"enabled": True, "custom_patterns": []},
        "truncation_limits": {
            "prompt_max_length": 200,
            "edit_string_max_length": 2000,
        },
    }


def should_exclude_operation(op: str | None, config: dict[str, Any]) -> bool:
    return op in config.get("excluded_operations", [])


def should_exclude_bash_command(cmd: str | None, config: dict[str, Any]) -> bool:
    if not cmd:
        return False
    excluded = config.get("excluded_bash_commands", [])
    low = cmd.lower().strip()
    return any(low.startswith(e.lower()) for e in excluded)


def should_exclude_prompt(text: str | None, config: dict[str, Any]) -> bool:
    if not text:
        return False
    pats = config.get("excluded_prompt_patterns", [])
    t = text.strip().lower()
    return any(p.lower() in t for p in pats)


def redact_if_available(val: Any, config: dict[str, Any]) -> Any:
    if not isinstance(val, str):
        return val
    if not config.get("redaction", {}).get("enabled", True):
        return val
    if REDACTION_AVAILABLE:
        try:
            return redact_sensitive_data(val, config.get("redaction", {}))
        except Exception:
            return val
    return val


def semantic_match(
    text: str | None, term: str | None, variations: dict[str, list[str]] | None = None
) -> bool:
    if not term or not text:
        return False
    text_lower = text.lower()
    term_lower = term.lower()
    if term_lower in text_lower:
        return True
    words = term_lower.split()
    if all(w in text_lower for w in words):
        return True
    if variations:
        for w in words:
            for v in variations.get(w, []):
                if v in text_lower:
                    return True
    return False


def get_codex_sessions_root() -> Path:
    return Path.home() / ".codex" / "sessions"


def parse_date_from_path(p: Path) -> datetime:
    return datetime.fromtimestamp(p.stat().st_mtime)


def iter_recent_jsonl_files(root: Path, days: int) -> Iterable[Path]:
    if not root.exists():
        return []
    cutoff = datetime.now() - timedelta(days=days)
    for p in root.rglob("*.jsonl"):
        try:
            if parse_date_from_path(p) >= cutoff:
                yield p
        except Exception:
            continue


def build_operation(
    *,
    timestamp: str,
    operation: str,
    session_id: str | None,
    data: dict[str, Any],
    config: dict[str, Any],
    search_term: str | None,
    semantic_variations: dict[str, list[str]] | None,
) -> dict[str, Any] | None:
    if should_exclude_operation(operation, config):
        return None
    # Redact common string fields
    redact_fields = {"command", "file_path", "prompt", "output", "arguments", "text"}
    safe = {}
    for k, v in data.items():
        safe[k] = redact_if_available(v, config) if k in redact_fields else v
    if search_term and not semantic_match(
        json.dumps(safe, ensure_ascii=False), search_term, semantic_variations
    ):
        return None
    return {
        "timestamp": timestamp,
        "operation": operation,
        "session_id": session_id,
        **safe,
        "search_match": bool(search_term),
    }


def extract_jsonl_operations(
    jsonl_path: Path,
    *,
    config: dict[str, Any],
    search_term: str | None,
    semantic_variations: dict[str, list[str]] | None,
) -> tuple[str, list[dict[str, Any]]]:
    session_id: str | None = None
    ops: list[dict[str, Any]] = []
    try:
        with open(jsonl_path, encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    evt = json.loads(raw)
                except Exception:
                    continue
                ts = (
                    evt.get("timestamp")
                    or datetime.utcfromtimestamp(
                        parse_date_from_path(jsonl_path).timestamp()
                    ).isoformat()
                    + "Z"
                )
                etype = evt.get("type")
                payload = (
                    evt.get("payload") if isinstance(evt.get("payload"), dict) else {}
                )

                if etype == "session_meta":
                    session_id = (
                        payload.get("id") or payload.get("thread_id") or session_id
                    )
                    op = build_operation(
                        timestamp=ts,
                        operation="session_meta",
                        session_id=session_id,
                        data={
                            "cwd": payload.get("cwd"),
                            "cli_version": payload.get("cli_version"),
                            "originator": payload.get("originator"),
                        },
                        config=config,
                        search_term=search_term,
                        semantic_variations=semantic_variations,
                    )
                    if op:
                        ops.append(op)
                    continue

                # item.* events per docs
                if etype in {"item.started", "item.updated", "item.completed"}:
                    item = evt.get("item") or payload.get("item") or {}
                    itype = item.get("item_type") or item.get("type")
                    if itype == "file_change":
                        data = {
                            k: item.get(k)
                            for k in ("file_path", "diff", "change_type")
                            if k in item
                        }
                        op = build_operation(
                            timestamp=ts,
                            operation="file_change",
                            session_id=session_id,
                            data=data,
                            config=config,
                            search_term=search_term,
                            semantic_variations=semantic_variations,
                        )
                        if op:
                            ops.append(op)
                        continue
                    if itype == "assistant_message":
                        text = item.get("text") or item.get("content")
                        if text and not should_exclude_prompt(text, config):
                            short = text[:500] + ("..." if len(text) > 500 else "")
                            op = build_operation(
                                timestamp=ts,
                                operation="assistant_message",
                                session_id=session_id,
                                data={"text": short},
                                config=config,
                                search_term=search_term,
                                semantic_variations=semantic_variations,
                            )
                            if op:
                                ops.append(op)
                        continue

                # response_item events observed in local logs
                if etype == "response_item":
                    ptype = payload.get("type")
                    if ptype == "function_call":
                        name = payload.get("name")
                        args = payload.get("arguments")
                        cmd_str: str | None = None
                        try:
                            if isinstance(args, str):
                                args_json = json.loads(args)
                                cmd = args_json.get("command")
                                if isinstance(cmd, list):
                                    cmd_str = " ".join(str(x) for x in cmd)
                                elif isinstance(cmd, str):
                                    cmd_str = cmd
                        except Exception:
                            cmd_str = None

                        if (
                            name == "shell"
                            and cmd_str
                            and not should_exclude_bash_command(cmd_str, config)
                        ):
                            op = build_operation(
                                timestamp=ts,
                                operation="bash",
                                session_id=session_id,
                                data={"command": cmd_str},
                                config=config,
                                search_term=search_term,
                                semantic_variations=semantic_variations,
                            )
                            if op:
                                ops.append(op)
                        else:
                            op = build_operation(
                                timestamp=ts,
                                operation="tool_call",
                                session_id=session_id,
                                data={"tool": name, "arguments": args},
                                config=config,
                                search_term=search_term,
                                semantic_variations=semantic_variations,
                            )
                            if op:
                                ops.append(op)
                        continue
                    if ptype == "function_call_output":
                        out = payload.get("output")
                        if isinstance(out, str):
                            short = out[:2000] + ("..." if len(out) > 2000 else "")
                        else:
                            short = out
                        op = build_operation(
                            timestamp=ts,
                            operation="tool_output",
                            session_id=session_id,
                            data={"output": short},
                            config=config,
                            search_term=search_term,
                            semantic_variations=semantic_variations,
                        )
                        if op:
                            ops.append(op)
                        continue

                if etype in {"turn.started", "turn.completed", "turn.failed"}:
                    op = build_operation(
                        timestamp=ts,
                        operation=etype,
                        session_id=session_id,
                        data={},
                        config=config,
                        search_term=search_term,
                        semantic_variations=semantic_variations,
                    )
                    if op:
                        ops.append(op)
                    continue

    except Exception:
        # Skip unreadable files
        pass

    return (session_id or jsonl_path.stem, ops)


def capture_codex_context() -> None:
    parser = argparse.ArgumentParser(
        description="Extract context from Codex sessions (JSONL events)"
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
    args = parser.parse_args()

    # Parse semantic variations if provided
    semantic_variations: dict[str, list[str]] | None = None
    if args.semantic_variations:
        try:
            semantic_variations = json.loads(args.semantic_variations)
        except json.JSONDecodeError as e:
            print(f"Error parsing semantic variations JSON: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        config = load_config()
        root = get_codex_sessions_root()
        files = list(iter_recent_jsonl_files(root, args.days))

        if args.uuid:
            files = [p for p in files if args.uuid in p.name]

        all_ops: list[dict[str, Any]] = []
        session_ids: list[str] = []
        for fpath in sorted(files):
            sid, ops = extract_jsonl_operations(
                fpath,
                config=config,
                search_term=args.search_term,
                semantic_variations=semantic_variations,
            )
            if args.uuid and args.uuid not in (sid or ""):
                continue
            session_ids.append(sid)
            all_ops.extend(ops)

        timestamps = [op.get("timestamp") for op in all_ops if op.get("timestamp")]
        date_range = {
            "earliest": min(timestamps) if timestamps else None,
            "latest": max(timestamps) if timestamps else None,
        }

        result = {
            "sessions_found": len(set(session_ids)),
            "date_range": date_range,
            "filter": f"UUID: {args.uuid}" if args.uuid else "All recent sessions",
            "search_term": args.search_term,
            "operations": all_ops,
        }

        if args.output_format == "json":
            print(json.dumps(result, indent=2))
        else:
            print(f"Sessions Found: {result['sessions_found']}")
            if date_range["earliest"]:
                print(f"Date Range: {date_range['earliest']} to {date_range['latest']}")
            print(f"Filter: {result['filter']}")
            if args.search_term:
                print(f"Search Term: {args.search_term}")
            print(f"Operations: {len(all_ops)}")

    except Exception as e:
        print(f"Error extracting Codex context: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    capture_codex_context()
