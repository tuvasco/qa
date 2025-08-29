from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Question
from sqlalchemy.orm import selectinload

async def create_question(db: AsyncSession, text: str) -> Question:
    question = Question(text=text)
    db.add(question)
    await db.commit()
    await db.refresh(question)

    return question


async def list_questions(db: AsyncSession) -> List[Question]:
    result = await db.execute(select(Question).order_by(Question.created_at.desc()))
    return result.scalars().all()


async def get_question(db: AsyncSession, question_id: int) -> Optional[Question]:
    result = await db.execute(
        select(Question).where(Question.id == question_id).options()
    )
    return result.scalars().first()


async def get_question_with_answers(db: AsyncSession, question_id: int) -> Optional[Question]:

    result = await db.execute(
        select(Question)
        .where(Question.id == question_id)
        .options(selectinload(Question.answers))
    )
    return result.scalars().first()


async def delete_question(db: AsyncSession, question: Question) -> None:
    await db.delete(question)
    await db.commit()
