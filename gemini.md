# Gemini Context & Project Guide: ReSearch_Mate

## Project Overview
**ReSearch_Mate** is a fully offline, self-hosted Agentic AI research assistant designed to help researchers analyze and compare academic papers using Retrieval-Augmented Generation (RAG), LangGraph multi-agent workflows, and citation verification.

---

## Key Tech Stack
- **Frontend**: React, Vite, Tailwind CSS, pdfjs-dist
- **Backend**: Python 3.10+, FastAPI (async), Server-Sent Events (SSE)
- **Database & Vector Store**: PostgreSQL with `pgvector` (HNSW index)
- **Local AI & Embeddings**:
  - LLM: `llama3.1:8b-instruct` via Ollama
  - Embeddings: `BAAI/bge-small-en-v1.5`
- **Agent Orchestration**: LangGraph
  - Retrieval Agent
  - Analysis Agent
  - Comparison Agent
  - Research Gap Agent
  - Citation Verifier Agent
- **Document Processing**: PyMuPDF (`fitz`) for section- and page-aware chunking

---

## Core Guidelines & Conventions
1. **Offline & Privacy First**: Rely on local model execution (Ollama, local embeddings) without third-party AI API leaks.
2. **Citation Verification**: Every claim must be grounded in source chunks and page numbers. Unsupported claims must be flagged or discarded.
3. **Clean Architecture**:
   - Keep document parsing, vector indexing, retrieval, and agent workflows modular.
   - Maintain strict typed schemas (e.g. Pydantic) for agent inputs/outputs.
4. **Code Quality**: Follow standard Python (PEP 8, type hinting) and modern React/TypeScript best practices.

---

## Expert AI Engineering Workflow & Execution Rules

> **Core Philosophy:**
> AI agents are built to finish tasks, not to judge quality or security. You have to be the one who checks and challenges it. Doing this makes your product stronger and develops deep engineering skills along the way. Never let the AI code freely without rules, tests, and adversarial audits.

### 1. Set Rules + Checklist Before You Start
- Follow strict project rules and an explicit checklist whenever building features or modifying code. Never code freely without predefined constraints and acceptance criteria.

### 2. Force Proper Testing From the Start (TDD & Cleanup)
- **Unit Tests First (Non-negotiable):** Always write unit tests before implementing the actual code.
- **Integration Tests:** Add integration tests covering cross-module and API workflows.
- **Test-Driven Development (TDD):** Follow strict TDD (write tests -> verify failure/coverage -> write code -> pass tests).
- **Delete Test Files After Testing:** Always clean up and delete test files and temporary test artifacts once testing has been completed.

### 3. Make the AI Attack Its Own Work (Adversarial Audit)
- Once a feature is marked "complete", act as an adversarial **security / penetration tester** and actively try to break it.
- **Do not fix immediately:** First systematically list all weak points, edge-case vulnerabilities, and improvement areas.
- Catch bugs and security flaws early before final deployment.

### 4. Load Test It
- Simulate heavy traffic (e.g., thousands of simultaneous users/requests) to see what breaks, where flows fail, and where bottlenecks emerge.


