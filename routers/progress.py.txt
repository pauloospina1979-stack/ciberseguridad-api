from fastapi import APIRouter, Depends
from sqlalchemy import insert
from db import get_db
from models import Progress
from deps import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])

@router.post("/complete/{lesson_id}")
def complete_lesson(lesson_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    db.execute(
        insert(Progress)
        .values(user_id=user["sub"], lesson_id=lesson_id, completed=True)
        .on_conflict_do_update(
            index_elements=[Progress.user_id, Progress.lesson_id],
            set_={"completed": True}
        )
    )
    db.commit()
    return {"status": "ok"}
