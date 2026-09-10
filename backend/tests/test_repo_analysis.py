"""Tests for repository analysis service."""
import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from app.models.schemas import AnalysisStatus
from app.services import repo_analysis


@pytest.fixture(autouse=True)
def mock_github_client():
    """Prevent real network calls: start_analysis() fires a background
    asyncio task that hits the GitHub API. Patch the client so tests are
    fast, deterministic, and don't depend on network/GitHub availability."""
    with patch("app.services.repo_analysis.GitHubAPIClient") as mock_client_cls:
        instance = mock_client_cls.return_value
        instance.fetch_repo_metadata = AsyncMock(return_value={"name": "repo"})
        instance.fetch_repo_readme = AsyncMock(return_value="# readme")
        instance.fetch_file_tree = AsyncMock(
            return_value=[{"path": "a.py", "type": "blob"}]
        )
        yield mock_client_cls


def test_parse_github_url_valid():
    """Test parsing valid GitHub URLs."""
    # Standard format
    result = repo_analysis._parse_github_url("https://github.com/owner/repo")
    assert result == ("owner", "repo")

    # With trailing slash
    result = repo_analysis._parse_github_url("https://github.com/owner/repo/")
    assert result == ("owner", "repo")

    # With dots and dashes in names
    result = repo_analysis._parse_github_url("https://github.com/my-org/my.repo-name")
    assert result == ("my-org", "my.repo-name")


def test_parse_github_url_invalid():
    """Test parsing invalid GitHub URLs."""
    # Wrong domain
    assert repo_analysis._parse_github_url("https://gitlab.com/owner/repo") is None

    # Wrong protocol
    assert repo_analysis._parse_github_url("http://github.com/owner/repo") is None

    # Missing repo
    assert repo_analysis._parse_github_url("https://github.com/owner") is None

    # Empty string
    assert repo_analysis._parse_github_url("") is None

    # Invalid characters
    assert repo_analysis._parse_github_url("https://github.com/owner/repo name") is None


# NOTE: start_analysis() calls asyncio.create_task() internally, which requires
# a running event loop (it has one in production — FastAPI's async endpoint
# provides it). Tests must call it from inside an async test function.


@pytest.mark.asyncio
async def test_start_analysis_valid_url():
    """Test starting analysis with valid URL."""
    url = "https://github.com/owner/awesome-project"
    repo_id = repo_analysis.start_analysis(url)

    assert repo_id is not None
    assert len(repo_id) > 0

    # Check job was created with PENDING status (background fetch hasn't
    # necessarily run yet — this checks the synchronous part of start_analysis)
    status = repo_analysis.get_status(repo_id)
    assert status is not None
    assert status.id == repo_id
    assert status.status == AnalysisStatus.PENDING

    await asyncio.sleep(0.05)  # let the mocked background fetch finish


def test_start_analysis_invalid_url():
    """Test starting analysis with invalid URL."""
    with pytest.raises(repo_analysis.InvalidRepositoryError) as exc_info:
        repo_analysis.start_analysis("https://gitlab.com/owner/repo")

    assert "invalid" in str(exc_info.value).lower()


def test_start_analysis_malformed_url():
    """Test starting analysis with malformed URL."""
    with pytest.raises(repo_analysis.InvalidRepositoryError):
        repo_analysis.start_analysis("not-a-url")


@pytest.mark.asyncio
async def test_get_status_existing_job():
    """Test getting status of existing job."""
    url = "https://github.com/owner/repo"
    repo_id = repo_analysis.start_analysis(url)

    status = repo_analysis.get_status(repo_id)
    assert status is not None
    assert status.id == repo_id
    assert status.error is None

    await asyncio.sleep(0.05)


def test_get_status_nonexistent_job():
    """Test getting status of non-existent job."""
    status = repo_analysis.get_status("nonexistent-id")
    assert status is None


@pytest.mark.asyncio
async def test_get_repo_data_after_fetch_completes():
    """Test repo data is populated once the background fetch finishes."""
    repo_id = repo_analysis.start_analysis("https://github.com/owner/repo")

    await asyncio.sleep(0.05)  # let the mocked background fetch finish

    status = repo_analysis.get_status(repo_id)
    assert status.status == AnalysisStatus.READY
    assert status.files_indexed == 1

    data = repo_analysis.get_repo_data(repo_id)
    assert data is not None
    assert data["owner"] == "owner"
    assert data["repo"] == "repo"
    assert data["file_count"] == 1


def test_get_repo_data_nonexistent():
    """Test getting repo data for a job that doesn't exist."""
    result = repo_analysis.get_repo_data("nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_multiple_repos():
    """Test handling multiple repository requests."""
    urls = [
        "https://github.com/owner1/repo1",
        "https://github.com/owner2/repo2",
        "https://github.com/owner3/repo3",
    ]

    repo_ids = [repo_analysis.start_analysis(url) for url in urls]

    # All should be unique
    assert len(set(repo_ids)) == 3

    # All should have status
    for repo_id in repo_ids:
        status = repo_analysis.get_status(repo_id)
        assert status is not None
        assert status.status == AnalysisStatus.PENDING

    await asyncio.sleep(0.05)
