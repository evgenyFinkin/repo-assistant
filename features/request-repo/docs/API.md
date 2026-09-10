# Request Repo API Documentation

## Endpoints

### Create Repository Analysis

**Endpoint:** `POST /api/repositories`

Accept a GitHub repository URL and start background analysis.

**Request:**

```json
{
  "url": "https://github.com/owner/repo"
}
```

**Fields:**

- `url` (string, required): Public GitHub HTTPS URL in format `https://github.com/owner/repo`

**Response 200 (OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

**Response 400 (Bad Request):**

```json
{
  "detail": "Invalid GitHub URL format. Expected: https://github.com/owner/repo"
}
```

**Status Values:**

- `pending` — URL validated, fetching from GitHub API
- `cloning` — Fetching repo metadata
- `parsing` — Fetching file tree
- `embedding` — Processing files (future phase)
- `ready` — Analysis complete, ready for queries
- `failed` — Error occurred (see `error` field in status response)

---

### Get Repository Status

**Endpoint:** `GET /api/repositories/{repo_id}/status`

Poll the analysis status of a repository.

**Path Parameters:**

- `repo_id` (string, required): Job ID from repository creation response

**Response 200 (OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "ready",
  "files_indexed": 247,
  "error": null
}
```

**Response 404 (Not Found):**

```json
{
  "detail": "repository not found"
}
```

**Fields:**

- `id`: Job identifier
- `status`: Current analysis phase
- `files_indexed`: Number of files processed (when ready)
- `error`: Error message if analysis failed

---

## Response Schemas

### RepositoryCreateRequest

```typescript
interface RepositoryCreateRequest {
  url: string;  // e.g., "https://github.com/python/cpython"
}
```

### RepositoryCreateResponse

```typescript
interface RepositoryCreateResponse {
  id: string;              // UUID
  status: AnalysisStatus;  // "pending" | "cloning" | "parsing" | ...
}
```

### RepositoryStatusResponse

```typescript
interface RepositoryStatusResponse {
  id: string;
  status: AnalysisStatus;
  error?: string | null;       // Error message if failed
  files_indexed?: number | null; // Count when ready
}
```

### AnalysisStatus (Enum)

```python
class AnalysisStatus(str, Enum):
    PENDING = "pending"     # Initial state
    CLONING = "cloning"     # Fetching metadata
    PARSING = "parsing"     # Fetching file tree
    EMBEDDING = "embedding" # Processing (future)
    READY = "ready"         # Complete
    FAILED = "failed"       # Error occurred
```

---

## Example Usage

### JavaScript/TypeScript

```typescript
// 1. Create repository analysis job
const createResponse = await fetch("http://localhost:8000/api/repositories", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    url: "https://github.com/facebook/react"
  })
});

const { id, status } = await createResponse.json();
console.log(`Job created: ${id}, status: ${status}`);

// 2. Poll status until ready
async function waitForReady(jobId, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    const statusResponse = await fetch(
      `http://localhost:8000/api/repositories/${jobId}/status`
    );
    const { status, error, files_indexed } = await statusResponse.json();

    console.log(`Status: ${status}, Files: ${files_indexed}`);

    if (status === "ready") {
      return { success: true, files_indexed };
    } else if (status === "failed") {
      return { success: false, error };
    }

    // Wait 1 second before polling again
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  throw new Error("Timeout waiting for analysis");
}

const result = await waitForReady(id);
if (result.success) {
  console.log(`Analysis complete! ${result.files_indexed} files indexed.`);
} else {
  console.error(`Analysis failed: ${result.error}`);
}
```

### Python

```python
import httpx
import asyncio

async def analyze_repo(url: str):
    async with httpx.AsyncClient() as client:
        # 1. Create job
        create_response = await client.post(
            "http://localhost:8000/api/repositories",
            json={"url": url}
        )
        job_id = create_response.json()["id"]
        print(f"Job created: {job_id}")

        # 2. Poll until ready
        for attempt in range(30):
            status_response = await client.get(
                f"http://localhost:8000/api/repositories/{job_id}/status"
            )
            data = status_response.json()
            status = data["status"]
            print(f"Status: {status}")

            if status == "ready":
                print(f"Complete! {data['files_indexed']} files indexed.")
                return data
            elif status == "failed":
                raise Exception(f"Analysis failed: {data['error']}")

            await asyncio.sleep(1)

        raise TimeoutError("Analysis timeout")

# Usage
result = asyncio.run(analyze_repo("https://github.com/python/cpython"))
```

### cURL

```bash
# 1. Create repository analysis
curl -X POST http://localhost:8000/api/repositories \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/python/cpython"
  }'

# Response:
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "status": "pending"
# }

# 2. Poll status (repeat until status changes)
curl http://localhost:8000/api/repositories/550e8400-e29b-41d4-a716-446655440000/status

# Response:
# {
#   "id": "550e8400-e29b-41d4-a716-446655440000",
#   "status": "ready",
#   "files_indexed": 3847,
#   "error": null
# }
```

---

## Error Handling

### Client-Side Validation

Before calling the API, validate URL format:

```regex
^https://github\.com/[\w.-]+/[\w.-]+/?$
```

### Common Errors

| Status Code | Error | Cause | Solution |
|-------------|-------|-------|----------|
| 400 | Invalid URL format | Malformed URL or wrong domain | Use format: `https://github.com/owner/repo` |
| 404 | repository not found | Job ID doesn't exist | Verify job ID was returned from create endpoint |
| Failed status | "Repository not found" | Repo doesn't exist or is private | Check URL and ensure repo is public |
| Failed status | "Connection error" | Network issue | Retry request, check GitHub status |
| Failed status | "API rate limit exceeded" | Too many requests to GitHub | Implement token auth (Phase 2) |

### Retry Logic

```typescript
async function createWithRetry(url: string, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch("http://localhost:8000/api/repositories", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });

      if (response.status === 400) {
        // Bad request — don't retry
        throw new Error("Invalid URL");
      }

      if (!response.ok) {
        // Server error — retry with backoff
        await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
        continue;
      }

      return response.json();
    } catch (e) {
      if (i === maxRetries - 1) throw e;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

---

## Rate Limits

GitHub API has rate limits based on authentication:

**Without token (MVP):**
- 60 requests per hour per IP
- Shared across all users at your IP

**With token (Phase 2):**
- 5,000 requests per hour per user
- Recommended for production

**Recommendations:**

1. Add token support in Phase 2
2. Implement request caching
3. Monitor rate limit usage via response headers
4. Implement backoff for 429 responses

---

## API Health

**Endpoint:** `GET /health`

Check if API is running.

**Response 200:**

```json
{
  "status": "ok"
}
```
