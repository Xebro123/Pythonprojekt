from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import ast
import io
import sys

router = APIRouter()

class PythonCode(BaseModel):
    code: str

class LessonProgress(BaseModel):
    course: str
    lesson: int
    completed: bool

@router.post("/api/run-python")
async def run_python(data: PythonCode):
    """
    Execute Python turtle code and return drawing commands
    """
    try:
        # Parse code to extract turtle commands
        commands = []
        tree = ast.parse(data.code)
        
        # Simple turtle command extraction
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'forward' and node.args:
                        distance = ast.literal_eval(node.args[0])
                        commands.append({'type': 'forward', 'distance': distance})
                    elif node.func.attr == 'right' and node.args:
                        degrees = ast.literal_eval(node.args[0])
                        commands.append({'type': 'right', 'degrees': degrees})
                    elif node.func.attr == 'left' and node.args:
                        degrees = ast.literal_eval(node.args[0])
                        commands.append({'type': 'left', 'degrees': degrees})
        
        return {
            'success': True,
            'commands': commands
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@router.post("/api/complete-lesson")
async def complete_lesson(progress: LessonProgress):
    """
    Save lesson completion progress to database
    """
    # TODO: Save to Directus/PostgreSQL
    # For now, just return success
    return {'success': True}

