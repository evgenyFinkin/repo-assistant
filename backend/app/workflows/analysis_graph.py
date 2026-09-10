"""LangGraph workflow: analyze -> embed -> store -> retrieve -> generate.

Scaffold only. Each node is a stub to be filled in per MVP.md Technical Tasks.
"""
from __future__ import annotations

from app.models.schemas import ChatResponse

# TODO: build actual StateGraph once node implementations exist:
#   clone_repo -> extract_files -> parse_tree_sitter -> chunk_content
#   -> embed_chunks -> store_in_chroma  (Story 2, "analyze" pipeline)
#   retrieve_chunks -> generate_answer  (Story 3/4, "chat" pipeline)


async def run_analysis_pipeline(repo_id: str, url: str) -> None:
    """Clone -> parse -> chunk -> embed -> store. Not yet implemented."""
    raise NotImplementedError("analysis pipeline not yet built")


async def answer_question(repo_id: str, question: str) -> ChatResponse:
    """Retrieve top-5 chunks, prompt LLM with citation instructions, return answer.

    Stub response so the API contract is exercisable before the real
    retrieve/generate nodes exist.
    """
    return ChatResponse(
        answer="Analysis pipeline not yet implemented — this is a scaffold response.",
        sources=[],
    )
