"""Embedding generation via Openrouter (ling-3.0-flash-fin:free).

See MVP-context.md Stack Choices -> Embeddings.
"""
from __future__ import annotations

import httpx

from app.config import get_settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of text chunks.

    TODO: batch requests, respect Openrouter rate limits (Story 5 - queue
    requests), retry with backoff.
    """
    settings = get_settings()
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    async with httpx.AsyncClient(base_url=settings.openrouter_base_url, timeout=30) as client:
        resp = await client.post(
            "/embeddings",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json={"model": settings.embedding_model, "input": texts},
        )
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in data["data"]]
