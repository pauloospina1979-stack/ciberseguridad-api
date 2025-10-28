from pydantic import BaseModel
from typing import List, Optional

class ModuleOut(BaseModel):
    id: int
    slug: str | None
    title: str | None
    description: str | None
    level: str | None
    published: bool
    class Config:
        from_attributes = True

class LessonOut(BaseModel):
    id: int
    module_id: int
    title: str
    content_md: str | None
    order_idx: int
    class Config:
        from_attributes = True

class StartAttemptOut(BaseModel):
    attempt_id: int

class SubmitAnswer(BaseModel):
    question_id: int
    option_ids: list[int]

class FinishAttemptIn(BaseModel):
    answers: list[SubmitAnswer]

class ScoreOut(BaseModel):
    score: float
