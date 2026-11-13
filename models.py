from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    education = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    jd_id = Column(Integer, ForeignKey("job_descriptions.id"))
    score = Column(Integer, nullable=False)
    matched_skills = Column(Text, nullable=True)
    missing_skills = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)