from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Answer


async def create_answer(db: AsyncSession, question_id: int, user_id: str, text: str) -> Answer:
    answer = Answer(question_id=question_id, user_id=user_id, text=text)
    db.add(answer)
    await db.commit()
    await db.refresh(answer)

    return answer


async def get_answer(db: AsyncSession, answer_id: int) -> Optional[Answer]:
    result = await db.execute(select(Answer).where(Answer.id == answer_id))
    return result.scalars().first()


async def delete_answer(db: AsyncSession, answer: Answer) -> None:
    await db.delete(answer)
    await db.commit()
