from fastapi import FastAPI
from app.api.routers import questions as questions_router
from app.api.routers import answers as answers_router
from app.core.config import settings

app = FastAPI(title="QA API", version="1.0")
app.include_router(questions_router.router)
app.include_router(answers_router.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
