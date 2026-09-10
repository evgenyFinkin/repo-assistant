"""Chroma vector store wrapper — one collection per analyzed repo."""
from __future__ import annotations

from functools import lru_cache
from typing import Any

import chromadb

from app.config import get_settings


@lru_cache
def get_client() -> chromadb.ClientAPI:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)


def get_collection(repo_id: str) -> Any:
    settings = get_settings()
    client = get_client()
    name = f"{settings.chroma_collection_prefix}_{repo_id}"
    return client.get_or_create_collection(name=name)


def upsert_chunks(
    repo_id: str,
    ids: list[str],
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict[str, Any]],
) -> None:
    collection = get_collection(repo_id)
    collection.upsert(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)


def query(repo_id: str, query_embedding: list[float], top_k: int = 5) -> Any:
    """Retrieve top-k relevant chunks (Story 4 acceptance criteria)."""
    collection = get_collection(repo_id)
    return collection.query(query_embeddings=[query_embedding], n_results=top_k)
