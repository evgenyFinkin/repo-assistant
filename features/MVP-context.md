# MVP Feature Context

## Problem Statement

Developers need a fast way to understand unfamiliar GitHub repositories without manually searching through source code, documentation, and issues.

## Solution Approach

Build a chat interface that:
1. Accepts a public GitHub repo URL
2. Clones and analyzes the repo (parsing, chunking, embedding)
3. Answers user questions with source-grounded responses (file references + code snippets)

## Key Technical Decisions

### Stack Choices

**Backend: FastAPI + LangGraph**
- FastAPI: Fast, async-ready, automatic OpenAPI docs
- LangGraph: Orchestrate multi-step workflows (clone → parse → embed → retrieve → generate)
- Why not: Django (overkill), Flask (too minimal)

**Processing: Python + Tree-sitter**
- Tree-sitter: Accurate AST parsing for multiple languages (JS, Python, TS, Go)
- Why not: Language-specific parsers (fragmented), regex (unreliable)

**Embeddings: Openrouter (ling-3.0-flash-fin:free)**
- Free tier available
- Fast, good quality for code/docs
- Why not: OpenAI (cost), Ollama (latency, host infra)

**Vector DB: Chroma**
- Lightweight, local-first, easy to embed
- Good for MVP; can migrate to Weaviate/Pinecone later
- Why not: Pinecone (cost/overkill), PostgreSQL pgvector (more setup)

**Frontend: React + TypeScript**
- TypeScript for type safety
- React for interactive UI
- Why not: Vue/Angular (team familiarity, React ecosystem)

**Containerization: Docker**
- Isolate repo analysis (security + reproducibility)
- Simplify deployment
- Multi-stage builds to reduce image size

### Architecture Decisions

**Why isolated Docker container for analysis?**
- Security: Arbitrary GitHub repos might contain malicious code (future: sandboxing)
- Reproducibility: Same environment across dev/prod
- Scalability: Can spawn multiple workers for parallel analyses

**Why chunking + embeddings over full-file indexing?**
- Embeddings preserve semantic meaning (vs keyword search)
- Chunking keeps context window manageable for LLM
- Allows retrieval of most relevant code sections

**Why LLM generation over template-based answers?**
- Natural language responses to varied questions
- Can synthesize insights across multiple code sections
- Adaptable to different query styles

## Known Limitations (MVP)

1. **Public repos only** — Private repos need auth (phase 2)
2. **No persistence** — Chat history lost on page refresh (phase 2)
3. **Single repo per session** — Multi-repo queries in phase 2
4. **Large repos slow** — Need optimization for 100k+ files (phase 2)
5. **No code execution** — Can't run tests/examples yet
6. **Language support** — Only: JS, Python, TS, Go (extensible via Tree-sitter)

## Integration Points

| Component | Purpose | Notes |
|-----------|---------|-------|
| GitHub API | Repo metadata, clone | Public repos, rate limits |
| Openrouter | Embeddings + LLM generation | Free tier, ling-3.0-flash-fin |
| Chroma | Vector storage | Local instance, ephemeral |
| Tree-sitter | Code parsing | Language plugins |
| Docker | Process isolation | Buildkit for efficiency |

## Success Criteria

- User can ask 3+ questions about a repo in <30 seconds
- Answers cite relevant files 90%+ of the time
- No hallucinated file paths or code
- Handles repos up to 100k files without OOM

## Open Questions

1. **Chunking strategy:** Fixed size vs semantic chunks? Overlap amount?
2. **LLM instructions:** How to best prompt for citations?
3. **Scale:** How many concurrent analyses? Memory per container?
4. **Privacy:** Log user queries? For analytics?

---

**Last updated:** 2026-09-09  
**Related:** [[MVP]]
