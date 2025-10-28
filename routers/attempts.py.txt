from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from db import get_db
from models import Attempt, Answer, Question, Option
from schemas import StartAttemptOut, FinishAttemptIn, ScoreOut
from deps import get_current_user

router = APIRouter(prefix="/attempts", tags=["attempts"])

@router.post("/{quiz_id}/start", response_model=StartAttemptOut)
def start_attempt(quiz_id: int, db=Depends(get_db), user=Depends(get_current_user)):
    a = Attempt(quiz_id=quiz_id, user_id=user["sub"])
    db.add(a); db.commit(); db.refresh(a)
    return {"attempt_id": a.id}

@router.post("/{attempt_id}/finish", response_model=ScoreOut)
def finish_attempt(attempt_id: int, payload: FinishAttemptIn, db=Depends(get_db), user=Depends(get_current_user)):
    a = db.get(Attempt, attempt_id)
    if not a or str(a.user_id) != user["sub"]:
        raise HTTPException(404, detail="Attempt not found")
    correct = 0; total = 0
    for sa in payload.answers:
        q = db.get(Question, sa.question_id)
        if not q: continue
        total += 1
        for oid in sa.answers if hasattr(sa, 'answers') else sa.option_ids:
            db.add(Answer(attempt_id=a.id, question_id=q.id, option_id=oid))
        correct_options = {o.id for o in db.execute(select(Option).where(Option.question_id==q.id, Option.is_correct==True)).scalars().all()}
        if set(sa.option_ids) == correct_options:
            correct += 1
    a.score = round(100 * correct / max(total,1), 2)
    db.commit()
    return {"score": float(a.score or 0)}
