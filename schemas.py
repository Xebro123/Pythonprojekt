from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    nickname: Optional[str] = None  # volitelná přezdívka

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    nickname: Optional[str] = None
    display_name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Course schemas
class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    code_example: Optional[str] = None

class LessonResponse(LessonBase):
    id: int
    lesson_number: int
    order_index: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    course_id: str
    order_index: int
    is_active: bool
    created_at: datetime
    lessons: List[LessonResponse] = []

    class Config:
        from_attributes = True

# Progress schemas
class UserProgressBase(BaseModel):
    lesson_id: int
    completed: bool = False
    completion_percentage: float = 0.0
    time_spent: int = 0

class UserProgressResponse(UserProgressBase):
    id: int
    user_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Achievement schemas
class AchievementBase(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    points: int = 0

class AchievementResponse(AchievementBase):
    id: int
    condition_type: Optional[str] = None
    condition_value: Optional[int] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserAchievementResponse(BaseModel):
    id: int
    user_id: int
    achievement_id: int
    earned_at: datetime
    achievement: AchievementResponse

    class Config:
        from_attributes = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

# Student progress (používá se v šablonách)
class StudentProgress(BaseModel):
    name: str
    completed_lessons: List[int] = []
    current_level: str = "Úvod"
    total_points: int = 0
    achievements: List[UserAchievementResponse] = []

# Lesson progress API
class LessonProgress(BaseModel):
    lesson_id: str
    completed: bool = True
