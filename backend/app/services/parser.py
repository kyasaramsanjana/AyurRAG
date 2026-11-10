import re
import io
from typing import List, Dict, Any
from pypdf import PdfReader

class DocumentParser:
    """
    Document Parser for AyurRAG (PPT Slide 21 & 22):
    Parses PDF, TXT, and Markdown files while extracting text page-by-page
    and carrying detected chapter context forward.
    """
    
    CHAPTER_PATTERNS = [
        re.compile(r'(?:Chapter|Adhyaya)\s+(\d+[:\.\s\-]+[^\n\r]+)', re.IGNORECASE),
        re.compile(r'((?:Sutra|Chikitsa|Sharira|Nidana|Kalpa|Siddhi|Uttara)\s+Sthana[^\n\r]*)', re.IGNORECASE),
        re.compile(r'(?:Varga|Khanda|Prakarana)\s+(\d+[:\.\s\-]+[^\n\r]+)', re.IGNORECASE),
        re.compile(r'^[#]{1,3}\s+([^\n\r]+)', re.MULTILINE),
        re.compile(r'([A-Z\s]{4,30}\s+(?:CHAPTER|SECTION|TREATISE))', re.IGNORECASE)
    ]

    def parse_pdf(self, file_bytes: bytes) -> List[Dict[str, Any]]:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages_data = []
        current_chapter = "Introductory Chapter"

        for page_idx, page in enumerate(reader.pages):
            page_num = page_idx + 1
            extracted_text = page.extract_text() or ""
            
            # Detect chapter
            detected = self._detect_chapter(extracted_text)
            if detected:
                current_chapter = detected

            pages_data.append({
                "page_number": page_num,
                "chapter": current_chapter,
                "text": extracted_text.strip()
            })

        return pages_data

    def parse_text(self, text_content: str, words_per_page: int = 350) -> List[Dict[str, Any]]:
        """
        Parses raw TXT or Markdown by segmenting into approximate pages
        and detecting chapter landmarks.
        """
        lines = text_content.splitlines()
        pages_data = []
        current_chapter = "General Treatise"
        
        current_page_words = []
        page_num = 1

        for line in lines:
            stripped = line.strip()
            # Check for chapter marker in line
            detected = self._detect_chapter(stripped)
            if detected:
                current_chapter = detected

            words = stripped.split()
            current_page_words.extend(words)

            if len(current_page_words) >= words_per_page:
                pages_data.append({
                    "page_number": page_num,
                    "chapter": current_chapter,
                    "text": " ".join(current_page_words)
                })
                page_num += 1
                current_page_words = []

        if current_page_words:
            pages_data.append({
                "page_number": page_num,
                "chapter": current_chapter,
                "text": " ".join(current_page_words)
            })

        return pages_data

    def _detect_chapter(self, text_snippet: str) -> str:
        for pat in self.CHAPTER_PATTERNS:
            match = pat.search(text_snippet)
            if match:
                ch_title = match.group(1).strip()
                # Sanitize length
                if 3 <= len(ch_title) <= 80:
                    return ch_title
        return None

parser = DocumentParser()
