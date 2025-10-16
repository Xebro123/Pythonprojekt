import os
from typing import Optional

class Settings:
    """Konfigurace aplikace"""
    
    # Directus konfigurace (online verze)
    DIRECTUS_URL: str = os.getenv("DIRECTUS_URL", "http://188.245.190.72:8057")
    DIRECTUS_TOKEN: Optional[str] = os.getenv("DIRECTUS_TOKEN")
    
    # JWT konfigurace
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Aplikace
    APP_TITLE: str = "NextGen Coders"
    APP_DESCRIPTION: str = "Platforma pro výuku programování"

# Globální instance nastavení
settings = Settings()
