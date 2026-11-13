# Secure Login System with 2FA using FastAPI

Secure login system with Two-Factor Authentication (2FA) using FastAPI. Users cannot login with password alone. After correct email and password, OTP is generated. Only after verifying OTP, user receives JWT Access Token.

## Features
- User Signup with Email & Password
- Password Hashing using pbkdf2_sha256
- Login with OTP Generation (6-digit)
- OTP Verification (2FA)
- JWT Token Authentication
- Duplicate User Prevention
- SQLite Database

## Technologies Used
- Python 3.14
- FastAPI, Uvicorn
- SQLite, SQLAlchemy
- Passlib, Python-JOSE [JWT]
- Swagger UI

## API Endpoints
- POST /api/auth/signup -> Register new user
- POST /api/auth/login -> Login & generate OTP
- POST /api/auth/verify-otp -> Verify OTP & get Token

## How to Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
