from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    mobile: Optional[str] = None
    job_title: Optional[str] = None
    address: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateOut(CandidateBase):
    id: int
    status: str
    applied_on: datetime

    class Config:
        from_attributes = True

###

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str



### Candidate Profile Schemas
class CandidateProfileBase(BaseModel):
    summary: Optional[str] = None
    skills: Optional[str] = None
    linkedin: Optional[str] = None
    address: Optional[str] = None

class CandidateProfileUpdate(CandidateProfileBase):
    pass

class CandidateProfileOut(CandidateProfileBase):
    id: int
    resume_path: Optional[str] = None
    photo_path: Optional[str] = None
    # When returned as JSON
    class Config:
        from_attributes = True
