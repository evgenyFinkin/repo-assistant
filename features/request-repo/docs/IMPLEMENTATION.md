# Request Repo Feature — Implementation

## Overview

This document describes the implementation of the `request-repo` feature, which accepts GitHub repository URLs and fetches repository metadata and file tree from the GitHub REST API without cloning.

## Architecture

```
┌─────────────────────────────────────────────┐
│ Frontend (React/Next.js)                    │
│ User submits GitHub URL                     │
└──────────────────┬──────────────────────────┘
                   │ POST /api/repositories
                   ▼
┌─────────────────────────────────────────────┐
│ FastAPI Backend                             │
│ api/repositories.py::create_repository()    │
│ - Validates URL format                      │
│ - Calls repo_analysis.start_analysis()      │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│ Repository Analysis Service                 │
│ services/repo_analysis.py                   │
│ - Parses GitHub URL (owner/repo)            │
│ - Creates job record (PENDING status)       │
│ - Starts async task for fetching            │
└──────────────────┬──────────────────────────┘
                   │ (async)
                   ▼
┌─────────────────────────────────────────────┐
│ GitHub API Client                           │
│ services/github_api.py                      │
│ - Fetch repo metadata (/repos/{o}/{r})      │
│ - Fetch README (/repos/{o}/{r}/readme)      │
│ - Fetch file tree (/git/trees/{ref})        │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
         GitHub REST API
         (public endpoint)
```

## Key Components

### 1. GitHub API Client (`services/github_api.py`)

Wrapper around GitHub REST API with error handling.

**Class: `GitHubAPIClient`**

```python
# Initialize with optional GitHub token
client = GitHubAPIClient(token="ghp_...")

# Fetch repo metadata
metadata = await client.fetch_repo_metadata("owner", "repo")
# Returns: name, description, language, stars, forks, topics, etc.

# Fetch README
readme = await client.fetch_repo_readme("owner", "repo")
# Returns: README content as string, or None if not found

# Fetch file tree
tree = await client.fetch_file_tree("owner", "repo", ref="main")
# Returns: List of files/dirs with metadata
```

**Error Handling:**

- `GitHubRepositoryNotFoundError` (404) — Repository not found or private
- `GitHubRateLimitError` (403) — API rate limit exceeded
- `GitHubConnectionError` — Network error connecting to GitHub
- `GitHubAPIError` — Other GitHub API errors

**Rate Limits:**

- **Without token:** 60 requests/hour (per IP)
- **With token:** 5,000 requests/hour (per user)

The MVP uses public endpoint without token.

### 2. Repository Analysis Service (`services/repo_analysis.py`)

Orchestrates repository intake and status tracking.

**Key Functions:**

```python
# Start analysis
repo_id = start_analysis(url: str) -> str
# - Validates URL format
# - Creates job record
# - Starts async fetch task
# - Returns job ID

# Get analysis status
status = get_status(repo_id: str) -> RepositoryStatusResponse | None
# Returns: id, status, error (if failed), files_indexed

# Get repository data
data = get_repo_data(repo_id: str) -> dict | None
# Returns: metadata, readme, file_tree, file_count
```

**Job Lifecycle:**

```
PENDING      → URL received, validation passed
    ↓
CLONING      → Fetching repo metadata from GitHub API
    ↓
PARSING      → Fetching file tree
    ↓
READY        → Analysis complete, ready for embedding
    ↓
(→ EMBEDDING → FAILED [optional next phases])
```

**Error States:**

If any step fails, status becomes `FAILED` and `error` field is populated.

### 3. API Endpoint (`api/repositories.py`)

```http
POST /api/repositories
Content-Type: application/json

{
  "url": "https://github.com/owner/repo"
}

Response 200:
{
  "id": "a1b2c3d4-...",
  "status": "pending"
}

Response 400:
{
  "detail": "Invalid GitHub URL format. Expected: https://github.com/owner/repo"
}
```

**Polling Status:**

```http
GET /api/repositories/{repo_id}/status

Response 200:
{
  "id": "a1b2c3d4-...",
  "status": "ready",
  "files_indexed": 247,
  "error": null
}
```

## Implementation Details

### URL Validation

Regex pattern: `^https://github\.com/([\w.-]+)/([\w.-]+)/?$`

- Must be HTTPS (not HTTP)
- Must be github.com domain
- Owner and repo can contain alphanumerics, dots, dashes, underscores
- Trailing slash optional

**Examples:**

✓ `https://github.com/owner/repo`
✓ `https://github.com/my-org/my.repo-name/`
✗ `https://gitlab.com/owner/repo` (wrong domain)
✗ `http://github.com/owner/repo` (not HTTPS)
✗ `https://github.com/owner` (missing repo)

### Async Task Management

File tree fetching happens in background using `asyncio.create_task()`:

1. User submits URL → endpoint returns immediately with job ID
2. Backend fetches repo data async
3. Frontend polls `/repositories/{id}/status` for completion
4. When `status` becomes `ready`, data is available for next phase (embedding)

**Why async?**

- GitHub API calls take 1-3 seconds each
- Fetching large file trees (100k+ files) takes longer
- Frontend needs immediate response with job ID for progress tracking

### File Tree Filtering

Common paths excluded to reduce noise:

```python
excluded = {"node_modules", ".git", "dist", "build", "__pycache__"}
```

These are filtered server-side before storing.

### Storage Strategy

**In MVP:**

- `_JOBS` dict: Job status records (in-memory)
- `_REPO_DATA` dict: Fetched repo data (in-memory)

**Limitations:**

- Data lost on server restart
- Doesn't scale beyond single worker
- Not suitable for production

**TODO for Phase 2:**

- Replace with database (PostgreSQL/MongoDB)
- Add Redis for job queue
- Implement proper async task framework (Celery/RQ)

## Testing Strategy

### Unit Tests

**`test_github_api.py`**

- Valid repo metadata fetch
- Invalid repo (404) error handling
- Rate limit (403) error handling
- Connection errors
- README fetch (exists and not found)
- File tree with exclusion filters
- Client initialization with/without token

**`test_repo_analysis.py`**

- URL parsing (valid/invalid formats)
- Job creation and status tracking
- Multiple concurrent jobs
- Error propagation from GitHub API

### Integration Tests

Run in Docker:

```bash
# Build image
docker build -t repo-assistant-backend .

# Run tests
docker run --rm repo-assistant-backend pytest tests/ -v

# Run app
docker run -p 8000:8000 repo-assistant-backend
```

**Manual Testing:**

```bash
# Start backend
python -m uvicorn app.main:app --reload

# Submit repo
curl -X POST http://localhost:8000/api/repositories \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/python/cpython"}'

# Expected response
# {
#   "id": "a1b2c3d4-...",
#   "status": "pending"
# }

# Poll status
curl http://localhost:8000/api/repositories/a1b2c3d4-../status

# Expected after 2-3 seconds
# {
#   "id": "a1b2c3d4-...",
#   "status": "ready",
#   "files_indexed": 3847,
#   "error": null
# }
```

## Error Scenarios

| Scenario | Error Code | Message | Solution |
|----------|------------|---------|----------|
| Invalid URL format | 400 | "Invalid GitHub URL format..." | Check URL starts with `https://github.com/owner/repo` |
| Repo not found | Failed status | "Repository not found. Check URL..." | Verify repo exists and is public |
| Private repo | Failed status | "Repository not found..." | OAuth/token auth needed (Phase 2) |
| GitHub down | Failed status | "Connection error..." | Retry after GitHub is back online |
| Rate limited | Failed status | "API rate limit exceeded..." | Implement token support or caching |
| Network timeout | Failed status | "Connection error..." | Check internet connection |

## Performance Notes

**GitHub API Latency:**

- Metadata fetch: ~200-500ms
- README fetch: ~200-500ms
- File tree (small repo <1k files): ~500-1000ms
- File tree (large repo 10k+ files): ~2-5s

**Total time:** Typically 1-3 seconds for small-medium repos

**Scaling Considerations:**

- For repos >100k files: Might need pagination or async tree walking
- Add caching if same repo requested multiple times
- Consider GitHub GraphQL API for better batching (future optimization)

## Future Enhancements

1. **Authentication** (Phase 2)
   - Add GitHub token support from user settings
   - Higher rate limits (5k req/hour)
   - Access to private repos

2. **Caching** (Phase 2)
   - Cache metadata for 24 hours
   - Cache file tree for 1 week
   - Reduce API calls and costs

3. **Async Improvements** (Phase 2)
   - Replace in-memory `_JOBS` with proper job queue (Redis/Celery)
   - Support for distributed analysis workers
   - Webhook-based status updates instead of polling

4. **Large Repo Handling** (Phase 2/3)
   - Paginate file tree for repos >100k files
   - Stream tree to frontend
   - Lazy loading of file contents

5. **Monitoring** (Phase 2)
   - Track API error rates
   - Monitor rate limit usage
   - Alert on GitHub API issues

## See Also

- `../request-repo.md` — Feature overview
- `../request-repo-context.json` — Design decisions
- `API.md` — Request/response schema documentation
