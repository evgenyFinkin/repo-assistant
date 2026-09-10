"""GitHub API client for fetching repository metadata and file tree without cloning."""
from __future__ import annotations

import httpx
from typing import Any


class GitHubAPIError(Exception):
    """Base exception for GitHub API errors."""


class GitHubRepositoryNotFoundError(GitHubAPIError):
    """Repository not found (404)."""


class GitHubRateLimitError(GitHubAPIError):
    """GitHub API rate limit exceeded."""


class GitHubConnectionError(GitHubAPIError):
    """Failed to connect to GitHub API."""


class GitHubAPIClient:
    """Fetch repository data from GitHub REST API."""

    BASE_URL = "https://api.github.com"
    TIMEOUT = 10.0

    def __init__(self, token: str | None = None):
        """Initialize GitHub API client.

        Args:
            token: Optional GitHub personal access token. Without it, limited to 60 req/hour.
        """
        self.token = token
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            self.headers["Authorization"] = f"token {token}"

    async def fetch_repo_metadata(self, owner: str, repo: str) -> dict[str, Any]:
        """Fetch repository metadata (name, description, language, etc).

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            Dictionary with repo metadata

        Raises:
            GitHubRepositoryNotFoundError: If repo not found (404)
            GitHubRateLimitError: If rate limited
            GitHubConnectionError: If connection fails
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"

        async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
            try:
                response = await client.get(url, headers=self.headers)
            except httpx.RequestError as exc:
                raise GitHubConnectionError(
                    f"Failed to connect to GitHub API: {exc}"
                ) from exc

        if response.status_code == 404:
            raise GitHubRepositoryNotFoundError(
                f"Repository '{owner}/{repo}' not found. Check URL and ensure it's public."
            )
        elif response.status_code == 403:
            # 403 can mean rate limit or permission denied
            if "API rate limit exceeded" in response.text:
                raise GitHubRateLimitError(
                    "GitHub API rate limit exceeded. Try again later."
                )
            raise GitHubAPIError(f"Access denied: {response.text}")
        elif response.status_code >= 400:
            raise GitHubAPIError(f"GitHub API error: {response.status_code} {response.text}")

        data = response.json()
        return {
            "name": data.get("name"),
            "description": data.get("description"),
            "url": data.get("html_url"),
            "language": data.get("language"),
            "stars": data.get("stargazers_count"),
            "forks": data.get("forks_count"),
            "topics": data.get("topics", []),
            "is_fork": data.get("fork"),
            "is_private": data.get("private"),
        }

    async def fetch_repo_readme(self, owner: str, repo: str) -> str | None:
        """Fetch repository README content.

        Args:
            owner: Repository owner
            repo: Repository name

        Returns:
            README content as string, or None if not found

        Raises:
            GitHubConnectionError: If connection fails
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/readme"

        async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
            try:
                response = await client.get(
                    url,
                    headers={**self.headers, "Accept": "application/vnd.github.v3.raw"},
                )
            except httpx.RequestError as exc:
                raise GitHubConnectionError(
                    f"Failed to connect to GitHub API: {exc}"
                ) from exc

        if response.status_code == 404:
            # README not found, return None (not an error)
            return None
        elif response.status_code >= 400:
            raise GitHubAPIError(f"GitHub API error: {response.status_code}")

        return response.text

    async def fetch_file_tree(
        self, owner: str, repo: str, ref: str = "HEAD", recursive: bool = True
    ) -> list[dict[str, Any]]:
        """Fetch repository file tree.

        Args:
            owner: Repository owner
            repo: Repository name
            ref: Git ref (branch, tag, commit SHA). Defaults to HEAD.
            recursive: If True, fetch full tree. If False, just top level.

        Returns:
            List of file entries with path, type (blob/tree), size, etc.

        Raises:
            GitHubRepositoryNotFoundError: If repo not found
            GitHubConnectionError: If connection fails
            GitHubAPIError: On other API errors
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{ref}"
        params = {}
        if recursive:
            params["recursive"] = "1"

        async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
            try:
                response = await client.get(url, headers=self.headers, params=params)
            except httpx.RequestError as exc:
                raise GitHubConnectionError(
                    f"Failed to connect to GitHub API: {exc}"
                ) from exc

        if response.status_code == 404:
            raise GitHubRepositoryNotFoundError(
                f"Could not find repository or git ref '{ref}'"
            )
        elif response.status_code >= 400:
            raise GitHubAPIError(f"GitHub API error: {response.status_code}")

        data = response.json()
        tree = data.get("tree", [])

        # Filter out common excluded paths
        excluded = {"node_modules", ".git", "dist", "build", "__pycache__"}
        filtered_tree = [
            entry
            for entry in tree
            if not any(excl in entry.get("path", "") for excl in excluded)
        ]

        return filtered_tree
