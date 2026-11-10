import json
import logging
import re
from typing import List, Dict, Any
import requests
from app.config import settings

logger = logging.getLogger("ayurrag.synthesis")

class SynthesisService:
    """
    Synthesis Service for AyurRAG (PPT Slide 4, 21, 23, 24).
    Uses Gemini LLM when configured, with an intelligent classical
    extractive synthesis fallback when offline or unconfigured.
    """

    DISCLAIMER = (
        "Educational Prototype Notice: This response is synthesized for research and "
        "textual exploration of classical Ayurvedic literature. It does not constitute medical "
        "advice, diagnosis, or clinical prescription. Verify all findings against authoritative "
        "treatises and qualified Ayurvedic physicians."
    )

    def synthesize(self, query: str, retrieved_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not retrieved_items:
            return {
                "answer_text": f"No relevant Ayurvedic passages found for '{query}'. Please try querying specific herbs, conditions (e.g., Jwara, Kasa, Vrana), or Ayurvedic concepts.",
                "remedies": [],
                "key_takeaways": ["No matching text chunks retrieved."],
                "comparisons": [],
                "citations": [],
                "model_used": "None (Empty Context)"
            }

        # Try Gemini API if key is configured
        if settings.GEMINI_API_KEY:
            try:
                gemini_res = self._call_gemini(query, retrieved_items)
                if gemini_res:
                    return gemini_res
            except Exception as e:
                logger.warning(f"Gemini API invocation failed ({e}), falling back to structured classical synthesis.")

        # Classical Rule-Based & Extractive Synthesis Fallback (Slide 4 & 23)
        return self._fallback_synthesis(query, retrieved_items)

    def _call_gemini(self, query: str, retrieved_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        context_blocks = []
        for idx, item in enumerate(retrieved_items, start=1):
            ch = item["chunk"]
            context_blocks.append(
                f"[Source {idx}]: {ch.book_title} | {ch.chapter} | Page {ch.page_number}\nText: {ch.text}"
            )
        context_str = "\n\n".join(context_blocks)

        prompt = f"""You are AyurRAG, an AI system grounded strictly in classical Ayurvedic treatises (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Bhavaprakasha Nighantu).
Based ONLY on the provided retrieved passages below, answer the user query in JSON format.

User Query: "{query}"

Retrieved Passages:
{context_str}

Respond with valid JSON containing:
{{
  "answer_text": "Detailed, coherent narrative synthesis grounded in the classical passages, citing sources like [Charaka Samhita, p. 12].",
  "remedies": [
    {{
      "title": "Remedy Name",
      "source_book": "Book Name",
      "ingredients": ["Item 1", "Item 2"],
      "method": "Preparation and dosage instruction",
      "indications": "Conditions treated"
    }}
  ],
  "key_takeaways": [
    "Core classical principle 1",
    "Core classical principle 2"
  ],
  "comparisons": [
    {{
      "aspect": "e.g. Etiology / Treatment Focus / Herb Properties",
      "charaka_samhita": "Charaka perspective from context",
      "sushruta_samhita": "Sushruta perspective from context",
      "ashtanga_hridaya": "Ashtanga Hridaya perspective from context",
      "bhavaprakasha_nighantu": "Bhavaprakasha perspective from context"
    }}
  ]
}}
Only return the JSON object, without backticks or extra commentary.
"""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
        }
        resp = requests.post(url, json=payload, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)
            parsed["citations"] = self._build_citations(retrieved_items)
            parsed["model_used"] = f"Gemini ({settings.GEMINI_MODEL})"
            parsed["answer_text"] += f"\n\n> {self.DISCLAIMER}"
            return parsed
        return None

    def _fallback_synthesis(self, query: str, retrieved_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Grounded Extractive Synthesis Fallback (Slide 4, 7, 24).
        Synthesizes direct answer, remedies, key takeaways, cross-textual comparison,
        and citations directly from retrieved source passages.
        """
        citations = self._build_citations(retrieved_items)
        
        # Analyze retrieved chunks
        books_involved = list(set(it["chunk"].book_title for it in retrieved_items))
        chunks = [it["chunk"] for it in retrieved_items]
        combined_text = " ".join(ch.text for ch in chunks)

        # 1. Generate Narrative Answer
        lead_chunk = chunks[0]
        narrative_parts = [
            f"According to classical Ayurvedic literature ({', '.join(books_involved)}), "
            f"addressing '{query}' involves balancing the bodily Doshas (Vata, Pitta, and Kapha) and stimulating digestive fire (Agni).",
            f"Primary guidance from **{lead_chunk.book_title}** ({lead_chunk.chapter}, p. {lead_chunk.page_number}) emphasizes: \"{self._truncate(lead_chunk.text, 220)}\""
        ]

        if len(chunks) > 1:
            second_chunk = chunks[1]
            narrative_parts.append(
                f"Furthermore, **{second_chunk.book_title}** ({second_chunk.chapter}, p. {second_chunk.page_number}) corroborates: \"{self._truncate(second_chunk.text, 200)}\""
            )

        narrative_parts.append(f"\n> **Note**: {self.DISCLAIMER}")
        answer_text = "\n\n".join(narrative_parts)

        # 2. Extract Specific Classical Remedies
        remedies = []
        for ch in chunks:
            remedy_match = self._extract_remedy(ch)
            if remedy_match and len(remedies) < 4:
                remedies.append(remedy_match)

        # 3. Key Takeaways
        takeaways = [
            f"Cross-textual consensus across {len(books_involved)} classical treatise(s): {', '.join(books_involved)}.",
            f"Top retrieved evidence chunk ranked #1 with Reciprocal Rank Fusion score: {retrieved_items[0]['rrf_score']}.",
            "Formulations emphasize synergy between hot-potency herbs (Ushna Virya) and digestive pacification.",
            "Always corroborate traditional preparations with authoritative botanical and clinical references."
        ]

        # 4. Cross-Textual Comparative Table (Slide 24)
        comparisons = self._build_comparison_table(chunks)

        return {
            "answer_text": answer_text,
            "remedies": remedies,
            "key_takeaways": takeaways,
            "comparisons": comparisons,
            "citations": citations,
            "model_used": "AyurRAG Classical Extractive Synthesis Engine (Rule-Based Fallback)"
        }

    def _build_citations(self, retrieved_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cits = []
        for item in retrieved_items:
            ch = item["chunk"]
            cits.append({
                "chunk_id": ch.id,
                "book_title": ch.book_title,
                "chapter": ch.chapter,
                "page_number": ch.page_number,
                "chunk_index": ch.chunk_index,
                "excerpt": self._truncate(ch.text, 160)
            })
        return cits

    def _extract_remedy(self, chunk: Any) -> Dict[str, Any]:
        text = chunk.text
        # Identify common herbs in chunk
        herbs = ["Tulsi", "Ginger", "Shunthi", "Haridra", "Turmeric", "Pippali", "Triphala",
                 "Black Pepper", "Honey", "Coriander", "Cumin", "Fennel", "Ashwagandha", "Amla", "Neem", "Ghee"]
        found_herbs = [h for h in herbs if re.search(r'\b' + h + r'\b', text, re.IGNORECASE)]
        
        if not found_herbs:
            found_herbs = ["Ayurvedic Botanical Compounds", "Tri-Dosha Balancing Herbs"]

        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        method_snippet = sentences[0] if sentences else text[:120]

        return {
            "title": f"{chunk.book_title} Formulation ({chunk.chapter})",
            "source_book": f"{chunk.book_title} (p. {chunk.page_number})",
            "ingredients": found_herbs[:5],
            "method": method_snippet + ".",
            "indications": f"Prescribed in {chunk.chapter} for relief, digestive equilibrium, and symptom alleviation."
        }

    def _build_comparison_table(self, chunks: List[Any]) -> List[Dict[str, Any]]:
        # Map chunks by book
        book_snippets = {
            "Charaka Samhita": "Emphasizes internal medicine (Kayachikitsa), metabolic balance (Agni), and doshic harmony via herbal teas and decoctions.",
            "Sushruta Samhita": "Highlights surgical cleansing (Shalya), antiseptic dressings (Haridra/Kshara), and anti-inflammatory wound management.",
            "Ashtanga Hridaya": "Focuses on daily routine (Dinacharya), seasonal adaptation (Ritucharya), digestion, and balanced home dietary regimens.",
            "Bhavaprakasha Nighantu": "Provides comprehensive Materia Medica (Dravyaguna), classifying herbs by Rasa (Taste), Virya (Potency), and Vipaka."
        }

        # Override with exact snippets if matched
        for ch in chunks:
            for bname in book_snippets.keys():
                if bname.lower() in ch.book_title.lower():
                    book_snippets[bname] = f"[{ch.chapter}, p.{ch.page_number}]: {self._truncate(ch.text, 140)}"

        return [
            {
                "aspect": "Core Philosophy & Focus",
                "charaka_samhita": book_snippets["Charaka Samhita"],
                "sushruta_samhita": book_snippets["Sushruta Samhita"],
                "ashtanga_hridaya": book_snippets["Ashtanga Hridaya"],
                "bhavaprakasha_nighantu": book_snippets["Bhavaprakasha Nighantu"]
            },
            {
                "aspect": "Therapeutic Approach",
                "charaka_samhita": "Internal decoctions, fasting (Langhana), and restoring gastrointestinal fire.",
                "sushruta_samhita": "Direct purification, sterile pastes, external application, and tissue regeneration.",
                "ashtanga_hridaya": "Synergistic combinations of honey, medicated ghee, and balanced lifestyle.",
                "bhavaprakasha_nighantu": "Pharmacological properties: Hot/Cold potency (Virya) and post-digestive bio-transformation (Vipaka)."
            }
        ]

    def _truncate(self, text: str, max_chars: int) -> str:
        if len(text) <= max_chars:
            return text
        return text[:max_chars].rstrip() + "..."

synthesis_service = SynthesisService()
