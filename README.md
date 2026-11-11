# ReSearch_Mate

> **Offline, privacy-first agentic AI assistant for academic research.**  
> Analyze, compare, and extract insights from multiple research papers — entirely on your local machine. No cloud APIs. No data leakage.

---

## Overview

ReSearch_Mate is a fully self-hosted research assistant powered by a LangGraph multi-agent pipeline, local LLMs via Ollama, and a PostgreSQL + pgvector knowledge base. It ingests academic PDFs, indexes them with section-aware semantic chunking, and answers research questions with precise, grounded citations tied to page numbers.

The system is designed for researchers who need reliable, reproducible, and auditable AI assistance without sending sensitive academic work to third-party services.

---

## Features

- **Multi-Agent Orchestration** — LangGraph pipeline with dedicated Retrieval, Analysis, Comparison, Research Gap, and Citation Verifier agents
- **Local LLM Inference** — `llama3.1:8b-instruct` served via Ollama; zero external API calls
- **Semantic Search** — `BAAI/bge-small-en-v1.5` embeddings (384-dim) indexed in PostgreSQL with HNSW via pgvector
- **Citation Verification** — Every claim is grounded to a source passage with paper title and page number
- **Section-Aware PDF Chunking** — PyMuPDF extracts text with section and page metadata preserved
- **Literature Review Export** — Generate structured reviews in Markdown or LaTeX with one click
- **Secure Authentication** — PBKDF2 password hashing with HMAC-SHA256 JWT workspace tokens
- **Offline Training Pipeline** — 10,000+ synthetic academic Q&A dataset generator + LoRA fine-tuning config for local model adaptation
- **Answer Accuracy Evaluation** — Built-in evaluator scores keyword coverage, citation precision, detail completeness, and hallucination detection
- **React Frontend** — Three-panel UI: paper sidebar, chat interface, and in-browser PDF viewer

---

## Architecture

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React 18 + Vite + Tailwind CSS | Paper management, chat UI, PDF viewer, export controls |
| API Layer | FastAPI (async) + Server-Sent Events | Real-time streaming responses, file upload, auth endpoints |
| Agent Orchestration | LangGraph | Multi-step research pipelines with state management |
| Local LLM | Ollama (`llama3.1:8b-instruct`) | Answer generation, analysis, comparison |
| Embeddings | BAAI/bge-small-en-v1.5 (SentenceTransformers) | 384-dim dense vectors for semantic retrieval |
| Vector Store | PostgreSQL + pgvector (HNSW index) | Scalable approximate nearest-neighbor search |
| Reranker | CrossEncoderReranker (heuristic fallback) | Precision re-ranking of retrieved chunks |
| PDF Processing | PyMuPDF (fitz) | Section-aware, page-metadata-preserving text extraction |
| Database ORM | asyncpg connection pool | Async PostgreSQL access with schema migration runner |
| Authentication | PBKDF2 + HMAC-SHA256 JWT | Passwordless-dependency user auth and workspace isolation |
| Training | HuggingFace Transformers + PEFT (LoRA) | Fine-tuning adapter config for local llama3.1 |
| Export | Markdown + LaTeX renderer | Structured literature review generation |
| Containerization | Docker Compose | One-command full-stack deployment |

---

## Team

| Member | Role | Branch |
|---|---|---|
| Vivek Solanki | Infrastructure, API, Auth, Security | `feature/infra-api-architecture`, `feature/security-validation-hardening`, `feature/auth-user-workspaces` |
| Saksham Mahato | PDF Processing, Embeddings, Database, Retrieval | `feature/pdf-processing-database-retrieval`, `feature/database-pgvector-reranker`, `feature/async-pgvector-pool` |
| Grishma Doshi | Agents, Citation Verifier, Training Pipeline, Evaluation | `feature/agents-langgraph-citations`, `feature/advanced-agents-review-exporter`, `feature/model-training-finetuning` |
| Priyanshu Thakur | Frontend UI, PDF Canvas, Export UI, Auth UI | `feature/frontend-ui-pdf-viewer`, `feature/pdf-canvas-rendering-ui`, `feature/frontend-auth-workspaces` |

---

## Quick Start

### Prerequisites

- Docker Desktop (recommended) or Python 3.10+, Node.js 18+, PostgreSQL 15+ with pgvector extension
- [Ollama](https://ollama.com) installed and running locally

### Pull the LLM

```bash
ollama pull llama3.1:8b-instruct
```

### Docker Compose (Recommended)

```bash
git clone https://github.com/vsviveksolanki2003/ReSearch_Mate.git
cd ReSearch_Mate
cp .env.example .env        # configure DB credentials and JWT secret
docker compose up --build
```

Frontend: http://localhost:5173  
API: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Manual Setup

**Backend:**
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Database:**
```bash
psql -U postgres -c "CREATE DATABASE research_mate;"
psql -U postgres -d research_mate -f backend/app/db/schema.sql
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/papers/upload` | Upload a PDF for processing and indexing |
| `GET` | `/api/papers` | List all indexed papers |
| `POST` | `/api/chat/query` | Submit a research question (returns SSE stream) |
| `POST` | `/api/chat/export` | Export literature review as Markdown or LaTeX |
| `POST` | `/api/auth/register` | Register a new user account |
| `POST` | `/api/auth/login` | Authenticate and receive a JWT token |
| `GET` | `/api/health` | Backend health and DB connectivity check |

---

## Training Pipeline

A 10,000+ sample synthetic academic Q&A dataset is included for LoRA fine-tuning:

```bash
# Generate dataset
python -m backend.app.training.synthetic_dataset

# Configure LoRA (see backend/app/training/lora_trainer.py)
# Requires: pip install peft transformers datasets trl bitsandbytes accelerate
python -m backend.app.training.lora_trainer
```

Dataset format: Llama 3.1 instruct template with system/user/assistant turns and mandatory `[Paper Title, p. N]` citations.

---

## Security

- PDF files validated via magic bytes before processing
- Filenames sanitized (alphanumeric + hyphen/underscore/dot only)
- 50 MB upload size limit enforced
- JWT tokens scoped to individual user workspaces
- All LLM inference runs locally — no data leaves the machine

---

## License

MIT License — see [LICENSE](LICENSE)
