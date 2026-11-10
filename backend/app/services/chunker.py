import re
from typing import List, Dict, Any

class WordBoundedChunker:
    """
    Provenance-aware chunker per Slide 16 & 22:
    Splits document pages into word-bounded chunks with overlap,
    retaining book, page, chapter, and chunk-index metadata.
    """
    def __init__(self, target_words: int = 180, overlap_words: int = 40):
        self.target_words = target_words
        self.overlap_words = overlap_words

    def chunk_pages(self, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Input: list of page dicts: [{'page_number': 1, 'chapter': 'Sutra Sthana Ch. 1', 'text': '...'}]
        Output: list of chunk dicts
        """
        all_chunks = []
        global_chunk_idx = 0

        for page_data in pages:
            page_num = page_data.get("page_number", 1)
            chapter = page_data.get("chapter", "General Section")
            text = page_data.get("text", "").strip()

            if not text:
                continue

            words = text.split()
            if len(words) <= self.target_words:
                all_chunks.append({
                    "chunk_index": global_chunk_idx,
                    "page_number": page_num,
                    "chapter": chapter,
                    "text": text,
                    "word_count": len(words)
                })
                global_chunk_idx += 1
            else:
                step = self.target_words - self.overlap_words
                if step <= 0:
                    step = self.target_words // 2

                start = 0
                while start < len(words):
                    end = min(start + self.target_words, len(words))
                    chunk_text = " ".join(words[start:end])
                    
                    all_chunks.append({
                        "chunk_index": global_chunk_idx,
                        "page_number": page_num,
                        "chapter": chapter,
                        "text": chunk_text,
                        "word_count": end - start
                    })
                    global_chunk_idx += 1

                    if end == len(words):
                        break
                    start += step

        return all_chunks

chunker = WordBoundedChunker()
