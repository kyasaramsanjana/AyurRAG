import math
import re
from typing import List, Dict, Any, Tuple
from app.services.embedding import embedding_service
from app.config import settings

class HybridRetriever:
    """
    Hybrid Retrieval and Reciprocal Rank Fusion (RRF) Service
    as specified in PPT Slide 11, 21, and 23.
    """

    def __init__(self, rrf_k: int = settings.RRF_K):
        self.rrf_k = rrf_k

    def dense_search(self, query_text: str, chunks: List[Any], top_k: int = 15) -> List[Tuple[Any, float, int]]:
        """
        Dense vector search using cosine distance with BAAI/bge-base-en-v1.5 embeddings.
        Returns list of (chunk, similarity_score, rank).
        """
        query_vec = embedding_service.embed_text(query_text)
        scored = []
        for ch in chunks:
            ch_vec = ch.embedding
            if ch_vec:
                sim = embedding_service.cosine_similarity(query_vec, ch_vec)
            else:
                sim = 0.0
            scored.append((ch, sim))

        # Sort descending by cosine similarity
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Assign 1-based ranks
        results = []
        for rank, (ch, score) in enumerate(scored[:top_k], start=1):
            results.append((ch, score, rank))
        return results

    def sparse_search(self, query_text: str, chunks: List[Any], top_k: int = 15) -> List[Tuple[Any, float, int]]:
        """
        Sparse / Lexical full-text search favoring exact terms, Sanskrit names,
        and keyword overlap per Slide 11.
        Returns list of (chunk, lexical_score, rank).
        """
        terms = re.findall(r'\b[a-zA-Z0-9_-]{2,}\b', query_text.lower())
        if not terms:
            return [(ch, 0.0, idx + 1) for idx, ch in enumerate(chunks[:top_k])]

        # Calculate IDF-like weights for terms across corpus
        doc_count = len(chunks) or 1
        doc_freqs = {term: 0 for term in terms}
        for ch in chunks:
            text_lower = ch.text.lower()
            for term in terms:
                if term in text_lower:
                    doc_freqs[term] += 1

        scored = []
        for ch in chunks:
            text_lower = ch.text.lower()
            chapter_lower = (ch.chapter or "").lower()
            book_lower = (ch.book_title or "").lower()
            
            score = 0.0
            for term in terms:
                # Term frequency
                tf = text_lower.count(term)
                if tf > 0:
                    df = doc_freqs.get(term, 1)
                    idf = math.log((doc_count + 1) / (df + 1)) + 1.0
                    score += (tf / (tf + 1.5)) * idf

                # Chapter / title bonus
                if term in chapter_lower:
                    score += 1.5
                if term in book_lower:
                    score += 0.8

            scored.append((ch, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for rank, (ch, score) in enumerate(scored[:top_k], start=1):
            results.append((ch, score, rank))
        return results

    def reciprocal_rank_fusion(
        self,
        dense_results: List[Tuple[Any, float, int]],
        sparse_results: List[Tuple[Any, float, int]],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Combines dense and sparse ranked lists using Cormack et al. (2009) RRF:
        RRF_score(d) = sum(1 / (k + rank_i))
        """
        rrf_scores: Dict[str, float] = {}
        chunk_map: Dict[str, Any] = {}
        dense_rank_map: Dict[str, int] = {}
        sparse_rank_map: Dict[str, int] = {}
        cosine_score_map: Dict[str, float] = {}

        for ch, sim, rank in dense_results:
            cid = ch.id
            chunk_map[cid] = ch
            dense_rank_map[cid] = rank
            cosine_score_map[cid] = sim
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        for ch, lex, rank in sparse_results:
            cid = ch.id
            chunk_map[cid] = ch
            sparse_rank_map[cid] = rank
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (1.0 / (self.rrf_k + rank))

        # Sort all chunks by RRF score descending
        sorted_cids = sorted(rrf_scores.keys(), key=lambda cid: rrf_scores[cid], reverse=True)

        # Slide 23: "Return a bounded set of chunks, initially favoring distinct books where possible"
        selected = []
        seen_books = set()
        deferred = []

        for cid in sorted_cids:
            ch = chunk_map[cid]
            item = {
                "chunk": ch,
                "rrf_score": round(rrf_scores[cid], 5),
                "rank_dense": dense_rank_map.get(cid),
                "rank_sparse": sparse_rank_map.get(cid),
                "cosine_similarity": round(cosine_score_map.get(cid, 0.0), 4)
            }
            if ch.book_title not in seen_books and len(selected) < top_k:
                seen_books.add(ch.book_title)
                selected.append(item)
            else:
                deferred.append(item)

        # Fill remaining slots with top deferred items
        while len(selected) < top_k and deferred:
            selected.append(deferred.pop(0))

        return selected

retriever = HybridRetriever()
