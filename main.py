from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import subprocess
import tempfile
import os

app = FastAPI(title="Python Kurz pro Základní Školy", description="Výuková platforma pro Python")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Data model for student progress
class StudentProgress(BaseModel):
    name: str
    completed_lessons: list = []
    current_level: str = "Úvod"

# Sample data
courses = {
    "uvod": {
        "title": "Úvod do Pythonu",
        "description": "Seznamte se se základy programování v Pythonu",
        "lessons": [
            {"id": 1, "title": "Co je Python?", "description": "Úvod do programování"},
            {"id": 2, "title": "Instalace Pythonu", "description": "Jak nainstalovat Python"},
            {"id": 3, "title": "První program", "description": "Hello World!"},
        ]
    },
    "zaklady": {
        "title": "Základy Pythonu",
        "description": "Naučte se základní koncepty programování",
        "lessons": [
            {"id": 4, "title": "Proměnné", "description": "Ukládání dat"},
            {"id": 5, "title": "Čísla a text", "description": "Datové typy"},
            {"id": 6, "title": "Podmínky", "description": "if, elif, else"},
            {"id": 7, "title": "Cykly", "description": "for a while"},
        ]
    },
    "pokrocile": {
        "title": "Pokročilé koncepty",
        "description": "Složitější témata pro pokročilé studenty",
        "lessons": [
            {"id": 8, "title": "Funkce", "description": "Vytváření vlastních funkcí"},
            {"id": 9, "title": "Seznamy", "description": "Práce s daty"},
            {"id": 10, "title": "Soubory", "description": "Čtení a zápis do souborů"},
        ]
    }
}

# Global student progress (in real app, this would be in database)
student_progress = StudentProgress(name="Student", completed_lessons=[], current_level="Úvod")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "courses": courses,
        "student": student_progress
    })

@app.get("/kurz/{course_id}", response_class=HTMLResponse)
async def course_page(request: Request, course_id: str):
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student_progress,
            "error": "Kurz nenalezen"
        })
    
    return templates.TemplateResponse("kurz.html", {
        "request": request,
        "course": courses[course_id],
        "course_id": course_id,
        "student": student_progress
    })

@app.get("/lekce/{course_id}/{lesson_id}", response_class=HTMLResponse)
async def lesson_page(request: Request, course_id: str, lesson_id: int):
    if course_id not in courses:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "courses": courses,
            "student": student_progress,
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
            "student": student_progress,
            "error": "Lekce nenalezena"
        })
    
    return templates.TemplateResponse("lekce.html", {
        "request": request,
        "course": course,
        "course_id": course_id,
        "lesson": lesson,
        "student": student_progress
    })

@app.get("/playground", response_class=HTMLResponse)
async def playground(request: Request):
    return templates.TemplateResponse("playground.html", {
        "request": request,
        "student": student_progress
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
async def profile(request: Request):
    return templates.TemplateResponse("profil.html", {
        "request": request,
        "student": student_progress
    })

@app.post("/update_progress")
async def update_progress(lesson_id: int = Form(...)):
    if lesson_id not in student_progress.completed_lessons:
        student_progress.completed_lessons.append(lesson_id)
    
    return {"success": True, "completed_lessons": student_progress.completed_lessons}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
