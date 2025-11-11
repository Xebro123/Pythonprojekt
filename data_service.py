from typing import Dict, List, Optional, Any
from config import settings
from directus_client import directus
from schemas import StudentProgress

class DataService:
    """Data vrstva pro online verzi (Directus + PostgreSQL)"""
    
    # Autentifikace
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Přihlášení uživatele přes Directus"""
        return await directus.authenticate(email, password)
    
    async def register_user(self, username: str, email: str, password: str) -> Optional[Dict]:
        """Registrace nového studenta přes Directus"""
        try:
            print(f"🔄 Calling directus.register for: {username}")
            result = await directus.register(username, email, password)
            print(f"🔍 Result from directus.register: {result}")
            print(f"🔍 Result type: {type(result)}")
            print(f"🔍 Result bool: {bool(result)}")
            
            if result:
                print(f"✅ Student registered successfully in data_service: {username}")
                return result
            else:
                print(f"❌ Failed to register student in data_service: {username}")
                return None
        except Exception as e:
            print(f"❌ Registration error in data_service: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    # Kurzy
    async def get_courses(self) -> Dict[str, Dict]:
        """Získání všech kurzů z Directus"""
        courses_data = await directus.get_courses()
        return {
            course["course_id"]: {
                "id": course["id"],
                "title": course["title"],
                "description": course["description"],
                "level": course["level"],
                "lessons": [
                    {
                        "id": lesson["id"],
                        "title": lesson["title"],
                        "description": lesson["description"],
                        "lesson_number": lesson["lesson_number"]
                    }
                    for lesson in course.get("lessons", [])
                ]
            }
            for course in courses_data
        }
    
    async def get_course(self, course_id: str) -> Optional[Dict]:
        """Získání konkrétního kurzu z Directus"""
        return await directus.get_course(course_id)
    
    # Pokrok uživatele
    async def get_user_progress(self, user_id: str) -> StudentProgress:
        """Získání pokroku uživatele z Directus"""
        progress_data = await directus.get_user_progress(user_id)
        completed_lessons = [str(p["lesson"]) for p in progress_data if p.get("completed")]
        
        # Získáme jméno uživatele z Directus
        user_info = await self.get_user_info(user_id)
        user_name = user_info.get("first_name", "User") if user_info else "User"
        
        return StudentProgress(
            name=user_name,
            completed_lessons=completed_lessons,
            current_level="Úvod"  # TODO: Vypočítat z pokroku
        )
    
    async def update_user_progress(self, user_id: str, lesson_id: str, completed: bool = True) -> bool:
        """Aktualizace pokroku uživatele v Directus"""
        result = await directus.update_user_progress(user_id, lesson_id, completed)
        return result is not None
    
    # Achievementy
    async def get_achievements(self) -> List[Dict]:
        """Získání všech achievementů z Directus"""
        return await directus.get_achievements()
    
    async def get_user_achievements(self, user_id: str) -> List[Dict]:
        """Získání achievementů uživatele z Directus"""
        return await directus.get_user_achievements(user_id)
    
    async def grant_achievement(self, user_id: str, achievement_id: str) -> bool:
        """Udělení achievementu uživateli v Directus"""
        result = await directus.grant_achievement(user_id, achievement_id)
        return result is not None
    
    # Helper metody
    async def get_user_info(self, user_id: str) -> Optional[Dict]:
        """Získání informací o uživateli z Directus"""
        try:
            # Directus API pro získání uživatele
            import httpx
            url = f"{settings.DIRECTUS_URL}/users/{user_id}"
            headers = {"Authorization": f"Bearer {settings.DIRECTUS_TOKEN}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json().get("data")
        except Exception:
            return None

# Globální instance služby
data_service = DataService()