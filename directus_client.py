import httpx
from typing import Dict, List, Optional
from config import settings

class DirectusClient:
    def __init__(self):
        self.base_url = settings.DIRECTUS_URL.rstrip('/')
        self.token = settings.DIRECTUS_TOKEN
        self._admin_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        } if self.token else {"Content-Type": "application/json"}

    # ── Auth ──────────────────────────────────────────────────────────────────

    async def authenticate(self, email: str, password: str) -> Optional[Dict]:
        """Přihlášení emailem+heslem přes Directus /auth/login."""
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{self.base_url}/auth/login",
                    json={"email": email, "password": password}
                )
                if response.status_code == 200:
                    return response.json()   # {"data": {"access_token": ..., "refresh_token": ...}}
                return None
        except Exception as e:
            print(f"❌ Auth error: {e}")
            return None

    async def create_directus_user(self, email: str, password: str, nickname: str = None) -> Optional[Dict]:
        """Vytvoří nového uživatele v directus_users (vyžaduje admin token)."""
        data = {"email": email, "password": password, "status": "active"}
        if nickname:
            data["first_name"] = nickname
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.post(
                    f"{self.base_url}/users",
                    json=data,
                    headers=self._admin_headers
                )
                print(f"📊 Create user status: {response.status_code}")
                if response.status_code in [200, 201]:
                    return response.json().get("data")
                print(f"❌ Create user failed: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Create user exception: {e}")
            return None

    async def get_user_info_by_token(self, directus_token: str) -> Optional[Dict]:
        """Vrátí info o přihlášeném uživateli z /users/me."""
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/users/me",
                    headers={"Authorization": f"Bearer {directus_token}"}
                )
                if response.status_code == 200:
                    return response.json().get("data")
                return None
        except Exception as e:
            print(f"❌ Get user me error: {e}")
            return None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Vrátí uživatele podle ID (admin token)."""
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/users/{user_id}",
                    headers=self._admin_headers
                )
                if response.status_code == 200:
                    return response.json().get("data")
                return None
        except Exception:
            return None

    # ── Kurzy ─────────────────────────────────────────────────────────────────

    async def get_courses(self) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/items/courses?filter[status][_eq]=published&sort=sort",
                    headers=self._admin_headers
                )
                response.raise_for_status()
                return response.json().get("data", [])
        except Exception:
            return []

    async def get_course(self, course_id: str) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/items/courses/{course_id}",
                    headers=self._admin_headers
                )
                response.raise_for_status()
                return response.json().get("data")
        except Exception:
            return None

    # ── Pokrok uživatele ──────────────────────────────────────────────────────

    async def get_user_progress(self, user_id: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/items/user_progress?filter[user][_eq]={user_id}",
                    headers=self._admin_headers
                )
                response.raise_for_status()
                return response.json().get("data", [])
        except Exception:
            return []

    async def update_user_progress(self, user_id: str, lesson_id: str,
                                   completed: bool = True,
                                   completion_percentage: float = 100.0,
                                   time_spent: int = 0) -> Optional[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                existing = await client.get(
                    f"{self.base_url}/items/user_progress?filter[user][_eq]={user_id}&filter[lesson][_eq]={lesson_id}",
                    headers=self._admin_headers
                )
                existing_data = existing.json().get("data", [])

                if existing_data:
                    progress_id = existing_data[0]["id"]
                    r = await client.patch(
                        f"{self.base_url}/items/user_progress/{progress_id}",
                        json={"completed": completed, "completion_percentage": completion_percentage, "time_spent": time_spent},
                        headers=self._admin_headers
                    )
                else:
                    r = await client.post(
                        f"{self.base_url}/items/user_progress",
                        json={"user": user_id, "lesson": lesson_id, "completed": completed,
                              "completion_percentage": completion_percentage, "time_spent": time_spent},
                        headers=self._admin_headers
                    )
                return r.json().get("data")
        except Exception:
            return None

    # ── Achievementy ──────────────────────────────────────────────────────────

    async def get_achievements(self) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/items/achievements?filter[status][_eq]=published",
                    headers=self._admin_headers
                )
                return response.json().get("data", [])
        except Exception:
            return []

    async def get_user_achievements(self, user_id: str) -> List[Dict]:
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                response = await client.get(
                    f"{self.base_url}/items/user_achievements?filter[user][_eq]={user_id}",
                    headers=self._admin_headers
                )
                return response.json().get("data", [])
        except Exception:
            return []

directus = DirectusClient()
