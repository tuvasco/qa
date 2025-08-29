from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.question import QuestionCreate, QuestionRead
from app.crud import question as question_crud
from app.api.deps import get_db_session

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=List[QuestionRead])
async def list_questions(db: AsyncSession = Depends(get_db_session)):
    questions = await question_crud.list_questions(db)
    return questions


@router.post("/", response_model=QuestionRead,
             status_code=status.HTTP_201_CREATED)
async def create_question(payload: QuestionCreate, db: AsyncSession = Depends(get_db_session)):
    q = await question_crud.create_question(db, text=payload.text)
    return q


@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db_session)):
    q = await question_crud.get_question_with_answers(db, question_id)
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found")
    return q


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db: AsyncSession = Depends(get_db_session)):
    q = await question_crud.get_question(db, question_id)
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Question not found")
    await question_crud.delete_question(db, q)
    return
