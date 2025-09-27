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

app = FastAPI(title="Python Kurz pro Základní Školy", description="Výuková platforma pro Python")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

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

def get_student_progress(db: Session, user: User = None) -> StudentProgress:
    """Získání pokroku studenta z databáze"""
    if not user:
        return StudentProgress(name="Host", completed_lessons=[], current_level="Úvod")
    
    # Získání dokončených lekcí
    completed_lessons = db.query(UserProgress.lesson_id).filter(
        UserProgress.user_id == user.id,
        UserProgress.completed == True
    ).all()
    completed_lesson_ids = [lesson[0] for lesson in completed_lessons]
    
    # Získání achievementů
    achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == user.id
    ).all()
    
    # Výpočet celkových bodů
    total_points = sum(achievement.achievement.points for achievement in achievements)
    
    return StudentProgress(
        name=user.full_name or user.username,
        completed_lessons=completed_lesson_ids,
        current_level="Úvod",  # TODO: Implementovat logiku pro určení úrovně
        total_points=total_points,
        achievements=achievements
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    courses = get_courses_data(db)
    student = get_student_progress(db, current_user)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "courses": courses,
        "student": student,
        "user": current_user
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    courses = get_courses_data(db)
    student = get_student_progress(db, current_user)
    
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student,
            "user": current_user,
            "error": "Kurz nenalezen"
        })
    
    return templates.TemplateResponse("kurz.html", {
        "request": request,
        "course": courses[course_id],
        "course_id": course_id,
        "student": student,
        "user": current_user
    })

@app.get("/lekce/{course_id}/{lesson_id}", response_class=HTMLResponse)
async def lesson_page(request: Request, course_id: str, lesson_id: int, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    courses = get_courses_data(db)
    student = get_student_progress(db, current_user)
    
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student,
            "user": current_user,
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
            "user": current_user,
            "error": "Lekce nenalezena"
        })
    
    return templates.TemplateResponse("lekce.html", {
        "request": request,
        "course": course,
        "course_id": course_id,
        "lesson": lesson,
        "student": student,
        "user": current_user
    })

@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    student = get_student_progress(db, current_user)
    
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.post("/run_code")
async def run_code(code: str = Form(...)):
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
async def profile(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user_optional(request, db)
    if not current_user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    student = get_student_progress(db, current_user)
    
    return templates.TemplateResponse("profil.html", {
        "request": request,
        "student": student,
        "user": current_user
    })

@app.post("/update_progress")
async def update_progress(lesson_id: int = Form(...), db: Session = Depends(get_db), request: Request = None):
    current_user = get_current_user_optional(request, db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Musíte být přihlášeni")
    
    # Kontrola, zda lekce existuje
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lekce nenalezena")
    
    # Kontrola, zda už není dokončena
    existing_progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.lesson_id == lesson_id
    ).first()
    
    if existing_progress:
        if not existing_progress.completed:
            existing_progress.completed = True
            existing_progress.completion_percentage = 100.0
            existing_progress.completed_at = datetime.utcnow()
            db.commit()
    else:
        # Vytvoření nového záznamu o pokroku
        progress = UserProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            completed=True,
            completion_percentage=100.0,
            completed_at=datetime.utcnow()
        )
        db.add(progress)
        db.commit()
    
    # Získání aktualizovaného pokroku
    student = get_student_progress(db, current_user)
    
    return {"success": True, "completed_lessons": student.completed_lessons}

# Autentifikační endpointy
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nesprávné uživatelské jméno nebo heslo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Aktualizace posledního přihlášení
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name
        )
        return {"message": "Uživatel úspěšně vytvořen", "user_id": user.id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/logout")
async def logout():
    return {"message": "Úspěšně odhlášen"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
