-- PostgreSQL + pgvector schema definition for ReSearch_Mate
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Papers table
CREATE TABLE IF NOT EXISTS papers (
    id VARCHAR(64) PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT[] DEFAULT '{}',
    publication_year INT,
    abstract TEXT,
    total_pages INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Chunks table with pgvector embeddings
CREATE TABLE IF NOT EXISTS chunks (
    id VARCHAR(128) PRIMARY KEY,
    paper_id VARCHAR(64) REFERENCES papers(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    page_number INT NOT NULL,
    section_title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    token_count INT,
    embedding vector(384),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- HNSW index for sub-millisecond approximate nearest neighbor search
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw
ON chunks USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- B-Tree index on paper_id and page_number
CREATE INDEX IF NOT EXISTS idx_chunks_paper_page
ON chunks (paper_id, page_number);
