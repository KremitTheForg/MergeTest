"""Routes for managing employees and worker records."""

import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import EmailStr
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

from .router import WORKER_STATUSES, router, templates


@router.get("/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    """List workers with optional filtering."""
    role = (request.query_params.get("role") or "").strip()
    status = (request.query_params.get("status") or "").strip()
    date_from = (request.query_params.get("date_from") or "").strip()
    date_to = (request.query_params.get("date_to") or "").strip()
    q = (request.query_params.get("q") or "").strip()

    cand_filters = [models.Candidate.status.in_(WORKER_STATUSES)]
    if status:
        cand_filters = [models.Candidate.status == status]
    if role:
        cand_filters.append(models.Candidate.job_title == role)

    def _parse_iso(value: str):
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None

    start_dt = _parse_iso(date_from)
    end_dt = _parse_iso(date_to)
    if start_dt:
        cand_filters.append(models.Candidate.applied_on >= start_dt)
    if end_dt:
        cand_filters.append(models.Candidate.applied_on < (end_dt + timedelta(days=1)))

    if q:
        like = f"%{q}%"
        cand_filters.append(
            or_(
                models.Candidate.first_name.ilike(like),
                models.Candidate.last_name.ilike(like),
                models.Candidate.email.ilike(like),
                models.Candidate.mobile.ilike(like),
                models.User.username.ilike(like),
                models.User.email.ilike(like),
            )
        )

    rows = (
        db.query(models.User, models.Candidate)
        .join(models.Candidate, models.Candidate.user_id == models.User.id)
        .filter(*cand_filters)
        .order_by(func.lower(models.User.username))
        .all()
    )

    users = [user for (user, _cand) in rows]
    user_candidates = {user.id: cand for (user, cand) in rows}

    roles = [
        r
        for (r,) in (
            db.query(models.Candidate.job_title)
            .filter(models.Candidate.status.in_(WORKER_STATUSES))
            .filter(models.Candidate.job_title.isnot(None))
            .distinct()
            .all()
        )
        if r
    ]
    roles.sort(key=lambda value: value.lower())

    status_options = sorted(WORKER_STATUSES)

    flash = request.session.pop("flash", None)
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "user_candidates": user_candidates,
            "flash": flash,
            "roles": roles,
            "status_options": status_options,
            "role": role,
            "status": status,
            "date_from": date_from,
            "date_to": date_to,
            "q": q,
        },
    )


@router.get("/staffs")
def list_staffs_redirect():
    """Retain backwards compatibility for the previous /admin/staffs route."""
    return RedirectResponse(url="/admin/users", status_code=307)


@router.get("/users/new", response_class=HTMLResponse)
def new_user_form(request: Request):
    """Render the form to create a new employee."""
    return templates.TemplateResponse("user_new.html", {"request": request})


@router.post("/users/new", response_class=HTMLResponse)
def create_user_and_candidate(
    request: Request,
    username: str = Form(...),
    email: EmailStr = Form(...),
    first_name: str = Form(""),
    last_name: str = Form(""),
    job_title: str = Form(""),
    mobile: str = Form(""),
    status: str = Form("Applied"),
    db: Session = Depends(get_db),
):
    """Create a User and matching Candidate record."""
    existing = (
        db.query(models.User)
        .filter((models.User.username == username) | (models.User.email == email))
        .first()
    )
    if existing:
        return templates.TemplateResponse(
            "user_new.html",
            {"request": request, "error": "Username or email already exists."},
            status_code=400,
        )

    temp_password = secrets.token_urlsafe(8)
    hashed = hashlib.sha256(temp_password.encode()).hexdigest()

    user = models.User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    candidate = models.Candidate(
        first_name=first_name or "",
        last_name=last_name or "",
        email=email,
        mobile=mobile or "",
        job_title=job_title or "",
        status=status or "Applied",
        user_id=user.id,
    )
    db.add(candidate)
    db.commit()

    request.session["flash"] = f"User created. Temporary password: {temp_password}"
    return RedirectResponse(url="/admin/users", status_code=303)
