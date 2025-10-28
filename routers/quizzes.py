from fastapi import APIRouter, Depends
from sqlalchemy import select
from db import get_db
from models import Quiz, Question, Option

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/{lesson_id}")
def get_quiz_by_lesson(lesson_id: int, db=Depends(get_db)):
    quiz = db.execute(select(Quiz).where(Quiz.lesson_id==lesson_id)).scalar_one()
    questions = db.execute(select(Question).where(Question.quiz_id==quiz.id)).scalars().all()
    opts = {q.id: db.execute(select(Option).where(Option.question_id==q.id)).scalars().all() for q in questions}
    return {
        "quiz": {"id": quiz.id, "title": quiz.title},
        "questions": [
            {"id": q.id, "prompt": q.prompt, "type": q.type, "options": [{"id": o.id, "text": o.text} for o in opts[q.id]]}
            for q in questions
        ]
    }
