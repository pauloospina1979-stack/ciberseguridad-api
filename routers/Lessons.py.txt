from fastapi import APIRouter, Depends
from sqlalchemy import select
from db import get_db
from models import Lesson
from schemas import LessonOut

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.get("/{lesson_id}", response_model=LessonOut)
def get_lesson(lesson_id: int, db=Depends(get_db)):
    return db.execute(select(Lesson).where(Lesson.id==lesson_id)).scalar_one()
