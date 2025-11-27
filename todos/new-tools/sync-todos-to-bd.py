#!/usr/bin/env python3
"""
Sync completed TodoWrite items to Beads (bd).

Extract bd IDs from completed todos and close them.

Usage: sync-todos-to-bd.py <TOOL_USE_PAYLOAD>
"""
import json
import re
import subprocess
import sys


def extract_bd_id(todo_content: str) -> str | None:
    """
    Extract a bd ID from todo content like "[bd-123] Task description".

    Args:
        todo_content: The todo item content string

    Returns
    -------
        bd ID string (e.g., 'bd-123') or None if not found
    """
    match = re.search(r"\[bd-(\d+)\]", todo_content)
    return f"bd-{match.group(1)}" if match else None


def close_bd_issue(bd_id: str) -> bool:
    """
    Close a bd issue and return success status.

    Args:
        bd_id: The bd issue ID (e.g., 'bd-123')

    Returns
    -------
        True if closed successfully, False otherwise
    """
    try:
        result = subprocess.run(
            ["bd", "close", bd_id, "--reason", "Completed via TodoWrite"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error closing {bd_id}: {e}", file=sys.stderr)
        return False


def main():
    """Run the TodoWrite → Beads sync hook."""
    if len(sys.argv) < 2:
        # No payload provided, exit silently
        sys.exit(0)

    try:
        # Parse the TodoWrite payload
        payload = json.loads(sys.argv[1])
        todos = payload.get("parameters", {}).get("todos", [])

        closed_count = 0
        for todo in todos:
            # Only process completed todos
            if todo.get("status") == "completed":
                bd_id = extract_bd_id(todo.get("content", ""))
                if bd_id and close_bd_issue(bd_id):
                    print(f"✓ Closed {bd_id}")
                    closed_count += 1

        if closed_count > 0:
            print(f"\n📝 Synced {closed_count} completed todo(s) to Beads")

    except json.JSONDecodeError as e:
        print(f"Error parsing payload JSON: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block TodoWrite on errors
    except Exception as e:
        print(f"Error syncing todos: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block TodoWrite on errors


if __name__ == "__main__":
    main()
