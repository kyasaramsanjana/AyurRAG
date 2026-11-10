import React, { useState, useEffect } from 'react';
import { BookOpen, FileText, ChevronRight, RefreshCw, Layers, Sparkles, CheckCircle2 } from 'lucide-react';

export default function CorpusExplorer({ onSelectChunk, onReSeed }) {
  const [books, setBooks] = useState([]);
  const [selectedBook, setSelectedBook] = useState(null);
  const [chunks, setChunks] = useState([]);
  const [isLoadingBooks, setIsLoadingBooks] = useState(false);
  const [isLoadingChunks, setIsLoadingChunks] = useState(false);
  const [seedStatus, setSeedStatus] = useState(null);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    setIsLoadingBooks(true);
    try {
      const res = await fetch('/api/books');
      if (res.ok) {
        const data = await res.json();
        setBooks(data);
        if (data.length > 0 && !selectedBook) {
          loadBookChunks(data[0]);
        }
      }
    } catch (err) {
      console.error("Failed to fetch books", err);
    } finally {
      setIsLoadingBooks(false);
    }
  };

  const loadBookChunks = async (book) => {
    setSelectedBook(book);
    setIsLoadingChunks(true);
    try {
      const res = await fetch(`/api/books/${book.id}/chunks?limit=50`);
      if (res.ok) {
        const data = await res.json();
        setChunks(data);
      }
    } catch (err) {
      console.error("Failed to load chunks", err);
    } finally {
      setIsLoadingChunks(false);
    }
  };

  const handleSeed = async () => {
    setSeedStatus('seeding');
    try {
      const res = await fetch('/api/seed', { method: 'POST' });
      if (res.ok) {
        setSeedStatus('done');
        fetchBooks();
        setTimeout(() => setSeedStatus(null), 3000);
      }
    } catch (err) {
      setSeedStatus('error');
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-[#233327]">
        <div>
          <h3 className="text-lg font-bold text-white uppercase tracking-wide flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-400" />
            Classical Ayurvedic Corpus Explorer
          </h3>
          <p className="text-xs text-stone-400 mt-1">
            Browse indexed classical treatises, chapters, and provenance chunks stored in PostgreSQL + pgvector.
          </p>
        </div>

        <button
          onClick={handleSeed}
          disabled={seedStatus === 'seeding'}
          className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-lg bg-[#18251c] hover:bg-[#1f3024] text-emerald-300 border border-emerald-700/50 transition-all"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${seedStatus === 'seeding' ? 'animate-spin' : ''}`} />
          <span>{seedStatus === 'done' ? 'Corpus Re-Indexed!' : 'Re-Seed Foundational Texts'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Books List Column */}
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400 mb-2">
            Indexed Treatises ({books.length})
          </h4>
          
          {books.map((book) => {
            const isSelected = selectedBook && selectedBook.id === book.id;
            return (
              <div
                key={book.id}
                onClick={() => loadBookChunks(book)}
                className={`ayur-card p-4 cursor-pointer transition-all ${
                  isSelected
                    ? 'border-emerald-500 bg-[#19271e] shadow-lg shadow-emerald-950/40'
                    : 'hover:border-[#38513d]'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h5 className="font-bold text-white text-sm">{book.title}</h5>
                    <p className="text-xs text-stone-400 mt-0.5">{book.author}</p>
                  </div>
                  <ChevronRight className={`w-4 h-4 text-stone-400 transition-transform ${isSelected ? 'rotate-90 text-emerald-400' : ''}`} />
                </div>
                
                <div className="mt-3 pt-2 border-t border-[#233327] flex items-center justify-between text-[11px] text-stone-400">
                  <span className="text-emerald-400/90 font-medium">{book.category}</span>
                  <span>{book.total_chunks || 0} Chunks</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Chunks Inspector Column */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold uppercase tracking-wider text-stone-400">
              Chunks from: <span className="text-emerald-300 font-bold">{selectedBook?.title || 'Select a Book'}</span> ({chunks.length} loaded)
            </h4>
          </div>

          {isLoadingChunks ? (
            <div className="ayur-card p-12 text-center text-stone-400">
              <RefreshCw className="w-8 h-8 animate-spin mx-auto text-emerald-400 mb-2" />
              <p className="text-xs">Loading chunks...</p>
            </div>
          ) : (
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
              {chunks.map((chk, idx) => (
                <div key={chk.id || idx} className="ayur-card p-4 hover:border-emerald-700/50 transition-all">
                  <div className="flex items-center justify-between text-xs mb-2">
                    <span className="font-semibold text-emerald-400">{chk.chapter}</span>
                    <span className="px-2 py-0.5 rounded bg-[#17221a] text-stone-300 border border-[#253629]">
                      Page {chk.page_number} • Chunk #{chk.chunk_index}
                    </span>
                  </div>
                  <p className="text-xs md:text-sm text-stone-300 leading-relaxed font-serif">
                    "{chk.text}"
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
