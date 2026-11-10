import datetime
import uuid
import json
from typing import List
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    author = Column(String(255), nullable=True)
    category = Column(String(100), default="Classical Ayurvedic Treatise")
    total_pages = Column(Integer, default=1)
    total_chunks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    chunks = relationship("TextChunk", back_populates="book", cascade="all, delete-orphan")

class TextChunk(Base):
    __tablename__ = "text_chunks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id = Column(String(36), ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    book_title = Column(String(255), nullable=False)
    chapter = Column(String(255), default="General Treatise", index=True)
    page_number = Column(Integer, default=1, index=True)
    chunk_index = Column(Integer, default=0)
    text = Column(Text, nullable=False)
    
    # Stored as serialized 768-d float array (compatible with both PostgreSQL pgvector and SQLite)
    embedding_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    book = relationship("Book", back_populates="chunks")

    @property
    def embedding(self) -> List[float]:
        if self.embedding_json:
            return json.loads(self.embedding_json)
        return []

    @embedding.setter
    def embedding(self, val: List[float]):
        self.embedding_json = json.dumps(val)
