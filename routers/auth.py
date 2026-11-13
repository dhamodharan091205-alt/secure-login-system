from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from passlib.context import CryptContext
from jose import jwt
import random, datetime

SECRET_KEY = "my-super-secret-key-123"
ALGORITHM = "HS256"

router = APIRouter(prefix="/api/auth", tags=["Auth - 2FA"])
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def create_token(email: str):
    return jwt.encode({"sub": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)}, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup")
async def signup(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    if result.scalars().first():
        raise HTTPException(400, "User already exists")
    user = User(email=email, hashed_password=pwd_context.hash(password))
    db.add(user)
    await db.commit()
    return {"message": "Signup success, now login to get OTP"}

@router.post("/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(401, "Wrong email or password")
    # Generate 6-digit OTP - for demo we return it in response
    otp = str(random.randint(100000, 999999))
    user.otp_code = otp
    await db.commit()
    # In real project, send this OTP via Email. For demo, we show it.
    return {"message": "OTP sent to email", "DEMO_OTP": otp, "email": email}

@router.post("/verify-otp")
async def verify_otp(email: str, otp: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or user.otp_code != otp:
        raise HTTPException(401, "Wrong OTP")
    user.is_verified = True
    user.otp_code = None
    await db.commit()
    token = create_token(email)
    return {"message": "2FA success! Login done", "access_token": token, "token_type": "bearer"}