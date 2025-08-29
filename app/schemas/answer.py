from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, constr


class AnswerCreate(BaseModel):
    user_id: UUID
    text: constr(strip_whitespace=True, min_length=1, max_length=2000)


class AnswerRead(BaseModel):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime


class Config:
    orm_mode = True
