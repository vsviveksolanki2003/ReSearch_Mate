 
# 🔬 ReSearch_Mate

### Your AI-Powered Companion for Academic Research

**ReSearch_Mate** is a locally deployable, AI-powered multi-paper academic research assistant designed to simplify literature reviews, research paper analysis, and citation verification.

It helps researchers, students, and academics explore multiple research papers, extract relevant information, compare methodologies, identify research gaps, and generate citation-supported answers.

Instead of manually searching through lengthy PDFs, users can ask questions in natural language and receive context-aware responses grounded in their uploaded research documents.

The system combines **Agentic AI, Retrieval-Augmented Generation (RAG), Semantic Search, and Local Large Language Models (LLMs)** to provide an intelligent, privacy-focused research environment.

---

## 🎯 Project Objectives

- Simplify academic literature reviews using AI.
- Enable question-answering across multiple research papers.
- Extract methodologies, datasets, results, and evaluation metrics.
- Compare research findings across different publications.
- Identify research gaps and possible future research directions.
- Reduce hallucinations through citation verification.
- Provide a locally running research assistant without external LLM APIs.

---

## ✨ Key Features

### 📄 1. Multi-Paper Question Answering
Upload multiple academic research papers and ask questions across them using natural language.

### 🔍 2. Semantic Information Retrieval
Retrieve relevant information using vector embeddings instead of relying only on keyword matching.

### 📊 3. Research Paper Comparison
Compare multiple papers based on:
- Research objectives
- Methodologies
- Datasets
- Experimental results
- Evaluation metrics
- Limitations

### 🧠 4. Research Gap Identification
Analyze existing publications to identify methodological differences, unresolved problems, and potential research opportunities.

### ✅ 5. Citation Verification
Verify generated claims and quotations against the original research papers using page numbers and source text.

### 🔒 6. Local AI Processing
Run AI models locally using Ollama, reducing dependency on commercial LLM APIs and protecting confidential documents.

### 📑 7. Interactive PDF Viewer
View research papers alongside AI-generated responses and navigate directly to referenced PDF pages.

---

## ⚙️ How It Works

**Step 1: Upload Research Papers**

Users upload one or multiple academic research papers in PDF format.

**Step 2: Document Processing**

PyMuPDF extracts text, identifies document sections, and preserves page information.

**Step 3: Text Chunking**

Extracted content is divided into section-aware text chunks while maintaining contextual information.

**Step 4: Embedding Generation**

The BAAI/bge-small-en-v1.5 model converts text chunks into 384-dimensional semantic embeddings.

**Step 5: Vector Storage**

Embeddings are stored in PostgreSQL using pgvector for efficient similarity search.

**Step 6: Query Processing**

Users submit research questions. LangGraph coordinates specialized agents to retrieve and analyze relevant information.

**Step 7: Citation Verification**

Generated claims are checked against the original source documents before being presented.

**Step 8: Result Presentation**

Users receive context-aware answers with citations and references to the uploaded research papers.

---

## 🏗️ System Architecture

```text
                 Academic Research Papers
                           |
                           v
                     PDF Upload
                           |
                           v
                    PyMuPDF Parser
                           |
                           v
                 Section-Aware Chunking
                           |
                           v
                  Embedding Generation
                  BGE-small-en-v1.5
                           |
                           v
                 PostgreSQL + pgvector
                           |
                           v
                      User Query
                           |
                           v
                  LangGraph Intent Router
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
        Retrieval      Structured     Comparison
          Agent         Analysis        Agent
                         Agent
             |             |             |
             +-------------+-------------+
                           |
                           v
                   Local LLM (Ollama)
                           |
                           v
                    Citation Verifier
                           |
                           v
                   Verified Response
                           |
                           v
                  React Split-View UI
                           |
                           v
                Answer + PDF References
```

---

## 🤖 Multi-Agent AI Workflow

ReSearch_Mate uses **LangGraph** to coordinate specialized agents for academic research tasks.

| Agent | Responsibility |
|-------|----------------|
| Intent Router | Identifies the type of research query |
| Retrieval Agent | Retrieves relevant information from uploaded papers |
| Structured Analysis Agent | Extracts objectives, methodologies, datasets, and metrics |
| Comparison Matrix Agent | Compares findings across multiple research papers |
| Citation Verifier | Validates generated quotations and source references |

### Agent Workflow

1. The Intent Router analyzes the user's question.
2. The Retrieval Agent searches relevant document chunks.
3. The Structured Analysis Agent extracts important research information.
4. The Comparison Matrix Agent compares papers when required.
5. The local language model generates a response.
6. The Citation Verifier checks claims against source documents.
7. The verified response is displayed with references.

---

## 🛠️ Technology Stack

| Component | Technologies |
|-----------|--------------|
| Frontend | React, Vite, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI |
| Language Model | Llama 3.1 8B Instruct |
| Local LLM Engine | Ollama |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Database | PostgreSQL 16 |
| Vector Database Extension | pgvector |
| Vector Search | HNSW |
| PDF Processing | PyMuPDF |
| Agent Framework | LangGraph |
| PDF Viewer | PDF.js (pdfjs-dist) |
| Communication | REST APIs, Server-Sent Events |
| Deployment | Docker, Docker Compose |

---

## 🧩 Core System Modules

| Module | Function |
|--------|----------|
| pdf_parser.py | Extracts PDF text, headings, and page information |
| chunker.py | Performs section-aware text chunking |
| embeddings.py | Generates semantic vector embeddings |
| vector_store.py | Stores and retrieves embeddings using pgvector |
| agent/graph.py | Coordinates the multi-agent workflow |
| agent/analyzer.py | Extracts structured research information |
| agent/comparator.py | Generates cross-paper comparisons |
| agent/verifier.py | Verifies citations and source quotations |
| api/routes.py | Handles API requests and responses |
| ui/PdfViewer.tsx | Displays PDFs and supports citation navigation |

---

## 📈 Performance Evaluation

The research report evaluates ReSearch_Mate using **50 academic queries across 10 computer science research publications**.

### Evaluation Results

| Evaluation Metric | Result |
|-------------------|--------|
| Top-1 Retrieval Accuracy | 92.0% |
| Top-3 Retrieval Accuracy | 98.0% |
| Citation Verification Precision | 100.0% |
| Vector Search Latency | 14.2 ms |
| End-to-End Query Latency | 1.84 seconds |

### Evaluation Dataset

| Parameter | Value |
|-----------|-------|
| Research Papers | 10 |
| Total Pages | 1,420 |
| Total Text Chunks | 4,890 |
| Evaluation Queries | 50 |
| Average Chunk Length | 312 tokens |

### Retrieval Comparison

| Method | Top-1 Accuracy | Top-3 Accuracy |
|--------|----------------|----------------|
| Keyword Search (Grep) | 38.0% | 52.0% |
| BM25 Lexical Search | 54.0% | 72.0% |
| Dense BGE + pgvector | 92.0% | 98.0% |
| ReSearch_Mate | 92.0% | 98.0% |

*These evaluation results are reported in the project's IEEE research document.*

---

## 🔐 Privacy and Security

ReSearch_Mate follows an **offline-first, local AI architecture**.

- Research papers are processed locally.
- Embeddings are generated using a locally hosted model.
- PostgreSQL stores document information and vector embeddings.
- Ollama runs the language model locally.
- External commercial LLM APIs are not required.
- Confidential research documents can remain within the local environment.

This makes the application suitable for academic research involving unpublished papers and confidential documents.

---

## 💡 Applications

### Academic Literature Review
Analyze multiple research publications and summarize their important findings.

### Research Paper Comparison
Compare methodologies, datasets, experimental results, and limitations.

### Research Gap Discovery
Identify unresolved challenges and possible future research directions.

### Research Assistance
Ask questions about uploaded papers and receive citation-supported answers.

### Confidential Research
Process unpublished academic documents without sending them to external LLM services.

---

## ⚠️ Limitations

- Complex mathematical equations and image-based tables may not be fully extracted.
- Comparing a large number of papers simultaneously may exceed the local model's context window.
- CPU-only inference may result in slower response generation.
- Performance depends on available hardware resources.

---

## 🚀 Future Scope

- Integrate advanced domain-specific embedding models such as SPECTER and SciBERT.
- Improve extraction of figures, mathematical equations, and complex tables.
- Support automated literature review generation.
- Introduce persistent citation relationship graphs using Neo4j.
- Add BibTeX and LaTeX citation export.
- Improve research gap identification.
- Support larger research paper collections.
- Enhance multi-agent collaboration and reasoning.

---

## 👨‍💻 Team Members

- **Vivek Solanki**
- **Priyanshu Thakur**
- **Saksham Mahato**
- **Grishma Doshi**

---

## 🔗 Project Repository

[ReSearch_Mate on GitHub](https://github.com/vsviveksolanki2003/ReSearch_Mate)

---

## 📜 License

This project is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

### ⭐ Support

If you find ReSearch_Mate useful, consider giving the repository a star!

**ReSearch_Mate — Making Academic Research Smarter, Faster, and More Reliable.**
