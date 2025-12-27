from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import settings
from data_service import data_service
from auth_directus import create_access_token, get_current_user_optional
from schemas import UserCreate, UserLogin, StudentProgress
from api.courses import router as courses_router
import uvicorn
import subprocess
import tempfile
import os
from datetime import datetime, timedelta

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)

# Include API routers
app.include_router(courses_router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Helper funkce pro získání dat z Directus
async def get_courses_data():
    """Získání všech kurzů z Directus"""
    return await data_service.get_courses()

async def get_student_progress(user_id: str = None) -> StudentProgress:
    """Získání pokroku studenta z Directus"""
    if user_id:
        return await data_service.get_user_progress(user_id)
    else:
        return StudentProgress(name="Host", completed_lessons=[], current_level="Úvod")

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Hlavní dashboard platformy"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    # Seznam dostupných kurzů na platformě
    available_courses = [
        {
            "id": "python",
            "title": "Python Kurz",
            "description": "Naučte se základy programování v Pythonu",
            "icon": "fas fa-python",
            "color": "success",
            "status": "available",
            "progress": len(student.completed_lessons) if student else 0,
            "total_lessons": 10
        },
        {
            "id": "javascript",
            "title": "JavaScript Kurz", 
            "description": "Webové programování s JavaScriptem",
            "icon": "fab fa-js-square",
            "color": "warning",
            "status": "coming_soon",
            "progress": 0,
            "total_lessons": 0
        },
        {
            "id": "ai",
            "title": "AI Kurz",
            "description": "Umělá inteligence pro začátečníky",
            "icon": "fas fa-robot",
            "color": "info",
            "status": "coming_soon", 
            "progress": 0,
            "total_lessons": 0
        }
    ]
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "courses": available_courses,
        "student": student,
        "user": current_user
    })

@app.get("/python", response_class=HTMLResponse)
async def python_course(request: Request):
    """Python kurz dashboard - seznam lekcí"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    # Počet lekcí
    total_lessons = 4  # Předlekce + 3 lekce
    completed_lessons = len(student.completed_lessons) if student else 0
    progress_percent = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
    
    return templates.TemplateResponse("python_dashboard.html", {
        "request": request,
        "student": student,
        "user": current_user,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "progress_percent": progress_percent
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str):
    """Stránka kurzu"""
    courses = await get_courses_data()
    if course_id not in courses:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "courses": courses,
            "student": await get_student_progress(),
            "error": "Kurz nenalezen"
        })
    
    return templates.TemplateResponse("kurz.html", {
        "request": request,
        "course": courses[course_id],
        "course_id": course_id,
        "student": await get_student_progress()
    })

@app.get("/predlekce/python", response_class=HTMLResponse)
async def python_intro(request: Request):
    """Předlekce - Vítej v Pythonu s Terry želvou"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    return templates.TemplateResponse("predlekce.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.get("/python-course/lesson-1", response_class=HTMLResponse)
async def python_lesson_1(request: Request):
    """Lekce 1: Nauč želvu kreslit"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    return templates.TemplateResponse("python_lesson_1.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.get("/python-course/lesson-2", response_class=HTMLResponse)
async def python_lesson_2(request: Request):
    """Lekce 2: Tvoje první kouzelná spirála"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    return templates.TemplateResponse("python_lesson_2.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.get("/python-course/lesson-3", response_class=HTMLResponse)
async def python_lesson_3(request: Request):
    """Lekce 3: Barevná spirála (coming soon)"""
    current_user = await get_current_user_optional(request)
    student = await get_student_progress(current_user.get("id") if current_user else None)
    
    return templates.TemplateResponse("python_lesson_3.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.get("/lekce/{course_id}/{lesson_id}", response_class=HTMLResponse)
async def lesson_page(request: Request, course_id: str, lesson_id: int):
    """Stránka lekce"""
    courses = await get_courses_data()
    if course_id not in courses:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "courses": courses,
            "student": await get_student_progress(),
            "error": "Kurz nenalezen"
        })
    
    course = courses[course_id]
    lesson = None
    for l in course["lessons"]:
        if l["id"] == lesson_id:
            lesson = l
            break
    
    if not lesson:
        return templates.TemplateResponse("kurz.html", {
            "request": request,
            "course": course,
            "course_id": course_id,
            "student": await get_student_progress(),
            "error": "Lekce nenalezena"
        })
    
    return templates.TemplateResponse("lekce.html", {
        "request": request,
        "course": course,
        "course_id": course_id,
        "lesson": lesson,
        "student": await get_student_progress()
    })

@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request):
    """Python Playground"""
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "student": await get_student_progress()
    })

@app.post("/run_code")
async def run_code(code: str = Form(...)):
    """Spuštění Python kódu"""
    try:
        # Create temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            # Add encoding declaration to the file
            f.write('# -*- coding: utf-8 -*-\n')
            f.write(code)
            temp_file = f.name
        
        # Run the code with UTF-8 encoding
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5,
            encoding='utf-8',
            errors='replace'
        )
        
        # Clean up
        os.unlink(temp_file)
        
        return {
            "output": result.stdout,
            "error": result.stderr,
            "return_code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Kód běžel příliš dlouho (max 5 sekund)"}
    except Exception as e:
        return {"error": f"Chyba: {str(e)}"}

@app.get("/profil", response_class=HTMLResponse)
async def profile(request: Request):
    """Profil studenta"""
    return templates.TemplateResponse("profil.html", {
        "request": request,
        "student": await get_student_progress()
    })

@app.post("/update_progress")
async def update_progress(lesson_id: int = Form(...)):
    """Aktualizace pokroku studenta"""
    # V online režimu potřebujeme user_id z session/tokenu
    # Prozatím použijeme placeholder
    user_id = "1"  # TODO: Získat z autentifikace
    
    success = await data_service.update_user_progress(user_id, str(lesson_id), True)
    
    if success:
        return {"success": True}
    else:
        return {"success": False, "error": "Chyba při aktualizaci pokroku"}

# Autentifikace routes
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Přihlašovací stránka"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """Přihlášení studenta pomocí username"""
    print(f"🔐 Login attempt for username: {username}")
    
    # TODO: Implementovat ověření studenta v Directus kolekci 'students'
    # Prozatím vytvoříme JWT token bez ověření (DOČASNÉ ŘEŠENÍ)
    access_token = create_access_token(data={"sub": username})
    
    print(f"✅ Login successful, creating token for: {username}")
    
    # Redirect na hlavní stránku s tokenem
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=86400)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registrační stránka"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(user_data: UserCreate):
    """Registrace nového studenta"""
    try:
        print(f"🚀 Starting registration in main.py for: {user_data.username}")
        register_result = await data_service.register_user(
            user_data.username, 
            user_data.email,
            user_data.password
        )
        
        print(f"🔍 register_result in main.py: {register_result}")
        print(f"🔍 register_result type: {type(register_result)}")
        print(f"🔍 register_result bool: {bool(register_result)}")
        
        if register_result:
            # Automatické přihlášení po registraci
            access_token = create_access_token(data={"sub": user_data.username})
            
            print(f"✅ Registration successful, returning success response")
            return {
                "success": True,
                "access_token": access_token,
                "message": "Registrace úspěšná",
                "username": user_data.username
            }
        else:
            print(f"❌ register_result is falsy, raising HTTPException")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chyba při registraci. Uživatelské jméno nebo email už mohou být použity."
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Registration error in main.py: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chyba při registraci: {str(e)}"
        )

@app.post("/logout")
async def logout():
    """Odhlášení uživatele"""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

@app.get("/api/health")
async def health_check():
    """Health check endpoint pro testování Directus připojení"""
    import httpx
    from config import settings
    
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
        # Test 1: Je Directus dostupný?
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(f"{settings.DIRECTUS_URL}/server/ping")
                health_status["directus"]["reachable"] = response.status_code == 200
            except Exception as e:
                health_status["directus"]["error"] = f"Cannot reach Directus: {str(e)}"
            
            # Test 2: Funguje autentifikace?
            if settings.DIRECTUS_TOKEN:
                try:
                    headers = {"Authorization": f"Bearer {settings.DIRECTUS_TOKEN}"}
                    response = await client.get(f"{settings.DIRECTUS_URL}/collections", headers=headers)
                    health_status["directus"]["authenticated"] = response.status_code == 200
                    
                    if response.status_code == 200:
                        collections = response.json().get("data", [])
                        health_status["directus"]["collections"] = [c["collection"] for c in collections]
                    else:
                        health_status["directus"]["auth_error"] = response.text
                except Exception as e:
                    health_status["directus"]["auth_error"] = str(e)
    except Exception as e:
        health_status["error"] = str(e)
    
    return health_status

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)