from typing import Dict, List, Optional
from directus_client import directus
from schemas import StudentProgress

class DataService:

    # ── Auth ──────────────────────────────────────────────────────────────────

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict]:
        """Ověří email+heslo přes Directus. Vrátí {"data": {"access_token": ...}} nebo None."""
        return await directus.authenticate(email, password)

    async def register_user(self, email: str, password: str, nickname: str = None) -> Optional[Dict]:
        """Vytvoří nového uživatele v directus_users."""
        try:
            result = await directus.create_directus_user(email, password, nickname)
            if result:
                print(f"✅ User registered: {email}")
            else:
                print(f"❌ Registration failed for: {email}")
            return result
        except Exception as e:
            print(f"❌ register_user exception: {e}")
            return None

    async def get_user_info_by_token(self, directus_token: str) -> Optional[Dict]:
        """Vrátí info o uživateli z /users/me (po přihlášení)."""
        return await directus.get_user_info_by_token(directus_token)

    async def get_user_info_by_id(self, user_id: str) -> Optional[Dict]:
        return await directus.get_user_by_id(user_id)

    # ── Kurzy ─────────────────────────────────────────────────────────────────

    async def get_courses(self) -> Dict[str, Dict]:
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

    # ── Pokrok ────────────────────────────────────────────────────────────────

    async def get_user_progress(self, user_id: str) -> StudentProgress:
        progress_data = await directus.get_user_progress(user_id)
        completed_lessons = [p["lesson"] for p in progress_data if p.get("completed")]

        user_info = await self.get_user_info_by_id(user_id)
        display_name = ""
        if user_info:
            display_name = user_info.get("first_name") or user_info.get("email", "Student").split("@")[0]

        return StudentProgress(
            name=display_name or "Student",
            completed_lessons=completed_lessons,
            current_level="Úvod"
        )

    async def update_user_progress(self, user_id: str, lesson_id: str, completed: bool = True) -> bool:
        result = await directus.update_user_progress(user_id, lesson_id, completed)
        return result is not None

data_service = DataService()
