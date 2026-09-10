"""Repository intake + analysis status endpoints (Story 1, Story 2)."""
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
    """Accept a GitHub URL and kick off clone + analysis.

    TODO: validate URL format + public accessibility (Story 1 acceptance criteria).
    TODO: trigger LangGraph analysis workflow as a background job (Story 2).
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
