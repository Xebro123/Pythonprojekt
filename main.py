from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import settings
from data_service import data_service
from auth_directus import create_access_token, get_current_user_optional
from schemas import UserCreate, UserLogin, StudentProgress
import uvicorn
import subprocess
import tempfile
import os
from datetime import datetime, timedelta

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION)

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
async def home(request: Request):
    """Hlavní stránka"""
    courses = await get_courses_data()
    student = await get_student_progress()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "courses": courses,
        "student": student
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str):
    """Stránka kurzu"""
    courses = await get_courses_data()
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
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

@app.get("/lekce/{course_id}/{lesson_id}", response_class=HTMLResponse)
async def lesson_page(request: Request, course_id: str, lesson_id: int):
    """Stránka lekce"""
    courses = await get_courses_data()
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
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
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    """Přihlášení uživatele"""
    auth_result = await data_service.authenticate_user(email, password)
    
    if auth_result:
        # Vytvoření JWT tokenu
        access_token = create_access_token(data={"sub": email})
        
        # Redirect na hlavní stránku s tokenem
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    else:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Neplatné přihlašovací údaje"
        })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registrační stránka"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, email: str = Form(...), password: str = Form(...), 
                  first_name: str = Form(...), last_name: str = Form(...)):
    """Registrace nového uživatele"""
    register_result = await data_service.register_user(email, password, first_name, last_name)
    
    if register_result:
        # Automatické přihlášení po registraci
        access_token = create_access_token(data={"sub": email})
        
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return response
    else:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Chyba při registraci. Email může být již používán."
        })

@app.post("/logout")
async def logout():
    """Odhlášení uživatele"""
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="access_token")
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)