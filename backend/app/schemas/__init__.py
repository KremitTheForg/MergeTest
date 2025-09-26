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


class CandidateWithProfile(BaseModel):
    candidate: CandidateOut
    profile: Optional["CandidateProfileOut"] = None

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


class AdminMetrics(BaseModel):
    candidates: int
    users: int
    training: int


class WorkerQueryFilters(BaseModel):
    role: Optional[str] = None
    status: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    q: Optional[str] = None


class WorkerUserOut(BaseModel):
    user: UserOut
    candidate: CandidateOut


class WorkerListResponse(BaseModel):
    results: list[WorkerUserOut]
    filters: WorkerQueryFilters
    roles: list[str]
    status_options: list[str]


class CandidateListResponse(BaseModel):
    results: list[CandidateWithProfile]


class ApplicantListResponse(BaseModel):
    results: list[CandidateOut]


class ApplicantConvertResponse(BaseModel):
    detail: str


class MeResponse(BaseModel):
    user: UserOut
    candidate: Optional[CandidateOut] = None
    profile: Optional[CandidateProfileOut] = None


class ProfileUpdatePayload(CandidateProfileUpdate):
    job_title: Optional[str] = None


class ProfileResponse(BaseModel):
    candidate: CandidateOut
    profile: CandidateProfileOut


class ProfileUploadResponse(BaseModel):
    candidate_id: int
    kind: str
    path: str
