from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Resume, JobDescription, MatchResult
from schemas import ResumeOut, JobDescriptionCreate, JobDescriptionOut, MatchOut
from services.parser import extract_text_from_pdf, extract_text_from_docx, parse_resume, calculate_match

router = APIRouter()

@router.post("/upload", response_model=ResumeOut)
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(content)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX allowed")

    parsed = parse_resume(text)

    new_resume = Resume(
        filename=file.filename,
        name=parsed["name"],
        email=parsed["email"],
        phone=parsed["phone"],
        skills=parsed["skills"],
        experience=parsed["experience"],
        education=parsed["education"],
        raw_text=parsed["raw_text"]
    )
    db.add(new_resume)
    await db.commit()
    await db.refresh(new_resume)
    return new_resume

@router.get("/", response_model=list[ResumeOut])
async def list_resumes(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resume))
    return result.scalars().all()

@router.get("/{resume_id}", response_model=ResumeOut)
async def get_resume(resume_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.post("/jd", response_model=JobDescriptionOut)
async def create_jd(jd: JobDescriptionCreate, db: AsyncSession = Depends(get_db)):
    new_jd = JobDescription(title=jd.title, description=jd.description)
    db.add(new_jd)
    await db.commit()
    await db.refresh(new_jd)
    return new_jd

@router.post("/match/{resume_id}/{jd_id}", response_model=MatchOut)
async def match_resume(resume_id: int, jd_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    result = await db.execute(select(JobDescription).where(JobDescription.id == jd_id))
    jd = result.scalar_one_or_none()
    if not jd:
        raise HTTPException(status_code=404, detail="JD not found")

    score, matched, missing = calculate_match(resume.skills or "", jd.description)

    match = MatchResult(
        resume_id=resume_id,
        jd_id=jd_id,
        score=score,
        matched_skills=matched,
        missing_skills=missing
    )
    db.add(match)
    await db.commit()
    await db.refresh(match)
    return match