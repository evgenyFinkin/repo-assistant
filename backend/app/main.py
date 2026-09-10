"""FastAPI application entrypoint.

Run locally:
    python -m uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, repositories
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="Ask natural-language questions about a GitHub repository.",
    version="0.1.0",
)

# MVP: local dev only, tighten before any real deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repositories.router, prefix=settings.api_prefix, tags=["repositories"])
app.include_router(chat.router, prefix=settings.api_prefix, tags=["chat"])


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
