# AyurRAG: Cross-Textual Ayurvedic Knowledge Retrieval and Analysis System

> **CMR College of Engineering & Technology**  
> Kandlakoya, Medchal, Hyderabad – 501401  
> **Department of Computer Science and Engineering**  
> **Major Project Phase-I**  
> 
> **Project Team:**
> - **K. Sanjana** (23H51A05G5)
> - **B. Maheswari** (23H51A05E0)
> - **P. Rajvarun** (23H51A05H5)
>
> **Project Guide:**  
> **Dr. S. Siva Skandha**, Professor, Department of CSE

---

## 🌿 1. Abstract & System Overview
Ayurvedic knowledge is preserved in extensive classical treatises (*Charaka Samhita*, *Sushruta Samhita*, *Ashtanga Hridaya*, and *Bhavaprakasha Nighantu*), with relevant information spread across dispersed chapters, formulations, and materia medica sections.

**AyurRAG** is a cross-textual retrieval-augmented generation prototype designed to search, retrieve, and present relevant passages from indexed Ayurvedic texts. It solves the critical limitations of standard semantic chatbots:
1. **Preserves Provenance**: Tracks exact book, page, chapter, and chunk indices for complete textual verification.
2. **Hybrid Search with Reciprocal Rank Fusion (RRF)**: Merges dense vector retrieval (capturing semantic similarity and paraphrasing) with sparse lexical search (capturing exact Sanskrit herb and condition names).
3. **Structured Multi-View Presentation**: Segregates answers into **Answer & Remedies**, **Original Passages**, **Comparison Table**, and **Corpus Explorer**.

---

## 🏗️ 2. Architectural Specification (Matches Presentation Slide 21)

```
                            [ User (Browser) ]
                                    │
                                    ▼
                      [ React / Vite Frontend ]
        Search | Answer, Passages & Comparison tabs | Citation drawer | Corpus explorer
                                    │
                                    ▼
                     [ FastAPI Backend (REST API) ]
        Query | Raw search | Books / Chunks | Seed | Upload | Delete | Health
                     │                                   │
                     ▼ (Query Pipeline)                  ▼ (Ingestion Pipeline)
        ┌─────────────────────────┐         ┌─────────────────────────┐
        │ Dense Search (pgvector) │         │ Parser (PDF / TXT / MD) │
        │ Sparse Search (FTS/Lex) │         │ Chunker (Word-bounded)  │
        │ Reciprocal Rank Fusion  │         │ Embedding Service (BGE) │
        │ Gemini / Fallback Synth │         │                         │
        └─────────────────────────┘         └─────────────────────────┘
                     │                                   │
                     └─────────────────┬─────────────────┘
                                       ▼
                       [ PostgreSQL + pgvector ]
              books | text_chunks (text, page, chapter, embedding)
```

---

## ⚙️ 3. Core Technical Components (Slide-by-Slide Verification)

| Component | PPT Slide Specification | Implementation in Code |
| :--- | :--- | :--- |
| **Frontend UI** | React + Vite with Answer, Passages, Comparison tabs & Citation drawer | `frontend/src/App.jsx` + Components in `frontend/src/components/` |
| **Backend API** | FastAPI with REST endpoints (`/query`, `/search`, `/books`, `/upload`, etc.) | `backend/app/main.py` |
| **Database** | PostgreSQL + pgvector with books & text_chunks tables | `backend/app/database.py` (with automatic SQLite fallback for zero-friction demo) |
| **Embedding Model** | `BAAI/bge-base-en-v1.5` (768-dimensional normalized dense vectors) | `backend/app/services/embedding.py` |
| **Retrieval Engine** | Hybrid: Dense Cosine Similarity + Sparse Lexical Search + Reciprocal Rank Fusion ($k=60$) | `backend/app/services/retrieval.py` |
| **Synthesis Service**| Gemini API with intelligent rule-based / extractive synthesis fallback | `backend/app/services/synthesis.py` |
| **Foundational Corpus**| Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya, Bhavaprakasha Nighantu | `backend/app/data/seed_corpus.py` |

---

## 🚀 4. How to Run the Project

### Option A: One-Click Startup (Windows)
Double-click:
```cmd
run_ayurrag.bat
```
This automatically starts both the FastAPI backend (`http://127.0.0.1:8000`) and the Vite React frontend (`http://localhost:5173`).

---

### Option B: Manual Startup

#### Step 1: Start Backend
```powershell
cd AyurRAG
.\venv\Scripts\python.exe backend\run.py
```
Backend will start on `http://127.0.0.1:8000` (Interactive API docs at `http://127.0.0.1:8000/docs`).

#### Step 2: Start Frontend
```powershell
cd AyurRAG\frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 💡 5. Answers to Guide / Examiner Viva Questions

**Q1: Why did you use Reciprocal Rank Fusion (RRF) instead of just cosine similarity?**  
*Answer:* Dense retrieval using embeddings is great for semantic understanding and paraphrased questions, but it struggles with exact domain terms, classical botanical names, and specific Sanskrit keywords (like *Haridra*, *Langhana*, *Vrana*). Sparse/lexical search is great for exact words. Direct addition of vector similarity (0.0 to 1.0) and BM25 scores (unbounded) is unstable because their score distributions are completely different. RRF ($RRF(d) = \sum \frac{1}{60 + r_i}$) solves this by using rank order rather than raw scores, outperforming individual rank learning methods.

**Q2: What is the embedding dimension and model?**  
*Answer:* We use `BAAI/bge-base-en-v1.5` which produces 768-dimensional dense vector representations stored in `pgvector`.

**Q3: How does the citation drawer work?**  
*Answer:* During ingestion, the chunker maintains provenance metadata (`book_id`, `book_title`, `chapter`, `page_number`, `chunk_index`). When synthesis generates an answer, citations link back to the exact chunk ID, allowing the user to click the badge and inspect the original un-altered passage in the side drawer.

**Q4: Is this system intended for direct clinical prescription?**  
*Answer:* No. As clearly stated in our Abstract and Project Scope (Slide 4 & 25), AyurRAG is an educational and textual exploration prototype designed for students, researchers, and learners to cross-verify ancient literature. It is not a diagnostic or clinical prescription service.
