-- AyurRAG: Cross-Textual Ayurvedic Knowledge Retrieval and Analysis System
-- PostgreSQL + pgvector schema definition per Project Architecture (Slide 21)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- Books table: maintains corpus provenance
CREATE TABLE IF NOT EXISTS books (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    category VARCHAR(100) DEFAULT 'Classical Ayurvedic Treatise',
    total_pages INTEGER DEFAULT 1,
    total_chunks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Text Chunks table: maintains chunk, page, chapter & 768-d vector embedding
CREATE TABLE IF NOT EXISTS text_chunks (
    id VARCHAR(36) PRIMARY KEY,
    book_id VARCHAR(36) REFERENCES books(id) ON DELETE CASCADE,
    book_title VARCHAR(255) NOT NULL,
    chapter VARCHAR(255) DEFAULT 'General Treatise',
    page_number INTEGER DEFAULT 1,
    chunk_index INTEGER DEFAULT 0,
    text TEXT NOT NULL,
    embedding vector(768), -- BAAI/bge-base-en-v1.5 768-d dense vector
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Dense & Sparse Hybrid Search (Slide 11)
CREATE INDEX IF NOT EXISTS idx_chunks_book_id ON text_chunks(book_id);
CREATE INDEX IF NOT EXISTS idx_chunks_chapter ON text_chunks(chapter);
CREATE INDEX IF NOT EXISTS idx_chunks_page ON text_chunks(page_number);

-- Full-Text Search (Sparse Lexical) Index
CREATE INDEX IF NOT EXISTS idx_chunks_fts ON text_chunks USING gin(to_tsvector('english', text));

-- Cosine Distance HNSW Index for Dense Vector Retrieval
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_cosine ON text_chunks USING hnsw (embedding vector_cosine_ops);
