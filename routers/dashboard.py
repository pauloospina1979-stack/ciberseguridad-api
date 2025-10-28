from fastapi import APIRouter, Depends
from sqlalchemy import text
from db import get_db
from deps import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/kpis")
def kpis(db=Depends(get_db), user=Depends(get_current_user)):
    q = db.execute(text("""
      select
        (select count(*) from profiles) as users,
        (select count(*) from modules where published=true) as modules,
        (select coalesce(avg(score),0) from attempts) as avg_score,
        (select count(*) from progress where completed=true) as completions
    """)).mappings().first()
    return q
