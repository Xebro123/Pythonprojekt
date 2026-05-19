from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Request
from config import settings

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

async def get_current_user_optional(request: Request) -> Optional[dict]:
    """Vrátí dict s user info z cookie (nebo None pro nepřihlášené)."""
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    if not token:
        return None

    payload = verify_token(token)
    if not payload:
        return None

    user_id = payload.get("sub")
    email = payload.get("email", "")
    nickname = payload.get("nickname", "")
    display_name = nickname or (email.split("@")[0] if email else "Student")

    return {
        "id": user_id,
        "email": email,
        "nickname": nickname,
        "display_name": display_name,
        "username": display_name,  # zpětná kompatibilita pro šablony
    }
