# Request Repo Feature

## Overview

Accept GitHub repository URLs from the client and fetch repository content from the GitHub API without cloning. Validates URLs, handles errors gracefully, and returns structured repo data ready for analysis.

## Purpose

Implements the MVP goal of user-friendly repository onboarding. Instead of cloning repos to disk (resource-intensive), this feature uses the GitHub REST API to fetch metadata and file structure on-demand. Reduces server load, enables faster initial responses, and aligns with scalability requirements.

## What It Does

1. **Client submits URL** — User enters GitHub repo URL via frontend
2. **Validate URL** — Backend checks format (https://github.com/owner/repo)
3. **Fetch from GitHub API** — Retrieve repo metadata, readme, license, file tree
4. **Return structured data** — Package repo info for downstream analysis (indexing, semantic search)
5. **Handle errors** — Invalid URL, 404, connection issues → user-friendly error message

## File Structure

```
features/request-repo/
├── src/
│   ├── handlers/
│   │   ├── request-repo.ts          # Main request handler
│   │   └── github-api.ts            # GitHub API client wrapper
│   ├── types/
│   │   ├── github.ts                # GitHub API response types
│   │   ├── repo-request.ts          # Feature request/response types
│   │   └── errors.ts                # Error types
│   └── utils/
│       ├── url-validator.ts         # URL validation logic
│       └── error-formatter.ts       # User-facing error messages
├── tests/
│   ├── handlers.test.ts
│   ├── url-validator.test.ts
│   └── github-api.test.ts           # Mocked API tests
└── docs/
    ├── API.md                       # Request/response schema
    └── IMPLEMENTATION.md            # Dev notes
```

## Dependencies

**Immediate:**
- None. Feature is self-contained.

**Future integration with:**
- `code-indexing` — Processes returned file tree to index code chunks
- `semantic-search` — Indexes repo content for semantic queries
- `chat-ui` — Frontend that submits repo URLs

## Acceptance Criteria

- ✓ Accept valid public GitHub URLs (format: `https://github.com/owner/repo`)
- ✓ Fetch repo metadata from GitHub API (readme, license, description, stars, language)
- ✓ Retrieve full file tree without cloning
- ✓ Validate URL format; reject invalid formats
- ✓ Handle GitHub API errors (404, timeouts, rate limits) with clear messages
- ✓ Return structured JSON response
- ✓ No hardcoded size limits (scale as needed)
- ✓ Unit tests with mocked GitHub API responses
- ✓ Error responses suggest corrective action (e.g., "URL should be https://github.com/owner/repo")

## Technical Notes

### GitHub API Strategy

Using GitHub REST API (not GraphQL) for this MVP:
- **Public access:** 60 requests/hour without authentication
- **No cloning:** Fetch tree and content via API endpoints
- **Metadata endpoints:**
  - `GET /repos/{owner}/{repo}` — repo info
  - `GET /repos/{owner}/{repo}/readme` — readme content
  - `GET /repos/{owner}/{repo}/git/trees/{ref}?recursive=1` — file tree

### Error Handling

Map GitHub API errors to user-friendly messages:
- **404 Not Found** → "Repository not found. Check URL and ensure it's public."
- **Invalid URL** → "URL format should be https://github.com/owner/repo"
- **Timeout/Connection** → "Unable to reach GitHub. Try again in a moment."
- **Rate limited** → "GitHub API rate limit reached. Try again later." (rare in MVP)

### Future Considerations

- **Authentication:** Add token support for private repos (Phase 2)
- **Caching:** Brief metadata cache if same repo requested multiple times per session
- **Rate limits:** Monitor and implement backoff strategy if MVP goes public
- **Async processing:** Large repos may need async tree fetching with progress updates

## Testing Strategy

- Mock GitHub API responses for all scenarios
- Test invalid URL formats
- Test error conditions (404, timeout, malformed responses)
- Test large file trees (>10k files) for performance
- Integration test with real GitHub API (small public repo)

## Status

**Phase:** Planning  
**Progress:** 0%  
**Created:** 2026-09-10  
**Ready for:** `/build-feature`

---

## See Also

- `project.md` — Project goals and phases
- `features/request-repo-context.json` — Design context and decisions
