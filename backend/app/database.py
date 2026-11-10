import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base

logger = logging.getLogger("ayurrag.database")

DATABASE_ENGINE = None
_session_factory = None
ACTIVE_DIALECT = "sqlite"

def init_engine():
    global DATABASE_ENGINE, _session_factory, ACTIVE_DIALECT
    
    # Try PostgreSQL first (Slide 12, 21: PostgreSQL + pgvector)
    try:
        pg_engine = create_engine(settings.POSTGRES_URL, connect_args={"connect_timeout": 3})
        with pg_engine.connect() as conn:
            pass
        DATABASE_ENGINE = pg_engine
        ACTIVE_DIALECT = "postgresql"
        logger.info("Connected successfully to PostgreSQL + pgvector database.")
    except Exception as e:
        if settings.USE_SQLITE_FALLBACK:
            logger.warning(f"PostgreSQL not reachable ({e}). Engaging automatic SQLite local storage fallback.")
            sqlite_url = f"sqlite:///{settings.SQLITE_DB_PATH}"
            DATABASE_ENGINE = create_engine(sqlite_url, connect_args={"check_same_thread": False})
            ACTIVE_DIALECT = "sqlite"
        else:
            raise e

    _session_factory = sessionmaker(autocommit=False, autoflush=False, bind=DATABASE_ENGINE)
    Base.metadata.create_all(bind=DATABASE_ENGINE)

def SessionLocal():
    global _session_factory
    if _session_factory is None:
        init_engine()
    return _session_factory()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Generates PostgreSQL + pgvector DDL for evaluation / submission documentation
POSTGRES_PGVECTOR_DDL = """-- AyurRAG: Cross-Textual Ayurvedic Knowledge Retrieval and Analysis System
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
"""

try:
    with open("schema_postgres_pgvector.sql", "w", encoding="utf-8") as f:
        f.write(POSTGRES_PGVECTOR_DDL)
except Exception:
    pass
