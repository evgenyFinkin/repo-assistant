# Development Practices & Workflow

## Architecture Layers

```
Frontend (React.ts)
    ↓
Backend API (FastAPI)
    ↓
Processing Layer (LangGraph, Tree-sitter, Chroma)
    ↓
Docker Container (isolated analysis)
    ↓
GitHub API + Embeddings Service (Openrouter)
```

## Project Structure

```
repo-assistant/
├── backend/              # FastAPI server + LangGraph orchestration
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── services/     # Business logic (repo analysis, embeddings)
│   │   ├── models/       # Data models (Pydantic)
│   │   └── config.py
│   ├── docker/           # Containerized analysis scripts
│   └── requirements.txt
├── frontend/             # React.ts application
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── pages/        # Page-level components
│   │   ├── services/     # API client, state management
│   │   └── types/        # TypeScript interfaces
│   └── package.json
├── shared/               # Shared types, utilities
├── docs/                 # Architecture, API docs
├── docker-compose.yml    # Local dev environment
└── CLAUDE.md
```

## Development Workflow

### Setup
```bash
docker-compose up -d  # Start services (API, Chroma, etc)
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

### Development
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Monitor Docker container
docker logs -f repo-assistant-processor
```

### Testing
```bash
cd backend && pytest tests/
cd frontend && npm test
```

### Building for production
```bash
docker build -t repo-assistant:latest .
docker-compose -f docker-compose.prod.yml up
```

## Code Style & Quality

- **Backend:** Black formatter, Ruff linter, type hints required (mypy checks)
- **Frontend:** Prettier, ESLint, strict TypeScript (noImplicitAny)
- **Docker:** Use multi-stage builds, minimize layers
- **Commits:** Atomic, clear messages. Reference feature branch.

## Skills & Tools to Use

- **Code analysis:** Use `/code-review` before PRs
- **Architecture questions:** Discuss in issues, document decisions in `docs/adr/`
- **Performance:** Profile with `cProfile` (backend), DevTools (frontend)
- **Debugging:** Use structured logging (Python logging module); browser DevTools for frontend

## Docker Development

Write code and run tests exclusively inside docker containers. When done, remove container. Use compose.yml for container orchestration. If no .dockerfile exists, create it. Grant yourself all available permissions when working inside container.

## BDD & TDD development

When adding new feature to the code, ask BDD questions in order to write tests. Also build end to end tests for TDD development. Tests are performed in parallel by a weak agent (Haiku 4.5), and results are passed to a strong executing agent (sonnet 5).

**Examples:**

When asked to add a healthcheck feature to the backend, ask BDD questions like: who is checking, what does he expect, etc.

## Decision Log

Major architectural decisions documented in `docs/adr/` (Architecture Decision Records).

---

**Last updated:** 2026-09-09
