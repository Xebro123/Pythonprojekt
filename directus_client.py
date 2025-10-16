import httpx
from typing import Dict, List, Optional, Any
from config import settings
import json

class DirectusClient:
    """Klient pro komunikaci s Directus API"""
    
    def __init__(self):
        self.base_url = settings.DIRECTUS_URL.rstrip('/')
        self.token = settings.DIRECTUS_TOKEN
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}" if self.token else None
        }
        # Odstraníme None hodnoty z headers
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Základní HTTP request"""
        url = f"{self.base_url}/items/{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                if method.upper() == "GET":
                    response = await client.get(url, headers=self.headers)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                elif method.upper() == "PATCH":
                    response = await client.patch(url, headers=self.headers, json=data)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Neplatná HTTP metoda: {method}")
                
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Directus API chyba: {e}")
                raise
    
    # Autentifikace
    async def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Přihlášení uživatele"""
        try:
            url = f"{self.base_url}/auth/login"
            data = {"email": email, "password": password}
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError:
            return None
    
    async def register(self, email: str, password: str, first_name: str, last_name: str) -> Optional[Dict]:
        """Registrace nového uživatele"""
        try:
            url = f"{self.base_url}/users"
            data = {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "status": "active"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError:
            return None
    
    # Kurzy
    async def get_courses(self) -> List[Dict]:
        """Získání všech kurzů"""
        try:
            result = await self._make_request("GET", "courses?filter[status][_eq]=published&sort=sort")
            return result.get("data", [])
        except Exception:
            return []
    
    async def get_course(self, course_id: str) -> Optional[Dict]:
        """Získání konkrétního kurzu"""
        try:
            result = await self._make_request("GET", f"courses/{course_id}")
            return result.get("data")
        except Exception:
            return None
    
    # Lekce
    async def get_lessons(self, course_id: Optional[str] = None) -> List[Dict]:
        """Získání lekcí (volitelně filtrované podle kurzu)"""
        try:
            endpoint = "lessons"
            if course_id:
                endpoint += f"?filter[course][_eq]={course_id}&sort=lesson_number"
            else:
                endpoint += "?sort=lesson_number"
            
            result = await self._make_request("GET", endpoint)
            return result.get("data", [])
        except Exception:
            return []
    
    async def get_lesson(self, lesson_id: str) -> Optional[Dict]:
        """Získání konkrétní lekce"""
        try:
            result = await self._make_request("GET", f"lessons/{lesson_id}")
            return result.get("data")
        except Exception:
            return None
    
    # Pokrok uživatele
    async def get_user_progress(self, user_id: str) -> List[Dict]:
        """Získání pokroku uživatele"""
        try:
            result = await self._make_request("GET", f"user_progress?filter[user][_eq]={user_id}")
            return result.get("data", [])
        except Exception:
            return []
    
    async def update_user_progress(self, user_id: str, lesson_id: str, completed: bool = True, 
                                 completion_percentage: float = 100.0, time_spent: int = 0) -> Optional[Dict]:
        """Aktualizace pokroku uživatele"""
        try:
            # Nejdříve zkusíme najít existující záznam
            existing = await self._make_request("GET", f"user_progress?filter[user][_eq]={user_id}&filter[lesson][_eq]={lesson_id}")
            
            if existing.get("data"):
                # Aktualizujeme existující záznam
                progress_id = existing["data"][0]["id"]
                data = {
                    "completed": completed,
                    "completion_percentage": completion_percentage,
                    "time_spent": time_spent
                }
                result = await self._make_request("PATCH", f"user_progress/{progress_id}", data)
            else:
                # Vytvoříme nový záznam
                data = {
                    "user": user_id,
                    "lesson": lesson_id,
                    "completed": completed,
                    "completion_percentage": completion_percentage,
                    "time_spent": time_spent
                }
                result = await self._make_request("POST", "user_progress", data)
            
            return result.get("data")
        except Exception:
            return None
    
    # Achievementy
    async def get_achievements(self) -> List[Dict]:
        """Získání všech achievementů"""
        try:
            result = await self._make_request("GET", "achievements?filter[status][_eq]=published")
            return result.get("data", [])
        except Exception:
            return []
    
    async def get_user_achievements(self, user_id: str) -> List[Dict]:
        """Získání achievementů uživatele"""
        try:
            result = await self._make_request("GET", f"user_achievements?filter[user][_eq]={user_id}")
            return result.get("data", [])
        except Exception:
            return []
    
    async def grant_achievement(self, user_id: str, achievement_id: str) -> Optional[Dict]:
        """Udělení achievementu uživateli"""
        try:
            data = {
                "user": user_id,
                "achievement": achievement_id
            }
            result = await self._make_request("POST", "user_achievements", data)
            return result.get("data")
        except Exception:
            return None

# Globální instance klienta
directus = DirectusClient()
