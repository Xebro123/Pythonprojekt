from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings
from data_service import data_service

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Ověření hesla"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashování hesla"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Vytvoření JWT tokenu"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Ověření JWT tokenu"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Získání aktuálního uživatele z tokenu"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Získání uživatele z Directus
    user = await data_service.get_user_by_username(user_id)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_user_optional(request: Request) -> Optional[dict]:
    """Získání aktuálního uživatele (volitelné)"""
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
        
        payload = verify_token(token)
        if payload is None:
            return None
        
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        
        # Získání uživatele z Directus
        user = await data_service.get_user_by_username(user_id)
        return user
    except (ValueError, HTTPException):
        return None

async def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Autentifikace uživatele přes Directus"""
    return await data_service.authenticate_user(username, password)

async def create_user(username: str, email: str, password: str, full_name: str = None) -> dict:
    """Vytvoření nového uživatele přes Directus"""
    from schemas import UserCreate
    
    user_data = UserCreate(
        username=username,
        email=email,
        password=password,
        full_name=full_name
    )
    
    return await data_service.create_user(user_data)
