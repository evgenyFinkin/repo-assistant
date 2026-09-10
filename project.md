# repo-assistant: Project Overview

## Purpose

Help developers quickly understand unfamiliar open-source repositories by allowing natural-language questions about a GitHub project instead of manual source browsing.

## Problem

Open-source developers and maintainers spend significant time:
- Onboarding to unfamiliar codebases
- Answering repetitive questions about project architecture
- Pointing users to relevant files in documentation and code
- Understanding legacy or large projects

**Solution:** Conversational AI interface to GitHub repositories that retrieves source-grounded answers with file references.

## Goals

1. **User-friendly onboarding:** Accept GitHub URL, handle cloning and analysis automatically
2. **Accurate retrieval:** Parse, chunk, and index code/docs with semantic search
3. **Source-grounded answers:** Generate responses with references to specific files and line numbers
4. **Scalable processing:** Run analysis in isolated Docker containers
5. **Conversational UX:** Chat interface that maintains context across questions

## Success Metrics

- Answer latency: <5s for typical queries
- Retrieval precision: Relevant code sections included in context >80% of queries
- User satisfaction: Clear, referenced answers with minimal hallucination
- Scalability: Handle repositories up to 100k files without excessive resource use

## Scope

**MVP (Phase 1):**
- Public repos only
- Read-only analysis (no write operations)
- Ephemeral sessions (no persistence between chats)
- Single repo per session

**Future phases:**
- Private repos (auth + token handling)
- Persistent chat history
- Multi-repo queries
- Issue tracking integration
- Code search across organizations

## Planned Features

### MVP Phase 1

1. **request-repo** — Accept GitHub URL, fetch from API, validate, return repo data
   - Status: ✓ Complete
   - Location: `features/request-repo/`
   - Implementation: GitHub REST API client, async fetching, status tracking
   - Tests: `test_github_api.py`, `test_repo_analysis.py`
   - API: `POST /api/repositories`, `GET /api/repositories/{id}/status`

---

**Status:** Project initialization
**Created:** 2026-09-09
