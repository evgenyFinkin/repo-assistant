# Feature: MVP (Minimum Viable Product)

## Overview

Core functionality to enable asking natural-language questions about a GitHub repository.

## User Stories

### Story 1: Accept Repository URL
**As a** user  
**I want to** provide a GitHub repository URL  
**So that** the system can analyze that repository

**Acceptance Criteria:**
- Input field accepts valid GitHub HTTPS URLs (e.g., `https://github.com/owner/repo`)
- Validate URL format and repo accessibility (public only)
- Show loading state during clone + analysis
- Handle errors: invalid URL, repo not found, private repo

### Story 2: Analyze Repository
**As a** system  
**I want to** clone, parse, and index repository content  
**So that** I can answer questions about it

**Acceptance Criteria:**
- Clone public repo from GitHub
- Extract source files (exclude: node_modules, .git, build artifacts)
- Parse code using Tree-sitter (JavaScript, Python, TypeScript, Go)
- Extract documentation (README.md, .md files, code comments)
- Chunk content (1000-2000 token chunks with overlap)
- Generate embeddings using Openrouter (ling-3.0-flash-fin:free)
- Store in Chroma vector DB
- Run entirely in Docker container (isolated from host)

### Story 3: Chat Interface
**As a** user  
**I want to** ask questions about the repository in natural language  
**So that** I can understand its structure, API, and purpose

**Acceptance Criteria:**
- Text input for questions
- Send button, clear button
- Display chat history (user Q, assistant A)
- Show "retrieving..." during processing
- Format code blocks in responses

### Story 4: Source-Grounded Answers
**As a** assistant  
**I want to** include file references and code snippets  
**So that** users can trust and verify my answers

**Acceptance Criteria:**
- Retrieve top 5 relevant chunks from vector DB
- Pass chunks to LLM with instructions to cite sources
- Format references: `[filename:line-range](link-to-file)`
- Show code snippets inline
- Include retrieval confidence/similarity scores

### Story 5: Error Handling & Limits
**As a** developer  
**I want to** handle large repos and API limits gracefully  
**So that** the system remains stable

**Acceptance Criteria:**
- Timeout on analysis >60 seconds (show warning)
- Rate limit on Openrouter API (queue requests)
- Memory limits in Docker container
- User-friendly error messages
- Logs for debugging

## Technical Tasks

### Backend (FastAPI + LangGraph)
- [ ] POST `/api/repositories` — accept GitHub URL, trigger analysis
- [ ] GET `/api/repositories/{id}/status` — check analysis status
- [ ] POST `/api/chat/{id}` — send question, get answer
- [ ] Integrate Tree-sitter for code parsing
- [ ] Integrate Chroma for vector storage
- [ ] Create LangGraph workflow: analyze → embed → store → retrieve → generate
- [ ] Docker orchestration for analysis jobs

### Frontend (React.ts)
- [ ] URL input form with validation
- [ ] Loading spinner during analysis
- [ ] Chat component (message list + input)
- [ ] Display formatted responses with code blocks
- [ ] Error handling & user feedback

### Deployment
- [ ] Docker images for backend, processor
- [ ] docker-compose for local dev
- [ ] Environment variable management
- [ ] API documentation (OpenAPI)

---

**Status:** Not started  
**Priority:** P0 (blocking all other work)  
**Estimated Effort:** 4-6 weeks
