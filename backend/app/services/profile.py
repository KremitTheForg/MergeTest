"""Profile related helpers shared between the HTML and JSON routes."""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import HTTPException
from starlette.datastructures import UploadFile
from sqlalchemy.orm import Session

from app import crud, models

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_profile_upload(
    *,
    candidate: models.Candidate,
    kind: str,
    file: UploadFile,
    db: Session,
) -> str:
    """Persist an uploaded resume/photo and update the candidate profile."""

    normalized_kind = "photo" if kind == "picture" else kind
    if normalized_kind not in {"resume", "photo"}:
        raise HTTPException(status_code=400, detail="kind must be 'resume' or 'photo'")

    filename = file.filename or ""
    default_ext = ".png" if normalized_kind == "photo" else ".pdf"
    ext = os.path.splitext(filename)[1] or default_ext

    folder = UPLOAD_DIR / str(candidate.id)
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / f"{normalized_kind}{ext}"

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Uploaded file was empty")

    with open(dest, "wb") as buffer:
        buffer.write(contents)

    relative_path = str(dest.relative_to(BASE_DIR))
    crud.set_profile_file(db, candidate.id, normalized_kind, relative_path)
    return relative_path
