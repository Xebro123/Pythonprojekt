from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.gzip import GZipMiddleware
from config import settings
from data_service import data_service
from auth_directus import create_access_token, get_current_user_optional
from schemas import UserCreate, StudentProgress
from cache import progress_cache
from api.courses import router as courses_router
import uvicorn
import subprocess
import tempfile
import os
import hashlib
import httpx

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)

# Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Routery
app.include_router(courses_router)

# Statické soubory + šablony
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ── Pomocné funkce ────────────────────────────────────────────────────────────

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def _google_auth_url() -> str:
    """Sestaví URL pro Google OAuth (přímý flow přes Vercel)."""
    if not settings.GOOGLE_CLIENT_ID:
        return ""
    import urllib.parse
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": f"{settings.APP_URL}/auth/callback",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "online",
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"

async def get_student_progress(user_id: str = None) -> StudentProgress:
    """Pro nepřihlášené vrátí prázdný progress ihned (bez volání Directus)."""
    if not user_id:
        return StudentProgress(name="Host", completed_lessons=[], current_level="Úvod")

    cached = progress_cache.get(f"progress:{user_id}")
    if cached:
        return cached

    progress = await data_service.get_user_progress(user_id)
    progress_cache.set(f"progress:{user_id}", progress, ttl=60)
    return progress


# ── Stránky ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)

    available_courses = [
        {
            "id": "python",
            "title": "Python",
            "subtitle": "Programování s želvou Terry",
            "description": "Nauč se základy programování v Pythonu zábavnou formou s naší přátelskou želvou Terry.",
            "icon": "fab fa-python",
            "emoji": "🐢",
            "color": "success",
            "status": "available",
            "url": "/python",
            "progress": len(student.completed_lessons),
            "total_lessons": 4,
            "age": "10–15 let",
        },
        {
            "id": "javascript",
            "title": "JavaScript",
            "subtitle": "Magie webu",
            "description": "Oživuj webové stránky, vytvárej animace a interaktivní aplikace — přímo v prohlížeči.",
            "icon": "fab fa-js-square",
            "emoji": "🌐",
            "color": "warning",
            "status": "coming_soon",
            "url": "/kurz/javascript",
            "progress": 0,
            "total_lessons": 0,
            "age": "11–15 let",
        },
        {
            "id": "vibe-coding",
            "title": "Vibe Coding",
            "subtitle": "Programování s AI",
            "description": "Moderní způsob tvorby aplikací — programuj spolu s umělou inteligencí a vytvárej věci, které tě baví.",
            "icon": "fas fa-robot",
            "emoji": "🤖",
            "color": "info",
            "status": "coming_soon",
            "url": "/kurz/vibe-coding",
            "progress": 0,
            "total_lessons": 0,
            "age": "12–16 let",
        },
        {
            "id": "kybernetika",
            "title": "Kybernetická bezpečnost",
            "subtitle": "Bezpečně online",
            "description": "Nauč se chránit sebe i svá data na internetu. Hesla, phishing, soukromí — tohle chce každý vědět.",
            "icon": "fas fa-shield-alt",
            "emoji": "🔐",
            "color": "danger",
            "status": "coming_soon",
            "url": "/kurz/kybernetika",
            "progress": 0,
            "total_lessons": 0,
            "age": "10–16 let",
        },
        {
            "id": "pc-life-balance",
            "title": "PC-Life Balance",
            "subtitle": "Zdravý vztah k technologiím",
            "description": "Kdy a jak správně používat digitální svět. Obrazovkový čas, digitální pohoda a zdravé návyky.",
            "icon": "fas fa-balance-scale",
            "emoji": "⚖️",
            "color": "purple",
            "status": "coming_soon",
            "url": "/kurz/pc-life-balance",
            "progress": 0,
            "total_lessons": 0,
            "age": "9–15 let",
        },
    ]

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "courses": available_courses,
        "student": student,
        "user": current_user
    })

@app.get("/python", response_class=HTMLResponse)
async def python_course(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)

    total_lessons = 4
    completed_lessons = len(student.completed_lessons)
    progress_percent = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0

    return templates.TemplateResponse("python_dashboard.html", {
        "request": request,
        "student": student,
        "user": current_user,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percent": progress_percent
    })

@app.get("/predlekce/python", response_class=HTMLResponse)
async def python_intro(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    return templates.TemplateResponse("predlekce.html", {
        "request": request, "student": student, "user": current_user
    })

@app.get("/python-course/lesson-1", response_class=HTMLResponse)
async def python_lesson_1(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    return templates.TemplateResponse("python_lesson_1.html", {
        "request": request, "student": student, "user": current_user
    })

@app.get("/python-course/lesson-2", response_class=HTMLResponse)
async def python_lesson_2(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    return templates.TemplateResponse("python_lesson_2.html", {
        "request": request, "student": student, "user": current_user
    })

@app.get("/python-course/lesson-3", response_class=HTMLResponse)
async def python_lesson_3(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    return templates.TemplateResponse("python_lesson_3.html", {
        "request": request, "student": student, "user": current_user
    })

@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request):
    current_user = await get_current_user_optional(request)
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "student": StudentProgress(name="Host", completed_lessons=[], current_level="Úvod"),
        "user": current_user
    })

@app.get("/profil", response_class=HTMLResponse)
async def profile(request: Request):
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    return templates.TemplateResponse("profil.html", {
        "request": request, "student": student, "user": current_user
    })

@app.get("/kurz/javascript", response_class=HTMLResponse)
async def javascript_course(request: Request):
    current_user = await get_current_user_optional(request)
    return templates.TemplateResponse("coming_soon.html", {
        "request": request, "user": current_user,
        "course_title": "JavaScript", "course_emoji": "🌐",
        "course_color": "#f59e0b",
        "topics": ["Proměnné a funkce", "Manipulace s webem (DOM)", "Animace a efekty", "Jednoduché hry v prohlížeči"],
    })

@app.get("/kurz/vibe-coding", response_class=HTMLResponse)
async def vibe_coding_course(request: Request):
    current_user = await get_current_user_optional(request)
    return templates.TemplateResponse("coming_soon.html", {
        "request": request, "user": current_user,
        "course_title": "Vibe Coding", "course_emoji": "🤖",
        "course_color": "#06b6d4",
        "topics": ["Jak funguje AI asistent", "Prompt engineering pro programátory", "Tvorba aplikací s AI pomocníkem", "Projekty: web, hra, chatbot"],
    })

@app.get("/kurz/kybernetika", response_class=HTMLResponse)
async def kybernetika_course(request: Request):
    current_user = await get_current_user_optional(request)
    return templates.TemplateResponse("coming_soon.html", {
        "request": request, "user": current_user,
        "course_title": "Kybernetická bezpečnost", "course_emoji": "🔐",
        "course_color": "#ef4444",
        "topics": ["Silná hesla a správce hesel", "Phishing a podvodné zprávy", "Soukromí na sociálních sítích", "Bezpečné chování online"],
    })

@app.get("/kurz/pc-life-balance", response_class=HTMLResponse)
async def pc_life_balance_course(request: Request):
    current_user = await get_current_user_optional(request)
    return templates.TemplateResponse("coming_soon.html", {
        "request": request, "user": current_user,
        "course_title": "PC-Life Balance", "course_emoji": "⚖️",
        "course_color": "#8b5cf6",
        "topics": ["Zdravý obrazovkový čas", "Digitální detox a přestávky", "Sociální sítě bez závislosti", "Technologie jako nástroj, ne pán"],
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str):
    current_user = await get_current_user_optional(request)
    courses = await data_service.get_courses()
    if course_id not in courses:
        return templates.TemplateResponse("dashboard.html", {
            "request": request, "courses": courses,
            "student": await get_student_progress(),
            "user": current_user, "error": "Kurz nenalezen"
        })
    return templates.TemplateResponse("kurz.html", {
        "request": request, "course": courses[course_id],
        "course_id": course_id, "student": await get_student_progress(),
        "user": current_user
    })


# ── Přihlášení / Registrace ───────────────────────────────────────────────────

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    error = request.query_params.get("error")
    error_msg = None
    if error == "oauth_failed":
        error_msg = "Přihlášení přes Google se nezdařilo. Zkuste to znovu."
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": error_msg,
        "google_auth_url": _google_auth_url()
    })

@app.post("/login")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    auth_result = await data_service.authenticate_user(email, password)

    if not auth_result or not auth_result.get("data"):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Neplatný email nebo heslo.",
            "email": email,
            "google_auth_url": _google_auth_url()
        }, status_code=401)

    directus_token = auth_result["data"]["access_token"]
    user_info = await data_service.get_user_info_by_token(directus_token)

    user_id = str(user_info.get("id", email)) if user_info else email
    nickname = (user_info.get("first_name") or "") if user_info else ""

    access_token = create_access_token(data={
        "sub": user_id,
        "email": email,
        "nickname": nickname
    })

    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token", value=access_token,
        httponly=True, max_age=86400, samesite="lax"
    )
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {
        "request": request,
        "google_auth_url": _google_auth_url()
    })

@app.post("/register")
async def register(user_data: UserCreate):
    try:
        directus_user = await data_service.register_user(
            email=user_data.email,
            password=user_data.password,
            nickname=user_data.nickname
        )

        if not directus_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registrace selhala. Email může být již použit."
            )

        user_id = str(directus_user.get("id", user_data.email))
        nickname = user_data.nickname or user_data.email.split("@")[0]

        access_token = create_access_token(data={
            "sub": user_id,
            "email": user_data.email,
            "nickname": nickname
        })

        return {
            "success": True,
            "access_token": access_token,
            "message": "Registrace úspěšná",
            "display_name": nickname
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Register error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba při registraci: {str(e)}"
        )

@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response


# ── Google OAuth (přímý flow přes Vercel) ────────────────────────────────────

@app.get("/auth/google")
async def auth_google():
    """Přesměruje na Google OAuth."""
    url = _google_auth_url()
    if not url:
        return RedirectResponse(url="/login?error=google_not_configured")
    return RedirectResponse(url=url)

@app.get("/auth/callback")
async def auth_callback(request: Request, code: str = None, error: str = None):
    """Zpracuje callback po Google OAuth — vymění code za token a získá user info."""
    if error or not code:
        return RedirectResponse(url="/login?error=oauth_failed")

    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return RedirectResponse(url="/login?error=google_not_configured")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. Vymění authorization code za access token
            token_response = await client.post(GOOGLE_TOKEN_URL, data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{settings.APP_URL}/auth/callback",
                "grant_type": "authorization_code",
            })
            if token_response.status_code != 200:
                return RedirectResponse(url="/login?error=oauth_failed")

            access_token = token_response.json().get("access_token")
            if not access_token:
                return RedirectResponse(url="/login?error=oauth_failed")

            # 2. Získá info o uživateli od Googlu
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if userinfo_response.status_code != 200:
                return RedirectResponse(url="/login?error=oauth_failed")

            google_user = userinfo_response.json()
            email = google_user.get("email", "")
            nickname = google_user.get("given_name", "") or email.split("@")[0]
            google_id = google_user.get("sub", "")

        if not email:
            return RedirectResponse(url="/login?error=oauth_failed")

        # 3. Vytvoří uživatele v Directus pokud ještě neexistuje
        #    (chybu ignorujeme — může existovat z dřívějška)
        google_password = hashlib.sha256(
            f"{settings.SECRET_KEY}:{google_id}".encode()
        ).hexdigest()
        await data_service.register_user(
            email=email, password=google_password, nickname=nickname
        )

        # 4. Vytvoří naši session (JWT do cookie)
        our_token = create_access_token(data={
            "sub": f"google:{google_id}",
            "email": email,
            "nickname": nickname
        })

        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key="access_token", value=our_token,
            httponly=True, max_age=86400, samesite="lax"
        )
        return response

    except Exception as e:
        print(f"❌ OAuth callback error: {e}")
        return RedirectResponse(url="/login?error=oauth_failed")


# ── API ───────────────────────────────────────────────────────────────────────

@app.post("/run_code")
async def run_code(code: str = Form(...)):
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            ['python', temp_file],
            capture_output=True, text=True,
            timeout=5, encoding='utf-8', errors='replace'
        )
        os.unlink(temp_file)
        return {"output": result.stdout, "error": result.stderr, "return_code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Kód běžel příliš dlouho (max 5 sekund)"}
    except Exception as e:
        return {"error": f"Chyba: {str(e)}"}

@app.post("/update_progress")
async def update_progress(request: Request, lesson_id: int = Form(...)):
    current_user = await get_current_user_optional(request)
    if not current_user:
        return {"success": False, "error": "Nejsi přihlášen(a)"}

    user_id = current_user.get("id")
    # Invalidace cache po aktualizaci pokroku
    progress_cache.delete(f"progress:{user_id}")

    success = await data_service.update_user_progress(user_id, str(lesson_id), True)
    return {"success": success}

@app.get("/api/health")
async def health_check():
    import httpx
    health_status = {
        "app": "ok",
        "directus": {
            "url": settings.DIRECTUS_URL,
            "reachable": False,
            "authenticated": False,
            "collections": []
        }
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                r = await client.get(f"{settings.DIRECTUS_URL}/server/ping")
                health_status["directus"]["reachable"] = r.status_code == 200
            except Exception as e:
                health_status["directus"]["error"] = str(e)

            if settings.DIRECTUS_TOKEN:
                try:
                    headers = {"Authorization": f"Bearer {settings.DIRECTUS_TOKEN}"}
                    r = await client.get(f"{settings.DIRECTUS_URL}/collections", headers=headers)
                    health_status["directus"]["authenticated"] = r.status_code == 200
                    if r.status_code == 200:
                        health_status["directus"]["collections"] = [
                            c["collection"] for c in r.json().get("data", [])
                        ]
                except Exception as e:
                    health_status["directus"]["auth_error"] = str(e)
    except Exception as e:
        health_status["error"] = str(e)
    return health_status


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
