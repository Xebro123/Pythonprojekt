import os
from typing import Optional

class Settings:
    # Directus (online backend)
    DIRECTUS_URL: str = os.getenv("DIRECTUS_URL", "http://188.245.190.72:8057")
    DIRECTUS_TOKEN: Optional[str] = os.getenv("DIRECTUS_TOKEN")

    # Veřejná URL aplikace (pro OAuth callback)
    APP_URL: str = os.getenv("APP_URL", "https://pythonprojekt-ten.vercel.app")

    # Google OAuth (přímý flow přes Vercel, bez Directusu)
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h

    # Aplikace
    APP_TITLE: str = "NextGen Coders"
    APP_DESCRIPTION: str = "Platforma pro výuku programování"

settings = Settings()
