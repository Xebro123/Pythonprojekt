from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# SQLite databáze
DATABASE_URL = "sqlite:///./python_kurz.db"

# Vytvoření engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Potřebné pro SQLite
)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class pro modely
Base = declarative_base()

# Databázové modely
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Vztahy
    progress_records = relationship("UserProgress", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    level = Column(String(50))  # "uvod", "zaklady", "pokrocile"
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Vztahy
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content = Column(Text)  # HTML obsah lekce
    code_example = Column(Text)  # Příklad kódu
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Vztahy
    course = relationship("Course", back_populates="lessons")
    progress_records = relationship("UserProgress", back_populates="lesson")

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    completion_percentage = Column(Float, default=0.0)
    time_spent = Column(Integer, default=0)  # v sekundách
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Vztahy
    user = relationship("User", back_populates="progress_records")
    lesson = relationship("Lesson", back_populates="progress_records")

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    icon = Column(String(100))  # FontAwesome ikona
    points = Column(Integer, default=0)
    condition_type = Column(String(50))  # "lessons_completed", "time_spent", "perfect_score"
    condition_value = Column(Integer)  # Hodnota pro splnění
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Vztahy
    user_achievements = relationship("UserAchievement", back_populates="achievement")

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Vztahy
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")

# Dependency pro získání databázové session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Vytvoření tabulek
def create_tables():
    Base.metadata.create_all(bind=engine)

# Inicializace databáze s výchozími daty
def init_database():
    create_tables()
    
    db = SessionLocal()
    try:
        # Kontrola, zda už existují kurzy
        if db.query(Course).count() == 0:
            # Vytvoření výchozích kurzů
            courses_data = [
                {
                    "course_id": "uvod",
                    "title": "Úvod do Pythonu",
                    "description": "Seznamte se se základy programování v Pythonu",
                    "level": "uvod",
                    "order_index": 1
                },
                {
                    "course_id": "zaklady", 
                    "title": "Základy Pythonu",
                    "description": "Naučte se základní koncepty programování",
                    "level": "zaklady",
                    "order_index": 2
                },
                {
                    "course_id": "pokrocile",
                    "title": "Pokročilé koncepty", 
                    "description": "Složitější témata pro pokročilé studenty",
                    "level": "pokrocile",
                    "order_index": 3
                }
            ]
            
            for course_data in courses_data:
                course = Course(**course_data)
                db.add(course)
            
            # Vytvoření výchozích lekcí
            lessons_data = [
                # Úvod do Pythonu
                {"course_id": 1, "lesson_number": 1, "title": "Co je Python?", "description": "Úvod do programování"},
                {"course_id": 1, "lesson_number": 2, "title": "Instalace Pythonu", "description": "Jak nainstalovat Python"},
                {"course_id": 1, "lesson_number": 3, "title": "První program", "description": "Hello World!"},
                
                # Základy Pythonu
                {"course_id": 2, "lesson_number": 4, "title": "Proměnné", "description": "Ukládání dat"},
                {"course_id": 2, "lesson_number": 5, "title": "Čísla a text", "description": "Datové typy"},
                {"course_id": 2, "lesson_number": 6, "title": "Podmínky", "description": "if, elif, else"},
                {"course_id": 2, "lesson_number": 7, "title": "Cykly", "description": "for a while"},
                
                # Pokročilé koncepty
                {"course_id": 3, "lesson_number": 8, "title": "Funkce", "description": "Vytváření vlastních funkcí"},
                {"course_id": 3, "lesson_number": 9, "title": "Seznamy", "description": "Práce s daty"},
                {"course_id": 3, "lesson_number": 10, "title": "Soubory", "description": "Čtení a zápis do souborů"},
            ]
            
            for lesson_data in lessons_data:
                lesson = Lesson(**lesson_data)
                db.add(lesson)
            
            # Vytvoření výchozích achievementů
            achievements_data = [
                {"name": "První kroky", "description": "Dokončete svou první lekci", "icon": "fas fa-baby", "points": 10, "condition_type": "lessons_completed", "condition_value": 1},
                {"name": "Základy zvládnuty", "description": "Dokončete všechny lekce ze základů", "icon": "fas fa-graduation-cap", "points": 50, "condition_type": "lessons_completed", "condition_value": 7},
                {"name": "Maratonec", "description": "Strávte 10 hodin učením", "icon": "fas fa-clock", "points": 100, "condition_type": "time_spent", "condition_value": 36000},
            ]
            
            for achievement_data in achievements_data:
                achievement = Achievement(**achievement_data)
                db.add(achievement)
            
            db.commit()
            print("Databáze inicializována s výchozími daty")
            
    except Exception as e:
        print(f"Chyba při inicializaci databáze: {e}")
        db.rollback()
    finally:
        db.close()