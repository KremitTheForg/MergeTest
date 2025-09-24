"""Shared admin router configuration and resources."""

from pathlib import Path

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/admin", tags=["admin"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

WORKER_STATUSES = {"Hired", "Employee", "Active"}
APPLICANT_STATUSES_EXCLUDE = WORKER_STATUSES
