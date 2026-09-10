"""Repository intake + analysis status endpoints (Story 1, Story 2).

Story 1: Accept GitHub URL, validate format, fetch repo data from GitHub API.
Story 2: Background job to analyze repo (triggered on /repositories POST).
"""
from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    AnalysisStatus,
    RepositoryCreateRequest,
    RepositoryCreateResponse,
    RepositoryStatusResponse,
)
from app.services import repo_analysis

router = APIRouter()


@router.post("/repositories", response_model=RepositoryCreateResponse)
async def create_repository(payload: RepositoryCreateRequest) -> RepositoryCreateResponse:
    """Accept a GitHub URL and start background analysis.

    Validates URL format, fetches repo metadata from GitHub API without cloning,
    and returns a job ID for polling analysis status.

    Args:
        payload: Request containing GitHub repo URL

    Returns:
        Job ID and initial PENDING status

    Raises:
        HTTPException 400: Invalid URL format
    """
    try:
        repo_id = repo_analysis.start_analysis(payload.url)
    except repo_analysis.InvalidRepositoryError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RepositoryCreateResponse(id=repo_id, status=AnalysisStatus.PENDING)


@router.get("/repositories/{repo_id}/status", response_model=RepositoryStatusResponse)
async def get_repository_status(repo_id: str) -> RepositoryStatusResponse:
    """Poll analysis status. TODO: back with real job state (Story 1 loading state)."""
    status = repo_analysis.get_status(repo_id)
    if status is None:
        raise HTTPException(status_code=404, detail="repository not found")
    return status
