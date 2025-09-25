# app/routers/candidates.py

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional
from datetime import date, datetime, timezone
from datetime import date, datetime
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.datastructures import UploadFile

from app.database import get_db
from app import models

router = APIRouter()

# --- payload model the frontend sends ---
class CandidateCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    address: Optional[str] = None
    applied_on: Optional[date] = None  # optional; DB default handles if omitted


# --- JSON API used by the intake form ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/api/v1/hr/recruitment/candidates/", response_class=JSONResponse)
async def api_create_candidate(
    request: Request,
    db: Session = Depends(get_db),
):
    # must be logged in to attach user_id
    session_user = request.session.get("user")
    if not session_user:
        return JSONResponse({"detail": "Not authenticated"}, status_code=401)

    content_type = request.headers.get("content-type", "")
    resume_file: UploadFile | None = None

    if "application/json" in content_type:
        payload_data = await request.json()
    else:
        form = await request.form()
        payload_data = {}
        for field in (
            "first_name",
            "last_name",
            "email",
            "mobile",
            "job_title",
            "address",
            "applied_on",
        ):
            value = form.get(field)
            if isinstance(value, UploadFile):
                continue
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    value = None
            payload_data[field] = value
        maybe_resume = form.get("resume")
        if isinstance(maybe_resume, UploadFile) and (maybe_resume.filename or "").strip():
            resume_file = maybe_resume

    if isinstance(payload_data, dict):
        for optional_field in ("mobile", "job_title", "address", "applied_on"):
            if payload_data.get(optional_field) == "":
                payload_data[optional_field] = None

    try:
        payload = CandidateCreate(**payload_data)
    except ValidationError as exc:
        return JSONResponse({"detail": exc.errors()}, status_code=422)

    candidate_data = dict(
        first_name=payload.first_name.strip(),
        last_name=payload.last_name.strip(),
        email=str(payload.email),
        mobile=payload.mobile or "",
        job_title=payload.job_title or "",
        address=payload.address or "",
        status="Applied",
    )

    # Only auto-link the new candidate to the logged-in user when they are
    # submitting their own information. Admins adding applicants should not
    # overwrite the candidate->user linkage with their own account.
    session_email = (session_user.get("email") or "").strip().lower()
    if session_email and session_email == str(payload.email).lower():
        candidate_data["user_id"] = session_user["id"]
    if payload.applied_on:
        candidate_data["applied_on"] = datetime.combine(
            payload.applied_on,
            datetime.min.time(),
            tzinfo=timezone.utc,
        user_id=session_user["id"],
    )
    if payload.applied_on:
        candidate_data["applied_on"] = datetime.combine(
            payload.applied_on, datetime.min.time()

        )

    cand = models.Candidate(**candidate_data)

    try:
        db.add(cand)
        db.flush()
    except IntegrityError:
        db.rollback()
        return JSONResponse(
            {"detail": "Email already exists for a candidate."}, status_code=409
        )

    saved_file_path: Path | None = None
    resume_uploaded = False
    try:
        if resume_file and resume_file.filename:
            ext = Path(resume_file.filename).suffix or ".pdf"
            folder = UPLOAD_DIR / str(cand.id)
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / f"resume{ext}"
            saved_file_path = dest
            contents = await resume_file.read()
            with open(dest, "wb") as f:
                f.write(contents)

            relative_path = str(dest.relative_to(BASE_DIR))
            profile = (
                db.query(models.CandidateProfile)
                .filter(models.CandidateProfile.candidate_id == cand.id)
                .first()
            )
            if not profile:
                profile = models.CandidateProfile(candidate_id=cand.id)
            profile.resume_path = relative_path
            db.add(profile)
            resume_uploaded = True

        db.commit()
        db.refresh(cand)
    except Exception:
        db.rollback()
        if saved_file_path and saved_file_path.exists():
            saved_file_path.unlink(missing_ok=True)
        raise
    finally:
        if resume_file:
            try:
                await resume_file.close()
            except Exception:
                pass

    return JSONResponse(
        {"id": cand.id, "detail": "created", "resume_uploaded": resume_uploaded},
        status_code=201,
    )
