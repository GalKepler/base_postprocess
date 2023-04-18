# type: ignore[attr-defined]
"""Tractography pipeline(s) for TheBase scanning protocol"""

import sys  # noqa: F401
from importlib import metadata as importlib_metadata  # noqa: F401


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()
