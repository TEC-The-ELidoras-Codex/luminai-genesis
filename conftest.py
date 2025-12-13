"""
Top-level pytest conftest to ensure our repo root is on sys.path during tests.

Reason: some CI environments or local runner configurations can run pytest from a
tests subdirectory or with different working dir behavior. Adding the repo root
to sys.path at test collection time ensures absolute imports like
`import backend` or `import src.persona_blending` succeed reliably.

This is intentionally minimal and only affects test runs (pytest discovery).
"""

from __future__ import annotations

import sys
from pathlib import Path


def pytest_configure(config):
    # Repo root is directory containing this file
    repo_root = Path(__file__).resolve().parent
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
