"""Chat endpoint: question in, source-grounded answer out (Story 3, Story 4)."""
from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services import repo_analysis
from app.workflows.analysis_graph import answer_question

router = APIRouter()


@router.post("/chat/{repo_id}", response_model=ChatResponse)
async def chat(repo_id: str, payload: ChatRequest) -> ChatResponse:
    """Retrieve top-k chunks for the repo and generate a cited answer.

    TODO: wire to LangGraph retrieve -> generate nodes (Story 4).
    TODO: rate limit / queue Openrouter calls (Story 5).
    """
    if repo_analysis.get_status(repo_id) is None:
        raise HTTPException(status_code=404, detail="repository not found")

    return await answer_question(repo_id=repo_id, question=payload.question)
