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
FRONTEND_NODE_MODULES = FRONTEND_DIR / "node_modules"
FRONTEND_PACKAGE_JSON = FRONTEND_DIR / "package.json"
FRONTEND_PACKAGE_LOCK = FRONTEND_DIR / "package-lock.json"



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

    if _dependencies_need_install():
        if not _run_npm_command(npm_executable, ["install"], "install dependencies"):
            return False

    if not _run_npm_command(npm_executable, ["run", "build"], "build frontend"):
        return False

    return FRONTEND_INDEX_FILE.exists()


def _find_npm() -> Optional[str]:
    """Return the npm executable if it can be located on PATH."""

    for candidate in ("npm", "npm.cmd", "npm.exe"):
        if shutil.which(candidate):
            return candidate
    return None


def _dependencies_need_install() -> bool:
    """Return ``True`` when ``npm install`` should be executed."""

    if not FRONTEND_NODE_MODULES.exists():
        return True

    lock_mtime = _safe_mtime(FRONTEND_PACKAGE_LOCK)
    package_mtime = _safe_mtime(FRONTEND_PACKAGE_JSON)
    node_modules_mtime = _safe_mtime(FRONTEND_NODE_MODULES)

    newest_manifest = max(lock_mtime, package_mtime)
    if newest_manifest is None:
        return False

    if node_modules_mtime is None:
        return True

    return newest_manifest > node_modules_mtime


def _safe_mtime(path: Path) -> Optional[float]:
    try:
        return path.stat().st_mtime
    except OSError:
        return None


def _run_npm_command(npm_executable: str, args: list[str], description: str) -> bool:
    """Execute an npm command within the frontend directory."""

    try:
        completed = subprocess.run(
            [npm_executable, *args],

    try:
        completed = subprocess.run(
            [npm_executable, "run", "build"],

            cwd=FRONTEND_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    except subprocess.CalledProcessError as exc:
        logging.getLogger(__name__).warning(
            "Failed to %s: %s", description, exc
        )
        return False

    logger = logging.getLogger(__name__)
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    if stdout:
        logger.info("npm %s output: %s", description, stdout)
    if stderr:
        logger.debug("npm %s stderr: %s", description, stderr)

    return True

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

