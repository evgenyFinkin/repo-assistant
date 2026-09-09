# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Status

**Note:** This is a new project in early initialization. Fill in sections below as the project structure solidifies.

## Build & Development Commands

Once the project is set up, document key commands here:

```bash
# Installation
npm install / yarn install / [package manager]

# Development
npm run dev

# Build
npm run build

# Tests
npm test
npm run test:watch
npm run test:unit
npm run test:integration

# Linting
npm run lint
npm run lint:fix

# Type checking (if applicable)
npm run type-check
```

## Project Architecture

### Overview

[Add high-level description of what this project does and its core purpose]

### Directory Structure

[Document key directories and their roles once structure is established]

Example structure to update:
- `src/` — Source code
- `tests/` — Test files
- `docs/` — Documentation
- `scripts/` — Build/automation scripts

### Key Technologies

[List primary frameworks, libraries, and runtime — e.g., Node.js, React, TypeScript, database]

### Architecture Patterns

[Document any significant patterns: API design, state management, data flow, plugin system, etc. that require reading multiple files to understand]

## Development Workflow

- **Branch strategy:** [e.g., main is protected, PRs required]
- **Testing requirement:** [e.g., all PRs must pass CI]
- **Code style:** [e.g., enforced via linter/prettier]

## External Configuration

If this project imports settings from other tools (Cursor, Copilot, Gemini CLI, OpenAI Codex), check `.cursor/rules/`, `.github/copilot-instructions.md`, or similar.

## Notes for Claude Code

[Add any project-specific guidance, quirks, or gotchas that affect how Claude should approach tasks]

---

**Created:** 2026-09-09
