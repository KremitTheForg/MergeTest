"""Dashboard and general overview pages."""

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app import models
from app.database import get_db

from .router import router, templates


@router.get("", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    """Render the administrator dashboard."""
    candidates_count = db.query(models.Candidate).count()
    users_count = db.query(models.User).count()
    training_count = 0

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "candidates_count": candidates_count,
            "users_count": users_count,
            "training_count": training_count,
        },
    )


@router.get("/candidates", response_class=HTMLResponse)
def list_candidates(request: Request, db: Session = Depends(get_db)):
    """List all candidate records."""
    candidates = db.query(models.Candidate).all()
    return templates.TemplateResponse(
        "candidates.html", {"request": request, "candidates": candidates}
    )


@router.get("/candidates-users", response_class=HTMLResponse)
def list_candidates_users(request: Request, db: Session = Depends(get_db)):
    """Render a combined view of candidates and users."""
    candidates = db.query(models.Candidate).all()
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        "candidates_users.html",
        {"request": request, "candidates": candidates, "users": users},
    )


@router.get("/training", response_class=HTMLResponse)
def list_training(request: Request):
    """Placeholder page for training content."""
    training = []
    return templates.TemplateResponse(
        "training_list.html", {"request": request, "training": training}
    )


@router.get("/candidate-assessment", response_class=HTMLResponse)
def candidate_assessment(request: Request):
    """Render the candidate assessment template."""
    return templates.TemplateResponse(
        "candidate_assessment.html", {"request": request}
    )
