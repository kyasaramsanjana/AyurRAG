import time
import uuid
import logging
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db, init_engine, ACTIVE_DIALECT
from app.models import Book, TextChunk
from app.schemas import (
    QueryRequest, QueryResponse,
    RawSearchRequest, RawSearchResponse,
    BookSchema, ChunkSchema, UploadResponse
)
from app.services.embedding import embedding_service
from app.services.chunker import chunker
from app.services.parser import parser
from app.services.retrieval import retriever
from app.services.synthesis import synthesis_service
from app.data.seed_corpus import SEED_BOOKS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ayurrag.api")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Cross-Textual Ayurvedic Knowledge Retrieval and Analysis System (AyurRAG) REST API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_engine()
    # Auto-seed if database is empty
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        count = db.query(Book).count()
        if count == 0:
            logger.info("Empty database detected. Seeding foundational classical Ayurvedic treatises...")
            seed_database_internal(db)
    finally:
        db.close()

def seed_database_internal(db: Session):
    for b_data in SEED_BOOKS:
        existing = db.query(Book).filter(Book.title == b_data["title"]).first()
        if existing:
            continue
        book_id = str(uuid.uuid4())
        book = Book(
            id=book_id,
            title=b_data["title"],
            author=b_data.get("author", "Ancient Sage"),
            category=b_data.get("category", "Classical Treatise"),
            total_pages=b_data.get("total_pages", len(b_data["passages"])),
            total_chunks=len(b_data["passages"])
        )
        db.add(book)
        db.flush()

        for idx, pas in enumerate(b_data["passages"]):
            emb = embedding_service.embed_text(pas["text"])
            chunk = TextChunk(
                id=str(uuid.uuid4()),
                book_id=book_id,
                book_title=b_data["title"],
                chapter=pas.get("chapter", "General Section"),
                page_number=pas.get("page_number", idx + 1),
                chunk_index=idx,
                text=pas["text"]
            )
            chunk.embedding = emb
            db.add(chunk)
    db.commit()

@app.get("/")
def root():
    return {
        "system": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
        "endpoints": {
            "query": "/api/query",
            "search": "/api/search",
            "books": "/api/books",
            "seed": "/api/seed",
            "upload": "/api/upload",
            "health": "/api/health"
        }
    }

@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    book_count = db.query(Book).count()
    chunk_count = db.query(TextChunk).count()
    return {
        "status": "healthy",
        "dialect": ACTIVE_DIALECT,
        "embedding_model": settings.EMBEDDING_MODEL_NAME,
        "embedding_dimension": settings.EMBEDDING_DIM,
        "total_books": book_count,
        "total_chunks": chunk_count,
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

@app.post("/api/seed")
def seed_corpus(db: Session = Depends(get_db)):
    seed_database_internal(db)
    book_count = db.query(Book).count()
    chunk_count = db.query(TextChunk).count()
    return {
        "message": "Classical Ayurvedic Seed Corpus successfully indexed.",
        "books_total": book_count,
        "chunks_total": chunk_count
    }

@app.get("/api/books", response_model=List[BookSchema])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.get("/api/books/{book_id}/chunks", response_model=List[ChunkSchema])
def get_book_chunks(
    book_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    chunks = db.query(TextChunk).filter(TextChunk.book_id == book_id).offset(offset).limit(limit).all()
    return chunks

@app.post("/api/query", response_model=QueryResponse)
def execute_query(req: QueryRequest, db: Session = Depends(get_db)):
    t0 = time.time()
    all_chunks = db.query(TextChunk).all()
    if not all_chunks:
        raise HTTPException(status_code=400, detail="Corpus is empty. Please run /api/seed or upload documents.")

    # 1. Dense retrieval (Cosine distance over BGE embeddings)
    dense_ranked = retriever.dense_search(req.query, all_chunks, top_k=15)
    
    # 2. Sparse retrieval (Lexical FTS & term overlap)
    sparse_ranked = retriever.sparse_search(req.query, all_chunks, top_k=15)

    # 3. Reciprocal Rank Fusion (RRF)
    fused_results = retriever.reciprocal_rank_fusion(dense_ranked, sparse_ranked, top_k=req.top_k)

    # 4. Synthesis Service (Gemini or Classical Extractive Fallback)
    synth = synthesis_service.synthesize(req.query, fused_results)

    # Prepare response chunks
    retrieved_schemas = []
    for it in fused_results:
        ch = it["chunk"]
        retrieved_schemas.append(ChunkSchema(
            id=ch.id,
            book_id=ch.book_id,
            book_title=ch.book_title,
            chapter=ch.chapter,
            page_number=ch.page_number,
            chunk_index=ch.chunk_index,
            text=ch.text,
            score=it.get("cosine_similarity"),
            rank_dense=it.get("rank_dense"),
            rank_sparse=it.get("rank_sparse"),
            rrf_score=it.get("rrf_score")
        ))

    elapsed = round((time.time() - t0) * 1000, 2)

    return QueryResponse(
        query=req.query,
        answer_text=synth["answer_text"],
        remedies=synth.get("remedies", []),
        key_takeaways=synth.get("key_takeaways", []),
        comparisons=synth.get("comparisons", []),
        citations=synth.get("citations", []),
        retrieved_passages=retrieved_schemas,
        model_used=synth.get("model_used", "AyurRAG Synthesis Engine"),
        retrieval_method=f"Hybrid Dense (pgvector/bge-base-en-v1.5) + Sparse (FTS/Lexical) + RRF (k={settings.RRF_K})",
        stats={
            "latency_ms": elapsed,
            "dense_candidates": len(dense_ranked),
            "sparse_candidates": len(sparse_ranked),
            "total_corpus_chunks": len(all_chunks)
        }
    )

@app.post("/api/search", response_model=RawSearchResponse)
def raw_search(req: RawSearchRequest, db: Session = Depends(get_db)):
    all_chunks = db.query(TextChunk).all()
    if not all_chunks:
        return RawSearchResponse(query=req.query, mode=req.mode, results=[], total_found=0)

    if req.mode == "dense":
        dense = retriever.dense_search(req.query, all_chunks, top_k=req.top_k)
        results = [
            ChunkSchema(
                id=ch.id, book_id=ch.book_id, book_title=ch.book_title,
                chapter=ch.chapter, page_number=ch.page_number, chunk_index=ch.chunk_index,
                text=ch.text, score=score, rank_dense=rank
            )
            for ch, score, rank in dense
        ]
    elif req.mode == "sparse":
        sparse = retriever.sparse_search(req.query, all_chunks, top_k=req.top_k)
        results = [
            ChunkSchema(
                id=ch.id, book_id=ch.book_id, book_title=ch.book_title,
                chapter=ch.chapter, page_number=ch.page_number, chunk_index=ch.chunk_index,
                text=ch.text, score=score, rank_sparse=rank
            )
            for ch, score, rank in sparse
        ]
    else: # hybrid
        dense = retriever.dense_search(req.query, all_chunks, top_k=15)
        sparse = retriever.sparse_search(req.query, all_chunks, top_k=15)
        fused = retriever.reciprocal_rank_fusion(dense, sparse, top_k=req.top_k)
        results = [
            ChunkSchema(
                id=it["chunk"].id, book_id=it["chunk"].book_id, book_title=it["chunk"].book_title,
                chapter=it["chunk"].chapter, page_number=it["chunk"].page_number,
                chunk_index=it["chunk"].chunk_index, text=it["chunk"].text,
                score=it.get("cosine_similarity"), rank_dense=it.get("rank_dense"),
                rank_sparse=it.get("rank_sparse"), rrf_score=it.get("rrf_score")
            )
            for it in fused
        ]

    return RawSearchResponse(
        query=req.query,
        mode=req.mode,
        results=results,
        total_found=len(results)
    )

@app.post("/api/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: Optional[str] = Form("Ancient Scholar"),
    category: Optional[str] = Form("Ayurvedic Literature"),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        pages = parser.parse_pdf(contents)
    else:
        text_content = contents.decode("utf-8", errors="ignore")
        pages = parser.parse_text(text_content)

    if not pages:
        raise HTTPException(status_code=400, detail="Could not extract text from the provided document.")

    chunks_data = chunker.chunk_pages(pages)
    if not chunks_data:
        raise HTTPException(status_code=400, detail="Document produced 0 word-bounded chunks.")

    book_id = str(uuid.uuid4())
    book = Book(
        id=book_id,
        title=title,
        author=author,
        category=category,
        total_pages=len(pages),
        total_chunks=len(chunks_data)
    )
    db.add(book)
    db.flush()

    for ch_item in chunks_data:
        emb = embedding_service.embed_text(ch_item["text"])
        chunk = TextChunk(
            id=str(uuid.uuid4()),
            book_id=book_id,
            book_title=title,
            chapter=ch_item["chapter"],
            page_number=ch_item["page_number"],
            chunk_index=ch_item["chunk_index"],
            text=ch_item["text"]
        )
        chunk.embedding = emb
        db.add(chunk)

    db.commit()

    return UploadResponse(
        book_id=book_id,
        title=title,
        author=author,
        pages_processed=len(pages),
        chunks_created=len(chunks_data),
        status="Document successfully parsed, chunked, and embedded into AyurRAG."
    )

@app.delete("/api/books/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": f"Book '{book.title}' and all associated chunks deleted."}
