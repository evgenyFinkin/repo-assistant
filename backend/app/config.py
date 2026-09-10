"""App configuration, loaded from environment variables.

See .env.example at repo root for the full list of variables.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API
    app_name: str = "repo-assistant"
    api_prefix: str = "/api"

    # Openrouter (embeddings + LLM generation)
    openrouter_api_key: str = ""
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    embedding_model: str = "ling-3.0-flash-fin:free"

    # Chroma vector store
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_prefix: str = "repo"

    # Repo analysis limits (Story 5: Error Handling & Limits)
    analysis_timeout_seconds: int = 60
    max_repo_files: int = 100_000
    clone_dir: str = "./data/repos"

    # Chunking (see MVP-context.md: Open Questions -> chunking strategy)
    chunk_min_tokens: int = 1000
    chunk_max_tokens: int = 2000
    chunk_overlap_tokens: int = 200

    # Languages supported via Tree-sitter
    supported_languages: tuple[str, ...] = ("javascript", "python", "typescript", "go")


@lru_cache
def get_settings() -> Settings:
    return Settings()
