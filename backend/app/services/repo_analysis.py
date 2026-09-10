"""Repo intake + status tracking (Story 1, Story 2).

Fetches repo data from GitHub API (no cloning). URL validation + API error handling.
Stores repo metadata and file tree for downstream analysis.
"""
from __future__ import annotations

import asyncio
import re
import uuid
from typing import Any

from app.models.schemas import AnalysisStatus, RepositoryStatusResponse
from app.services.github_api import (
    GitHubAPIClient,
    GitHubAPIError,
    GitHubConnectionError,
    GitHubRepositoryNotFoundError,
    GitHubRateLimitError,
)

_GITHUB_URL_RE = re.compile(r"^https://github\.com/([\w.-]+)/([\w.-]+)/?$")

# TODO: replace with real job store (DB / redis) — this is process-local and
# will not survive restarts or scale beyond a single worker.
_JOBS: dict[str, RepositoryStatusResponse] = {}
_REPO_DATA: dict[str, dict[str, Any]] = {}


class InvalidRepositoryError(ValueError):
    """Raised for malformed URLs or inaccessible/private repos."""


def _parse_github_url(url: str) -> tuple[str, str] | None:
    """Extract owner and repo from GitHub URL.

    Args:
        url: GitHub URL (e.g., https://github.com/owner/repo)

    Returns:
        (owner, repo) tuple or None if URL is invalid
    """
    match = _GITHUB_URL_RE.match(url)
    if match:
        return match.group(1), match.group(2)
    return None


def start_analysis(url: str) -> str:
    """Start repository analysis.

    Args:
        url: GitHub repository URL

    Returns:
        Job ID for tracking status

    Raises:
        InvalidRepositoryError: If URL is invalid or repo not accessible
    """
    parsed = _parse_github_url(url)
    if not parsed:
        raise InvalidRepositoryError(
            f"Invalid GitHub URL format. Expected: https://github.com/owner/repo"
        )

    owner, repo = parsed
    repo_id = str(uuid.uuid4())
    _JOBS[repo_id] = RepositoryStatusResponse(id=repo_id, status=AnalysisStatus.PENDING)

    # Start async task to fetch repo data in background
    asyncio.create_task(_fetch_repo_data(repo_id, owner, repo, url))

    return repo_id


async def _fetch_repo_data(repo_id: str, owner: str, repo: str, url: str) -> None:
    """Fetch repository data from GitHub API.

    Runs in background. Updates job status as it progresses.

    Args:
        repo_id: Job ID
        owner: Repository owner
        repo: Repository name
        url: Original GitHub URL
    """
    client = GitHubAPIClient()

    try:
        # Fetch repo metadata
        _JOBS[repo_id].status = AnalysisStatus.CLONING
        metadata = await client.fetch_repo_metadata(owner, repo)

        # Fetch README
        readme = await client.fetch_repo_readme(owner, repo)

        # Fetch file tree
        _JOBS[repo_id].status = AnalysisStatus.PARSING
        file_tree = await client.fetch_file_tree(owner, repo)

        # Store repo data
        _REPO_DATA[repo_id] = {
            "url": url,
            "owner": owner,
            "repo": repo,
            "metadata": metadata,
            "readme": readme,
            "file_tree": file_tree,
            "file_count": len(file_tree),
        }

        # Mark as ready for embedding
        _JOBS[repo_id].status = AnalysisStatus.READY
        _JOBS[repo_id].files_indexed = len(file_tree)

    except GitHubRepositoryNotFoundError as exc:
        _JOBS[repo_id].status = AnalysisStatus.FAILED
        _JOBS[repo_id].error = str(exc)
    except GitHubRateLimitError as exc:
        _JOBS[repo_id].status = AnalysisStatus.FAILED
        _JOBS[repo_id].error = str(exc)
    except GitHubConnectionError as exc:
        _JOBS[repo_id].status = AnalysisStatus.FAILED
        _JOBS[repo_id].error = f"Connection error: {exc}"
    except GitHubAPIError as exc:
        _JOBS[repo_id].status = AnalysisStatus.FAILED
        _JOBS[repo_id].error = f"GitHub API error: {exc}"
    except Exception as exc:
        # Catch-all for unexpected errors
        _JOBS[repo_id].status = AnalysisStatus.FAILED
        _JOBS[repo_id].error = f"Unexpected error: {exc}"


def get_status(repo_id: str) -> RepositoryStatusResponse | None:
    """Get repository analysis status.

    Args:
        repo_id: Job ID

    Returns:
        Status response or None if job not found
    """
    return _JOBS.get(repo_id)


def get_repo_data(repo_id: str) -> dict[str, Any] | None:
    """Get repository data (metadata, file tree, etc).

    Args:
        repo_id: Job ID

    Returns:
        Repository data dict or None if not found
    """
    return _REPO_DATA.get(repo_id)
