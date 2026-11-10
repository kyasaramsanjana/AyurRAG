from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class BookBase(BaseModel):
    title: str
    author: Optional[str] = "Ancient Acharya"
    category: Optional[str] = "Classical Ayurvedic Treatise"
    total_pages: Optional[int] = 1

class BookCreate(BookBase):
    pass

class BookSchema(BookBase):
    id: str
    total_chunks: int = 0
    created_at: Any

    class Config:
        from_attributes = True

class ChunkSchema(BaseModel):
    id: str
    book_id: str
    book_title: str
    chapter: str
    page_number: int
    chunk_index: int
    text: str
    score: Optional[float] = None
    rank_dense: Optional[int] = None
    rank_sparse: Optional[int] = None
    rrf_score: Optional[float] = None

    class Config:
        from_attributes = True

class CitationItem(BaseModel):
    chunk_id: str
    book_title: str
    chapter: str
    page_number: int
    chunk_index: int
    excerpt: str

class RemedyItem(BaseModel):
    title: str
    source_book: str
    ingredients: List[str]
    method: str
    indications: str

class ComparisonItem(BaseModel):
    aspect: str
    charaka_samhita: str
    sushruta_samhita: str
    ashtanga_hridaya: str
    bhavaprakasha_nighantu: str

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=2, description="Natural language Ayurvedic question")
    top_k: int = Field(default=5, ge=1, le=20)
    enable_llm_synthesis: bool = True

class QueryResponse(BaseModel):
    query: str
    answer_text: str
    remedies: List[RemedyItem] = []
    key_takeaways: List[str] = []
    comparisons: List[ComparisonItem] = []
    citations: List[CitationItem] = []
    retrieved_passages: List[ChunkSchema] = []
    model_used: str = "Gemini 1.5 Flash (with Classical Extractive RAG Fallback)"
    retrieval_method: str = "Hybrid Dense (pgvector/bge-base-en-v1.5) + Sparse (FTS/Lexical) + RRF"
    stats: Dict[str, Any] = {}

class RawSearchRequest(BaseModel):
    query: str
    mode: str = "hybrid" # "hybrid", "dense", "sparse"
    top_k: int = 5

class RawSearchResponse(BaseModel):
    query: str
    mode: str
    results: List[ChunkSchema]
    total_found: int

class UploadResponse(BaseModel):
    book_id: str
    title: str
    author: Optional[str]
    pages_processed: int
    chunks_created: int
    status: str
