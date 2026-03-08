from fastapi import FastAPI, APIRouter
from settings import Settings

router = APIRouter(prefix="/ping", tags=["ping"])

@router.get("/db")
async def ping_db():
    settings = Settings()
    settings.GOOGLE_TOKEN_ID
    return {"message": settings.GOOGLE_TOKEN_ID}

@router.get("/app")
async def ping_app():
    return {"text": "app is working"}