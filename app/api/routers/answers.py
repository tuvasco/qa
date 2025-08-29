from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.answer import AnswerCreate, AnswerRead
from app.crud import answer as answer_crud
from app.crud import question as question_crud
from app.api.deps import get_db_session

router = APIRouter(tags=["answers"])

@router.post("/questions/{question_id}/answers/", response_model=AnswerRead,
             status_code=status.HTTP_201_CREATED)
async def create_answer(question_id: int, payload: AnswerCreate, db: AsyncSession = Depends(get_db_session)):
    q = await question_crud.get_question(db, question_id)
    if q is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Question not found")
    user_id_str = str(payload.user_id)
    ans = await answer_crud.create_answer(db, question_id=question_id,
                                          user_id=user_id_str, text=payload.text)
    return ans


@router.get("/answers/{answer_id}", response_model=AnswerRead)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_db_session)):
    ans = await answer_crud.get_answer(db, answer_id)
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Answer not found")
    return ans


@router.delete("/answers/{answer_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db: AsyncSession = Depends(get_db_session)):
    ans = await answer_crud.get_answer(db, answer_id)
    if ans is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Answer not found")

    await answer_crud.delete_answer(db, ans)
    return
