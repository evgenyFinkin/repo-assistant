"""Repo intake + status tracking (Story 1, Story 2).

Scaffold only: in-memory store, no real cloning/parsing yet.
Excludes on clone: node_modules, .git, build artifacts (per Story 2 criteria).
"""
from __future__ import annotations

import re
import uuid

from app.models.schemas import AnalysisStatus, RepositoryStatusResponse

_GITHUB_URL_RE = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+/?$")

EXCLUDED_PATHS = ("node_modules", ".git", "dist", "build", "__pycache__")

# TODO: replace with real job store (DB / redis) — this is process-local and
# will not survive restarts or scale beyond a single worker.
_JOBS: dict[str, RepositoryStatusResponse] = {}


class InvalidRepositoryError(ValueError):
    """Raised for malformed URLs or inaccessible/private repos."""


def start_analysis(url: str) -> str:
    if not _GITHUB_URL_RE.match(url):
        raise InvalidRepositoryError(f"not a valid public GitHub repo URL: {url}")

    repo_id = str(uuid.uuid4())
    _JOBS[repo_id] = RepositoryStatusResponse(id=repo_id, status=AnalysisStatus.PENDING)

    # TODO: enqueue LangGraph workflow (clone -> parse -> embed -> store),
    # run inside the isolated Docker analysis container (Story 2), enforce
    # analysis_timeout_seconds (Story 5).

    return repo_id


def get_status(repo_id: str) -> RepositoryStatusResponse | None:
    return _JOBS.get(repo_id)
