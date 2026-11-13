from pydantic import BaseModel
from typing import Optional

class ResumeOut(BaseModel):
    id: int
    filename: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None

    class Config:
        from_attributes = True

class JobDescriptionCreate(BaseModel):
    title: str
    description: str

class JobDescriptionOut(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True

class MatchOut(BaseModel):
    resume_id: int
    jd_id: int
    score: int
    matched_skills: Optional[str] = None
    missing_skills: Optional[str] = None

    class Config:
        from_attributes = True