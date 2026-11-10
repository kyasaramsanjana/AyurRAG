import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "AyurRAG - Cross-Textual Ayurvedic Knowledge Retrieval"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Database
    # Primary: PostgreSQL + pgvector (per PPT Slide 4, 12, 21)
    POSTGRES_URL: str = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres@localhost:5432/ayurrag")
    # Fallback to local SQLite if PostgreSQL is not active
    # On Vercel serverless environment, write to /tmp
    SQLITE_DB_PATH: str = os.getenv(
        "SQLITE_DB_PATH",
        "/tmp/ayurrag_local.db" if (os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME")) else "ayurrag_local.db"
    )
    USE_SQLITE_FALLBACK: bool = True
    
    # Embeddings: BAAI/bge-base-en-v1.5 (768 dimensions) (per PPT Slide 10, 21)
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-base-en-v1.5"
    EMBEDDING_DIM: int = 768
    
    # Retrieval
    RRF_K: int = 60              # Reciprocal Rank Fusion constant (PPT Slide 11)
    DEFAULT_TOP_K: int = 5       # Max context chunks (PPT Slide 20, 23)
    
    # LLM Synthesis (Gemini API with fallback per PPT Slide 4, 21, 23)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

settings = Settings()
