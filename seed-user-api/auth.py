from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User, hash_password
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional


SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel, EmailStr

# ✅ Input model (for registering new users)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"  # Default role

# ✅ Response model (for returning user data, without password)
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True  # ✅ Enables ORM mode for SQLAlchemy conversion


def create_access_token(email: str):
    """Generate JWT token. Admin users get non-expiring tokens."""
    payload = {"sub": email}

    # If NOT admin, add expiry
    if email != "admin@example.com":
        expire = datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
        payload["exp"] = expire.timestamp()

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


from fastapi import Security, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    """Decode JWT and verify expiry unless user is admin."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        exp: Optional[int] = payload.get("exp")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: No email found")

        # If user is NOT admin, enforce expiration check
        if email != "admin@example.com" and exp is not None:
            if datetime.utcnow() > datetime.utcfromtimestamp(exp):
                raise HTTPException(status_code=401, detail="Token expired")

        return email  # Return user email (or role, if needed)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")




@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if request.email == "admin@example.com" and request.password == "admin123":
        access_token = create_access_token(request.email)
        print({"access_token": access_token, "role": user.role, "token_type": "bearer"})
        return {"access_token": access_token, "token_type": "bearer"}
    access_token = create_access_token(request.email)
    #token = jwt.encode({"sub": user.email, "role": user.role}, SECRET_KEY, algorithm="HS256")
    print({"access_token": access_token, "role": user.role})
    return {"access_token": access_token, "role": user.role, "token_type": "bearer"}

# @router.post("/login")
# async def login(request: LoginRequest):
#     if request.email == "admin@example.com" and request.password == "admin123":
#         return {"access_token": "fake_token"}
#     raise HTTPException(status_code=401, detail="Invalid credentials")



@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)  # Hash the password before storing
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # ✅ Ensures the user object includes ID and other fields

    return new_user  # ✅ This now contains all required fields
