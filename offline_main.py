from fastapi import FastAPI, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, init_database, User, Course, Lesson, UserProgress, Achievement, UserAchievement
from auth import authenticate_user, create_access_token, get_current_user_optional, create_user
from schemas import UserCreate, UserLogin, StudentProgress, UserProgressBase
import uvicorn
import subprocess
import tempfile
import os
from datetime import datetime, timedelta
import json

app = FastAPI(title="Python Kurz - Offline Verze", description="Výuková platforma pro Python (offline)")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Offline verze - jeden "host" uživatel pro celou rodinu
OFFLINE_USER = {
    "id": 1,
    "username": "host",
    "full_name": "Host",
    "completed_lessons": [],
    "current_level": "Úvod",
    "total_points": 0,
    "achievements": []
}

# Inicializace databáze při startu
@app.on_event("startup")
async def startup_event():
    init_database()

# Helper funkce pro získání dat z databáze
def get_courses_data(db: Session):
    """Získání všech kurzů z databáze"""
    courses = db.query(Course).filter(Course.is_active == True).order_by(Course.order_index).all()
    return {course.course_id: {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "level": course.level,
        "lessons": [{
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "lesson_number": lesson.lesson_number
        } for lesson in course.lessons if lesson.is_active]
    } for course in courses}

def get_offline_progress() -> StudentProgress:
    """Získání pokroku pro offline verzi"""
    # Načtení z JSON souboru (místo databáze)
    progress_file = "offline_progress.json"
    if os.path.exists(progress_file):
        try:
            with open(progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return StudentProgress(**data)
        except:
            pass
    
    # Výchozí hodnoty
    return StudentProgress(
        name="Host",
        completed_lessons=[],
        current_level="Úvod",
        total_points=0,
        achievements=[]
    )

def save_offline_progress(progress: StudentProgress):
    """Uložení pokroku do JSON souboru"""
    progress_file = "offline_progress.json"
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress.dict(), f, ensure_ascii=False, indent=2)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    courses = get_courses_data(db)
    student = get_offline_progress()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "courses": courses,
        "student": student,
        "user": None,  # Offline verze nemá přihlašování
        "is_offline": True
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str, db: Session = Depends(get_db)):
    courses = get_courses_data(db)
    student = get_offline_progress()
    
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student,
            "user": None,
            "is_offline": True,
            "error": "Kurz nenalezen"
        })
    
    return templates.TemplateResponse("kurz.html", {
        "request": request,
        "course": courses[course_id],
        "course_id": course_id,
        "student": student,
        "user": None,
        "is_offline": True
    })

@app.get("/lekce/{course_id}/{lesson_id}", response_class=HTMLResponse)
async def lesson_page(request: Request, course_id: str, lesson_id: int, db: Session = Depends(get_db)):
    courses = get_courses_data(db)
    student = get_offline_progress()
    
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student,
            "user": None,
            "is_offline": True,
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
            "student": student,
            "user": None,
            "is_offline": True,
            "error": "Lekce nenalezena"
        })
    
    return templates.TemplateResponse("lekce.html", {
        "request": request,
        "course": course,
        "course_id": course_id,
        "lesson": lesson,
        "student": student,
        "user": None,
        "is_offline": True
    })

@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request, db: Session = Depends(get_db)):
    student = get_offline_progress()
    
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "student": student,
        "user": None,
        "is_offline": True
    })

@app.post("/run_code")
async def run_code(code: str = Form(...)):
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Run the code
        result = subprocess.run(
            ['python', temp_file],
            capture_output=True,
            text=True,
            timeout=5
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
async def profile(request: Request, db: Session = Depends(get_db)):
    student = get_offline_progress()
    
    return templates.TemplateResponse("profil.html", {
        "request": request,
        "student": student,
        "user": None,
        "is_offline": True
    })

@app.post("/update_progress")
async def update_progress(lesson_id: int = Form(...)):
    # Offline verze - ukládá do JSON souboru
    progress = get_offline_progress()
    
    if lesson_id not in progress.completed_lessons:
        progress.completed_lessons.append(lesson_id)
        progress.total_points += 10  # 10 bodů za lekci
        
        # Simulace achievementů
        if len(progress.completed_lessons) == 1:
            progress.achievements.append({
                "name": "První kroky",
                "description": "Dokončili jste svou první lekci!",
                "icon": "fas fa-baby",
                "points": 10
            })
        
        save_offline_progress(progress)
    
    return {"success": True, "completed_lessons": progress.completed_lessons}

# Offline verze nemá přihlašování
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("offline_info.html", {
        "request": request,
        "message": "Offline verze nevyžaduje přihlášení. Váš pokrok se ukládá lokálně."
    })

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("offline_info.html", {
        "request": request,
        "message": "Offline verze nevyžaduje registraci. Váš pokrok se ukládá lokálně."
    })

if __name__ == "__main__":
    print("🐍 Python Kurz - Offline Verze")
    print("📁 Data se ukládají do offline_progress.json")
    print("🌐 Aplikace běží na: http://localhost:8000")
    print("⚠️  Tato verze nevyžaduje přihlášení")
    uvicorn.run(app, host="0.0.0.0", port=8000)