"""Pydantic request/response models.

Covers Story 1 (repo URL intake), Story 3/4 (chat + source-grounded answers).
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    CLONING = "cloning"
    PARSING = "parsing"
    EMBEDDING = "embedding"
    READY = "ready"
    FAILED = "failed"


class RepositoryCreateRequest(BaseModel):
    url: str = Field(..., description="Public GitHub HTTPS URL, e.g. https://github.com/owner/repo")


class RepositoryCreateResponse(BaseModel):
    id: str
    status: AnalysisStatus


class RepositoryStatusResponse(BaseModel):
    id: str
    status: AnalysisStatus
    error: str | None = None
    files_indexed: int | None = None


class ChatRequest(BaseModel):
    question: str


class SourceReference(BaseModel):
    file_path: str
    line_start: int
    line_end: int
    snippet: str
    similarity: float


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)
