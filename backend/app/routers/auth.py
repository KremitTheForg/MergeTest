from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from .. import schemas, crud, database, models
from ..core.templates import get_templates
from jinja2 import TemplateNotFound

router = APIRouter(prefix="/auth", tags=["auth"])
templates = get_templates()


# GET: show login form
@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    try:
        return templates.TemplateResponse("login.html", {"request": request})
    except TemplateNotFound:
        fallback_html = """
        <!DOCTYPE html>
        <html lang=\"en\">
        <head>
            <meta charset=\"utf-8\">
            <title>Login</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem auto; max-width: 32rem; }
                form { display: flex; flex-direction: column; gap: 1rem; }
                label { font-weight: 600; }
                input { padding: 0.5rem; font-size: 1rem; }
                button { padding: 0.75rem; font-size: 1rem; cursor: pointer; }
                .hint { margin-top: 1rem; font-size: 0.9rem; }
                .hint code { font-family: monospace; }
            </style>
        </head>
        <body>
            <h2>Login</h2>
            <p>The expected template <code>backend/templates/login.html</code> could not be located. This
            inline fallback is rendered so local development can continue, but you should restore the
            missing template file for the full experience.</p>
            <form action=\"/auth/login\" method=\"post\">
                <label for=\"email\">Email</label>
                <input id=\"email\" type=\"email\" name=\"email\" required>

                <label for=\"password\">Password</label>
                <input id=\"password\" type=\"password\" name=\"password\" required>

                <button type=\"submit\">Login</button>
            </form>
            <p class=\"hint\">Don’t have an account? <a href=\"/auth/register\">Register here</a>.</p>
        </body>
        </html>
        """
        return HTMLResponse(content=fallback_html, status_code=200)


# POST: handle login
@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user or not crud.verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Save session
    request.session["user"] = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }

    candidate = db.query(models.Candidate).filter(models.Candidate.user_id == db_user.id).first()
    if not candidate:
        candidate = db.query(models.Candidate).filter(models.Candidate.email == db_user.email).first()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": db_user, "candidate": candidate}
    )


# GET: show register form
@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# POST: handle registration
@router.post("/register", response_class=HTMLResponse)
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(database.get_db)
):
    # 1) Uniqueness check
    existing_user = crud.get_user_by_email(db, email=email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2) Create user (crud.create_user should hash the password)
    user_data = schemas.UserCreate(username=username, email=email, password=password)
    db_user = crud.create_user(db, user_data)

    # 3) Ensure a Candidate exists & is linked to this user (status 'Applied')
    cand = db.query(models.Candidate).filter(models.Candidate.email == email).first()
    if not cand:
        cand = models.Candidate(
            first_name="",
            last_name="",
            email=email,
            job_title="",
            mobile="",
            status="Applied",          # => shows up under All Applicants
            user_id=db_user.id,
        )
        db.add(cand)
        db.commit()
    else:
        # Link any pre-existing candidate row to this new user
        updated = False
        if not cand.user_id:
            cand.user_id = db_user.id
            updated = True
        if not cand.status:
            cand.status = "Applied"
            updated = True
        if updated:
            db.add(cand)
            db.commit()

    # 4) Auto-login after register
    request.session["user"] = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
    }

    # You can keep dashboard or redirect to applicants; dashboard kept to preserve your flow
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": db_user, "candidate": cand}
    )


# GET or POST: logout
@router.get("/logout")
@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
