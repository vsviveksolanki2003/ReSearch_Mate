 # 🔬 ReSearch_Mate
# 📚 Agentic AI Research Assistant

**A fully offline, self-hosted research assistant using Retrieval-Augmented Generation (RAG), LangGraph multi-agent workflows, and citation verification.**

## 📌 Overview

**ReSearch_Mate** is an AI-powered research assistant designed to help students, researchers, and academics understand, analyze, and explore research papers more efficiently.

Users can upload research PDFs, ask questions about selected papers, compare multiple papers, identify potential research gaps, and generate structured literature-review outlines.

The system uses locally hosted models and document retrieval to produce evidence-grounded answers with page-level citations. It is designed to run without external AI inference API calls.

ReSearch_Mate combines a local language model, local embeddings, PostgreSQL with pgvector, and specialized agents coordinated by LangGraph. Generated claims are checked against retrieved source text; unsupported claims are rejected.

**The project is under development. Performance figures below are design targets, not measured results.**

## 🎯 Problem Statement

Reading and analyzing research papers is time-consuming, particularly when researchers need to review multiple papers on the same topic.

Researchers must extract methods, datasets, metrics, and findings, compare results, and identify unresolved problems. General-purpose language models can produce unsupported claims or fabricated citations, while sending unpublished or confidential documents to third-party APIs can create privacy and governance concerns.

ReSearch_Mate addresses these challenges through local PDF processing, evidence retrieval, specialized agents, and claim-level citation verification.

## ✨ Key Features

- **Research Paper Upload:** Upload research papers in PDF format.
- **Section- and Page-Aware Processing:** Extract text and retain section labels and page references.
- **Citation-Grounded Question Answering:** Answer questions about selected papers with page-level citations.
- **Hybrid Retrieval:** Combine dense vector similarity with lexical search to retrieve relevant evidence.
- **Multi-Paper Comparison:** Compare methods, datasets, metrics, findings, and limitations in a structured matrix.
- **Research Gap Identification:** Suggest possible gaps, limitations, and future directions for researcher validation.
- **Literature Review Generation:** Generate structured literature-review outlines from analyzed papers.
- **Claim-Level Citation Verification:** Check source quotes, page numbers, and key entities; reject unsupported claims.
- **Multi-Agent Collaboration:** Coordinate retrieval, analysis, comparison, gap identification, and verification agents.
- **Local Model Inference:** Use Ollama to run the language model locally.
- **Privacy-Focused Processing:** Keep document processing and AI inference on locally managed infrastructure.
- **Synchronized PDF Viewer:** Click citation badges to navigate to the cited page.

## 💡 Example Use Case

Imagine a researcher uploads three research papers related to:

> Detection of Fake News Using Machine Learning and Deep Learning.

The researcher asks:

> Compare the methodologies used in these papers and identify the limitations of existing approaches.

ReSearch_Mate retrieves evidence from the selected papers, analyzes the methods and findings, and produces a structured comparison. Claims are checked against source passages and page references before they are shown.

| Research Aspect | Paper 1 | Paper 2 | Paper 3 |
|---|---|---|---|
| Methodology | Extracted from source | Extracted from source | Extracted from source |
| Datasets and metrics | Extracted from source | Extracted from source | Extracted from source |
| Findings | Supported by cited evidence | Supported by cited evidence | Supported by cited evidence |
| Limitations | Reported limitations | Reported limitations | Reported limitations |

*Note: This table is illustrative. Actual comparisons will be generated from uploaded research papers.*

## ⚙️ How It Works

1. **Upload Research Papers:** Upload one or more research PDFs through `POST /papers/upload`.
2. **Document Processing:** PyMuPDF extracts text blocks, page numbers, and section information.
3. **Section-Aware Chunking:** Split text within section boundaries while retaining page references.
4. **Embedding Generation:** Generate local embeddings using `BAAI/bge-small-en-v1.5`.
5. **Vector Storage:** Store chunks and metadata in PostgreSQL with pgvector and an HNSW index.
6. **User Query:** Submit a question through `POST /chat/query` and select the papers to search.
7. **Hybrid Retrieval:** Combine vector similarity and lexical search; restrict results to selected paper IDs.
8. **Multi-Agent Analysis:** Analyze retrieved evidence, compare papers, identify potential gaps, and verify citations.
9. **Local Model Inference:** Generate responses using the Ollama-served `llama3.1:8b-instruct` model.
10. **Response Generation:** Stream verified output to the browser over Server-Sent Events (SSE), with citation badges linked to PDF pages.

## 🤖 Agentic AI Architecture

ReSearch_Mate uses a LangGraph state graph to coordinate specialized agents. Each agent has a defined responsibility and works with retrieved document evidence.

### Specialized Agents

| Agent | Responsibility |
|---|---|
| Retrieval Agent | Retrieves ranked, page-referenced chunks from the selected papers using hybrid search. |
| Analysis Agent | Extracts structured methods, datasets, and findings from retrieved chunks. |
| Comparison Agent | Produces a structured comparison matrix from per-paper summaries. |
| Research Gap Agent | Identifies possible gaps, limitations, and future directions from the comparison. |
| Citation Verifier | Checks claims against source quotes and page references; rejects unsupported claims. |

### Agent Workflow

The workflow uses conditional routing. If the Citation Verifier rejects a claim, control can return to retrieval or analysis for a bounded number of retries. Claims that remain unsupported are dropped rather than displayed. Strict JSON schemas constrain analysis output, and malformed output can trigger repair or retry.

The interface is planned as a split view with chat and comparison results alongside a PDF viewer. Clicking a citation such as `[p. 4]` navigates to the corresponding page.

## 🧠 Model Training and Development

The current report specifies locally deployed models rather than a custom fine-tuning pipeline:

- **Local language model:** Ollama serving `llama3.1:8b-instruct`.
- **Embedding model:** `BAAI/bge-small-en-v1.5` for local vector generation.
- **Inference:** Local execution with no external AI inference API calls.
- **Model evaluation:** Assess retrieval accuracy, citation correctness, hallucination rate, latency, and memory use.

Fine-tuning, larger models, and a cross-encoder reranker are listed as possible future extensions, not as completed or required components of the current design.

## 🛠️ Proposed Technology Stack

### Frontend
- React
- Vite
- Tailwind CSS
- pdfjs-dist

### Backend
- Python
- FastAPI (async)
- REST API and background ingestion
- Server-Sent Events (SSE) for streamed responses

### AI, ML, and NLP
- Ollama
- `llama3.1:8b-instruct`
- `BAAI/bge-small-en-v1.5`

### Agentic AI
- LangGraph
- Retrieval Agent
- Analysis Agent
- Comparison Agent
- Research Gap Agent
- Citation Verifier

### Retrieval-Augmented Generation (RAG)
- Section-aware document chunking
- Dense vector similarity and lexical full-text search
- Ranked-list fusion (e.g., reciprocal rank fusion)
- PostgreSQL with pgvector
- HNSW vector index

### PDF Processing
- PyMuPDF (fitz)

### Database and Storage
- PostgreSQL
- pgvector
- Local PDF/document storage
- Document, chunk, and chat-session metadata

### Deployment and Version Control
- Docker Compose
- Git
- GitHub

**Important:** The system is designed to make zero external AI inference API calls. All model inference and embedding generation are intended to run locally.

## 🗺️ Development Roadmap

### Phase 1: Ingestion Pipeline (Weeks 1–2)
- [ ] Set up FastAPI and PostgreSQL/pgvector.
- [ ] Implement PDF upload and PyMuPDF extraction.
- [ ] Build the upload and PDF viewer interface.
- [ ] Produce embedded, page-referenced chunks.

### Phase 2: Single-Paper RAG (Weeks 3–4)
- [ ] Integrate Ollama and the local embedding model.
- [ ] Implement the SSE query endpoint.
- [ ] Add citation badges and page navigation.
- [ ] Return single-paper answers grounded in specific pages.

### Phase 3: Multi-Agent and Comparison Matrix (Weeks 5–6)
- [ ] Implement the LangGraph workflow and specialized agents.
- [ ] Add the multi-paper comparison matrix UI.
- [ ] Enforce structured JSON schemas.
- [ ] Generate structured comparative analysis.

### Phase 4: Hardening and Packaging (Weeks 7–8)
- [ ] Add hallucination checks and citation verification.
- [ ] Benchmark memory usage.
- [ ] Package offline deployment with Docker Compose.
- [ ] Work toward one-command startup and zero external API calls.

## 🚀 Getting Started

The project is currently under development. Installation and execution instructions will be added once the initial application structure is ready.

### Prerequisites

- Git
- Docker and Docker Compose
- Node.js and npm
- Python
- Sufficient RAM and storage for local models
- GPU with suitable VRAM for faster inference (recommended)

The target resource budget is **16 GB RAM and 8 GB VRAM**. Phase 4 includes benchmarking to confirm resource usage.

## 👥 Team Members

| Name | Responsibility |
|---|---|
| Vivek Solanki | Coordination and integration; API contracts, Pydantic schemas, Docker Compose, and evaluation suite |
| Priyanshu Thakur | Frontend; split-view interface, citation navigation, comparison matrix, and streaming response parser |
| Saksham Mahato | Backend and storage; upload/query endpoints, PostgreSQL schema, and pgvector indexes |
| Grishma Doshi | AI/ML and agent systems; section-aware chunking and LangGraph Retrieval, Analysis, and Citation Verifier agents |

## 🔒 Responsible Use

- Upload only research papers and documents that you have permission to use and process.
- Respect the licenses of models and datasets.
- Verify important findings against original research papers.
- Treat suggested research gaps as hypotheses to validate, not established facts.
- Distinguish extracted evidence from AI-generated interpretation.
- Protect locally stored documents, model files, and credentials.
- Remember that the tool assists research and does not replace critical reading or proper attribution.

## 📊 Evaluation Plan

The planned evaluation suite contains 50 test queries covering factual questions, numeric lookups, multi-paper comparisons, and unanswerable questions.

| Metric | Definition | Design Target |
|---|---|---:|
| Retrieval accuracy (Recall@5) | Gold evidence chunk appears in top five results | ≥ 85% |
| Citation precision | Verified citations whose quote supports the claim | ≥ 95% |
| Hallucination rate | Unsupported claims shown / total claims | ≤ 5% |
| Vector search latency | HNSW query time | < 100 ms |
| Peak memory | Full stack under load | ≤ 16 GB RAM, ≤ 8 GB VRAM |
| External API calls | Third-party network calls | 0 |

*These are design targets, not measured results. Planned baselines include a no-retrieval LLM and RAG without the verifier.*

## 🤝 Contributing

We welcome contributions from our team members and other developers.

1. Clone the repository.
2. Create a separate branch for your feature or fix.
3. Implement and test your changes.
4. Commit and push your changes.
5. Open a Pull Request for review before merging into the main branch.

Please follow consistent coding practices, document important changes, and never commit secrets or credentials.

## 📄 License

The project's license will be decided before public distribution.

---

### 🎯 Our Mission

**To make academic research smarter, faster, and more reliable through local AI, intelligent document retrieval, and evidence-based multi-agent research assistance.**
