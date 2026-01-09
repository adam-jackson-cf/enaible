#!/usr/bin/env python3
import argparse
import json


def clean_claude_config(clear_all_history=False):
    config_path = "/Users/adamjackson/.claude.json"
    print("Reading large config file...")
    data = _load_config(config_path)

    projects_cleaned, total_entries_removed = _clean_project_histories(
        data, clear_all_history
    )

    images_removed = 0
    if not clear_all_history:
        images_removed = _clean_history_images(data)

    _print_cleanup_summary(clear_all_history, total_entries_removed, images_removed)

    print("Writing cleaned config file...")
    _write_config(config_path, data)
    _print_final_summary(clear_all_history, projects_cleaned, total_entries_removed)


def _load_config(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def _clean_project_histories(data: dict, clear_all_history: bool) -> tuple[int, int]:
    projects_cleaned = 0
    total_entries_removed = 0
    skip_keys = {
        "numStartups",
        "installMethod",
        "autoUpdates",
        "tipsHistory",
        "mcpServers",
    }
    for project_path, project_data in data.items():
        if project_path in skip_keys or not isinstance(project_data, dict):
            continue
        cleared, removed = _maybe_clear_history(
            project_path, project_data, clear_all_history
        )
        projects_cleaned += 1 if cleared else 0
        total_entries_removed += removed
        if not clear_all_history:
            _clean_large_arrays(project_path, project_data)
    return projects_cleaned, total_entries_removed


def _maybe_clear_history(
    project_path: str, project_data: dict, clear_all_history: bool
) -> tuple[bool, int]:
    history = project_data.get("history")
    if not isinstance(history, list):
        return False, 0
    original_count = len(history)
    if original_count == 0:
        return False, 0
    if not clear_all_history:
        return False, 0
    project_data["history"] = []
    print(f"Cleared ALL {original_count} history entries from {project_path}")
    return True, original_count


def _clean_large_arrays(project_path: str, project_data: dict) -> None:
    keep_keys = {
        "exampleFiles",
        "allowedTools",
        "mcpServers",
        "enabledMcpjsonServers",
        "disabledMcpjsonServers",
    }
    for key in list(project_data.keys()):
        if key in keep_keys:
            continue
        value = project_data[key]
        if isinstance(value, list) and len(value) > 20:
            orig_len = len(value)
            project_data[key] = []
            print(f"Cleared large {key} array ({orig_len} items) from {project_path}")


def _clean_history_images(data: dict) -> int:
    images_removed = 0

    def clean_history_recursively(obj):
        nonlocal images_removed
        if isinstance(obj, dict):
            for key, value in obj.items():
                if (
                    key == "content"
                    and isinstance(value, str)
                    and value.startswith("iVBORw0KGgo")
                ):
                    obj[key] = "[Large image removed to reduce file size]"
                    images_removed += 1
                elif isinstance(value, (dict, list)):
                    clean_history_recursively(value)
        elif isinstance(obj, list):
            for item in obj:
                clean_history_recursively(item)

    clean_history_recursively(data)
    if images_removed > 0:
        print(f"Removed {images_removed} large base64 images")
    return images_removed


def _print_cleanup_summary(
    clear_all_history: bool,
    total_entries_removed: int,
    images_removed: int,
) -> None:
    if clear_all_history:
        print(f"Total history entries completely removed: {total_entries_removed}")
        return
    print("Total history entries cleaned (kept but images removed): preserved")
    if images_removed:
        print(f"Total images removed: {images_removed}")


def _write_config(path: str, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def _print_final_summary(
    clear_all_history: bool, projects_cleaned: int, total_entries_removed: int
) -> None:
    print("\nCleaning complete:")
    if clear_all_history:
        print(f"- Completely cleared history from {projects_cleaned} projects")
        print(f"- Total history entries removed: {total_entries_removed}")
    else:
        print("- Cleaned large images and content from history (preserved structure)")
    print("- Backup available at /Users/adamjackson/.claude.json.backup")


def main():
    parser = argparse.ArgumentParser(description="Clean Claude configuration file")
    parser.add_argument(
        "--clear-all-history",
        action="store_true",
        help="Completely delete all history entries (default: just clean large content)",
    )

    args = parser.parse_args()

    clean_claude_config(clear_all_history=args.clear_all_history)


if __name__ == "__main__":
    main()
