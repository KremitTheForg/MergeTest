"""Routes for managing applicant-to-worker workflows."""

import hashlib
import secrets

from fastapi import Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

from .router import APPLICANT_STATUSES_EXCLUDE, router, templates


def _existing_user_for_candidate(candidate: models.Candidate, db: Session):
    if candidate.user_id:
        user = db.query(models.User).filter(models.User.id == candidate.user_id).first()
        if user:
            return user
    if candidate.email:
        return db.query(models.User).filter(models.User.email == candidate.email).first()
    return None


def _generate_candidate_username(candidate: models.Candidate, db: Session) -> str:
    if candidate.email and "@" in candidate.email:
        base_username = candidate.email.split("@")[0]
    else:
        base_username = (
            f"{(candidate.first_name or '').lower()}.{(candidate.last_name or '').lower()}".strip(".")
        )
    base_username = base_username or f"user{candidate.id}"

    username = base_username
    suffix = 1
    while db.query(models.User).filter(models.User.username == username).first():
        suffix += 1
        username = f"{base_username}{suffix}"
    return username


def _create_user_for_candidate(candidate: models.Candidate, db: Session):
    username = _generate_candidate_username(candidate, db)
    temp_password = secrets.token_urlsafe(8)
    hashed = hashlib.sha256(temp_password.encode()).hexdigest()

    user = models.User(
        username=username,
        email=candidate.email or f"{username}@example.com",
        hashed_password=hashed,
    )
    db.add(user)
    db.flush()

    candidate.user_id = user.id
    db.add(candidate)
    return user, temp_password


def _ensure_candidate_user(candidate: models.Candidate, db: Session):
    user = _existing_user_for_candidate(candidate, db)
    if user:
        return user, None
    return _create_user_for_candidate(candidate, db)


@router.get("/applicants", response_class=HTMLResponse)
def list_applicants(request: Request, db: Session = Depends(get_db)):
    """List applicants who have not yet been converted to workers."""
    applicants = (
        db.query(models.Candidate)
        .filter(~models.Candidate.status.in_(APPLICANT_STATUSES_EXCLUDE))
        .all()
    )
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(
        "applicants.html",
        {"request": request, "applicants": applicants, "flash": flash},
    )


@router.get("/applicants/{candidate_id}/profile")
def ensure_profile_and_open(
    candidate_id: int, request: Request, db: Session = Depends(get_db)
):
    """Ensure a candidate has a linked user before opening the profile view."""
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")

    user, temp_password = _ensure_candidate_user(cand, db)
    if temp_password:
        request.session["flash"] = (
            f"Created user '{user.username}'. Temporary password: {temp_password}"
        )
        db.commit()

    return RedirectResponse(url=f"/portal/profile/admin/{user.id}", status_code=303)


@router.post("/applicants/{candidate_id}/convert", response_class=HTMLResponse)
def convert_applicant_to_worker(
    candidate_id: int, request: Request, db: Session = Depends(get_db)
):
    """Convert an applicant into a worker, ensuring a user exists."""
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        request.session["flash"] = "Candidate not found."
        return RedirectResponse(url="/admin/applicants", status_code=303)

    user, temp_password = _ensure_candidate_user(cand, db)
    if temp_password:
        request.session["flash"] = (
            f"Created user '{user.username}'. Temporary password: {temp_password}"
        )

    cand.status = "Hired"
    if user:
        cand.user_id = user.id
    db.add(cand)
    db.commit()

    if "flash" not in request.session:
        full_name = f"{cand.first_name or ''} {cand.last_name or ''}".strip() or "Candidate"
        request.session["flash"] = f"{full_name} moved to Workers."

    return RedirectResponse(url="/admin/users", status_code=303)
