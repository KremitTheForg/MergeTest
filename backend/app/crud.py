from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

def create_candidate(db: Session, candidate: schemas.CandidateCreate, user_id: int | None = None):
    db_candidate = models.Candidate(
        first_name=candidate.first_name,
        last_name=candidate.last_name,
        email=candidate.email,
        mobile=candidate.mobile,
        job_title=candidate.job_title,
        address=candidate.address,
        status="Applied",
        user_id=user_id
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def get_candidates(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Candidate).offset(skip).limit(limit).all()

##

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


## Candidate Profile CRUD
def get_candidate_by_user(db: Session, user_id: int):
    return db.query(models.Candidate).filter(models.Candidate.user_id == user_id).first()

def get_profile(db: Session, candidate_id: int):
    return db.query(models.CandidateProfile).filter(models.CandidateProfile.candidate_id == candidate_id).first()

def get_or_create_profile(db: Session, candidate_id: int):
    prof = get_profile(db, candidate_id)
    if prof:
        return prof
    prof = models.CandidateProfile(candidate_id=candidate_id)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof

def update_profile(db: Session, candidate_id: int, data: "schemas.CandidateProfileUpdate"):
    prof = get_or_create_profile(db, candidate_id)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(prof, field, value)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof

def set_profile_file(db: Session, candidate_id: int, kind: str, path: str):
    prof = get_or_create_profile(db, candidate_id)
    if kind == "resume":
        prof.resume_path = path
    elif kind == "photo":
        prof.photo_path = path
    else:
        raise ValueError("kind must be 'resume' or 'photo'")
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof
