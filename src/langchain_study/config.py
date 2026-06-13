"""Small configuration helpers used by later examples."""

from __future__ import annotations

import os


def get_env(name: str, default: str | None = None) -> str | None:
    """Read an environment variable without hiding where configuration comes from."""
    return os.getenv(name, default)
