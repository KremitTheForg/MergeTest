"""Helpers for ensuring the React frontend build is available."""
from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
FRONTEND_DIST_DIR = BASE_DIR / "static" / "forms"
FRONTEND_INDEX_FILE = FRONTEND_DIST_DIR / "index.html"


def ensure_frontend_build(*, force: bool = False) -> bool:
    """Ensure the React frontend has been built.

    Returns ``True`` when the ``index.html`` file is present. If it is missing,
    the function will attempt to run ``npm run build`` in the frontend directory
    (if npm is available). The helper is intentionally best-effort – failures
    simply result in returning ``False`` so the caller can fall back to the
    legacy server rendered template.
    """

    if FRONTEND_INDEX_FILE.exists() and not force:
        return True

    if not FRONTEND_DIR.exists():
        return False

    npm_executable = _find_npm()
    if not npm_executable:
        return False

    try:
        completed = subprocess.run(
            [npm_executable, "run", "build"],
            cwd=FRONTEND_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logging.getLogger(__name__).info(
            "Built frontend assets via npm. output=%s", completed.stdout.strip()
        )
        if completed.stderr:
            logging.getLogger(__name__).debug(
                "npm build stderr: %s", completed.stderr.strip()
            )
    except subprocess.CalledProcessError as exc:
        logging.getLogger(__name__).warning(
            "Failed to build frontend assets: %s", exc
        )
        return False

    return FRONTEND_INDEX_FILE.exists()


def _find_npm() -> Optional[str]:
    """Return the npm executable if it can be located on PATH."""

    for candidate in ("npm", "npm.cmd", "npm.exe"):
        if shutil.which(candidate):
            return candidate
    return None
