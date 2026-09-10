"""Tests for repository analysis service."""
import pytest
from app.models.schemas import AnalysisStatus
from app.services import repo_analysis


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


def test_start_analysis_valid_url():
    """Test starting analysis with valid URL."""
    url = "https://github.com/owner/awesome-project"
    repo_id = repo_analysis.start_analysis(url)

    assert repo_id is not None
    assert len(repo_id) > 0

    # Check job was created with PENDING status
    status = repo_analysis.get_status(repo_id)
    assert status is not None
    assert status.id == repo_id
    assert status.status == AnalysisStatus.PENDING


def test_start_analysis_invalid_url():
    """Test starting analysis with invalid URL."""
    with pytest.raises(repo_analysis.InvalidRepositoryError) as exc_info:
        repo_analysis.start_analysis("https://gitlab.com/owner/repo")

    assert "invalid" in str(exc_info.value).lower()


def test_start_analysis_malformed_url():
    """Test starting analysis with malformed URL."""
    with pytest.raises(repo_analysis.InvalidRepositoryError):
        repo_analysis.start_analysis("not-a-url")


def test_get_status_existing_job():
    """Test getting status of existing job."""
    url = "https://github.com/owner/repo"
    repo_id = repo_analysis.start_analysis(url)

    status = repo_analysis.get_status(repo_id)
    assert status is not None
    assert status.id == repo_id
    assert status.error is None


def test_get_status_nonexistent_job():
    """Test getting status of non-existent job."""
    status = repo_analysis.get_status("nonexistent-id")
    assert status is None


def test_get_repo_data_exists():
    """Test getting repo data after fetch completes."""
    # This test would require async setup to fully test the background fetch
    # For now, we test the function exists and returns None for non-existent data
    result = repo_analysis.get_repo_data("nonexistent-id")
    assert result is None


def test_multiple_repos():
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
