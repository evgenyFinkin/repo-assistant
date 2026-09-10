"""Tests for GitHub API client."""
import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.github_api import (
    GitHubAPIClient,
    GitHubAPIError,
    GitHubRepositoryNotFoundError,
    GitHubRateLimitError,
    GitHubConnectionError,
)


def _mock_response(status_code: int, json_data=None, text: str = "") -> AsyncMock:
    """Build a mock httpx.Response. `.json()` is sync in httpx, so it must be
    a plain MagicMock, not AsyncMock (which would return an unawaited coroutine)."""
    resp = AsyncMock()
    resp.status_code = status_code
    resp.text = text
    resp.json = MagicMock(return_value=json_data)
    return resp


@pytest.mark.asyncio
async def test_fetch_repo_metadata_success():
    """Test successful repo metadata fetch."""
    client = GitHubAPIClient()

    mock_response = {
        "name": "awesome-project",
        "description": "An awesome project",
        "html_url": "https://github.com/owner/awesome-project",
        "language": "Python",
        "stargazers_count": 1234,
        "forks_count": 56,
        "topics": ["python", "ai", "github"],
        "fork": False,
        "private": False,
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(200, json_data=mock_response)
        result = await client.fetch_repo_metadata("owner", "awesome-project")

    assert result["name"] == "awesome-project"
    assert result["language"] == "Python"
    assert result["stars"] == 1234
    assert result["is_private"] is False


@pytest.mark.asyncio
async def test_fetch_repo_metadata_not_found():
    """Test repo not found (404) error."""
    client = GitHubAPIClient()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(404, text="Not Found")

        with pytest.raises(GitHubRepositoryNotFoundError) as exc_info:
            await client.fetch_repo_metadata("owner", "nonexistent")

    assert "not found" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_fetch_repo_metadata_rate_limited():
    """Test rate limit error (403)."""
    client = GitHubAPIClient()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(403, text="API rate limit exceeded")

        with pytest.raises(GitHubRateLimitError):
            await client.fetch_repo_metadata("owner", "repo")


@pytest.mark.asyncio
async def test_fetch_repo_metadata_connection_error():
    """Test connection error."""
    client = GitHubAPIClient()

    with patch("httpx.AsyncClient.get", side_effect=httpx.RequestError("Connection failed")):
        with pytest.raises(GitHubConnectionError):
            await client.fetch_repo_metadata("owner", "repo")


@pytest.mark.asyncio
async def test_fetch_repo_readme_success():
    """Test successful README fetch."""
    client = GitHubAPIClient()
    readme_content = "# Awesome Project\n\nThis is a great project."

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(200, text=readme_content)
        result = await client.fetch_repo_readme("owner", "repo")

    assert result == readme_content


@pytest.mark.asyncio
async def test_fetch_repo_readme_not_found():
    """Test README not found (returns None, not error)."""
    client = GitHubAPIClient()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(404)
        result = await client.fetch_repo_readme("owner", "repo")

    assert result is None


@pytest.mark.asyncio
async def test_fetch_file_tree_success():
    """Test successful file tree fetch."""
    client = GitHubAPIClient()

    mock_tree = {
        "tree": [
            {"path": "README.md", "type": "blob", "size": 1024, "sha": "abc123"},
            {"path": "src", "type": "tree", "sha": "def456"},
            {"path": "src/main.py", "type": "blob", "size": 2048, "sha": "ghi789"},
            {
                "path": "node_modules",
                "type": "tree",
                "sha": "excluded",
            },  # Should be filtered
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(200, json_data=mock_tree)
        result = await client.fetch_file_tree("owner", "repo")

    # node_modules should be filtered out
    assert len(result) == 3
    assert all("node_modules" not in entry.get("path", "") for entry in result)


@pytest.mark.asyncio
async def test_fetch_file_tree_not_found():
    """Test file tree fetch with invalid ref."""
    client = GitHubAPIClient()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value = _mock_response(404, text="Not Found")

        with pytest.raises(GitHubRepositoryNotFoundError):
            await client.fetch_file_tree("owner", "repo", ref="nonexistent-branch")


def test_client_with_token():
    """Test client initialization with GitHub token."""
    client = GitHubAPIClient(token="ghp_test123")
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "token ghp_test123"


def test_client_without_token():
    """Test client initialization without token (public rate limit)."""
    client = GitHubAPIClient()
    assert "Authorization" not in client.headers
