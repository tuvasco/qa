from datetime import datetime
from typing import List
from pydantic import BaseModel, constr
from app.schemas.answer import AnswerRead


class QuestionCreate(BaseModel):
    text: constr(strip_whitespace=True, min_length=1, max_length=2000)


class QuestionRead(BaseModel):
    id: int
    text: str
    created_at: datetime
    answers: List[AnswerRead] = []


class Config:
    orm_mode = True
