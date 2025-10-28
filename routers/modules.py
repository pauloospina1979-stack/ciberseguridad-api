from fastapi import APIRouter, Depends
from sqlalchemy import select
from db import get_db
from models import Module, Lesson
from schemas import ModuleOut, LessonOut

router = APIRouter(prefix="/modules", tags=["modules"])

@router.get("/", response_model=list[ModuleOut])
def list_modules(db=Depends(get_db)):
    rows = db.execute(select(Module)).scalars().all()
    return rows

@router.get("/{slug}/lessons", response_model=list[LessonOut])
def list_lessons(slug: str, db=Depends(get_db)):
    mod = db.execute(select(Module).where(Module.slug==slug)).scalar_one()
    lessons = db.execute(select(Lesson).where(Lesson.module_id==mod.id).order_by(Lesson.order_idx)).scalars().all()
    return lessons
