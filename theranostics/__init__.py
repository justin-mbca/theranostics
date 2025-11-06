"""Theranostics prototype package."""
# Apply local runtime compatibility shims early on import.
from . import _compat  # noqa: F401

__all__ = ["simulate", "models", "flow"]
