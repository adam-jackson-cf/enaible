"""Minimal module used for prompt integration tests."""


def handler(event: dict[str, str]) -> str:
    """Return a formatted greeting."""
    name = event.get("name", "world")
    return f"Hello, {name}!"
