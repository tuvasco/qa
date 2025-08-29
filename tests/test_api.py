import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db.session import Base, get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture
async def async_client():
    engine = create_async_engine(DATABASE_URL, future=True)

    AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_db():
        async with AsyncSessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_question_and_answer_and_cascade(async_client: AsyncClient):

    resp = await async_client.post("/questions/", json={"text": "Как дела?"})
    assert resp.status_code == 201
    question = resp.json()
    qid = question["id"] if isinstance(question, list) else question["id"]

    user_uuid = "00000000-0000-0000-0000-000000000001"
    resp = await async_client.post(f"/questions/{qid}/answers/",
                                   json={"user_id": user_uuid, "text": "Хорошо"})
    assert resp.status_code == 201
    answer = resp.json()
    aid = answer["id"]

    resp = await async_client.delete(f"/questions/{qid}")
    assert resp.status_code == 204

    resp = await async_client.get(f"/answers/{aid}")
    assert resp.status_code == 404
