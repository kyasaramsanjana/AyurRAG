import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import SearchBar from './components/SearchBar';
import AnswerView from './components/AnswerView';
import PassagesView from './components/PassagesView';
import ComparisonView from './components/ComparisonView';
import CorpusExplorer from './components/CorpusExplorer';
import CitationDrawer from './components/CitationDrawer';
import UploadModal from './components/UploadModal';
import { BookOpen, FileText, GitCompare, Sparkles, AlertCircle, Layers } from 'lucide-react';

export default function App() {
  const [query, setQuery] = useState('');
  const [activeTab, setActiveTab] = useState('answer'); // 'answer', 'passages', 'comparison', 'corpus'
  const [searchMode, setSearchMode] = useState('hybrid');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);
  const [systemHealth, setSystemHealth] = useState({
    dialect: 'postgresql',
    total_books: 4,
    total_chunks: 17,
    embedding_model: 'BAAI/bge-base-en-v1.5'
  });

  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedCitation, setSelectedCitation] = useState(null);
  const [isCitationDrawerOpen, setIsCitationDrawerOpen] = useState(false);

  useEffect(() => {
    fetchHealth();
    // Auto-search default question to populate rich UI on load
    handleSearch("What are the classical remedies for fever (Jwara)?");
  }, []);

  const fetchHealth = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setSystemHealth(data);
      }
    } catch (e) {
      console.warn("Could not reach backend health endpoint", e);
    }
  };

  const handleSearch = async (searchQuery) => {
    if (!searchQuery.trim()) return;
    setIsLoading(true);
    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: searchQuery.trim(),
          top_k: 5,
          enable_llm_synthesis: true
        })
      });

      if (res.ok) {
        const data = await res.json();
        setResponse(data);
        if (activeTab === 'corpus') {
          setActiveTab('answer');
        }
      }
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCitationClick = (cit) => {
    setSelectedCitation(cit);
    setIsCitationDrawerOpen(true);
  };

  const handleSelectChunk = (chunk) => {
    setSelectedCitation({
      book_title: chunk.book_title,
      chapter: chunk.chapter,
      page_number: chunk.page_number,
      chunk_index: chunk.chunk_index,
      text: chunk.text
    });
    setIsCitationDrawerOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0b100d] text-stone-100">
      
      {/* Top Navbar */}
      <Navbar
        systemHealth={systemHealth}
        onOpenUpload={() => setIsUploadModalOpen(true)}
        onOpenCorpus={() => setActiveTab('corpus')}
        onReSeed={fetchHealth}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Project Header Banner with CMR College Info */}
        <div className="text-center mb-8 relative">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/50 text-emerald-300 text-xs font-semibold mb-3">
            <span>✨ Cross-Textual Ayurvedic Knowledge Retrieval and Analysis System</span>
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white mb-2" style={{ fontFamily: 'Cinzel, serif' }}>
            Ayur<span className="emerald-gradient">RAG</span> Intelligence
          </h1>
          <p className="max-w-2xl mx-auto text-xs sm:text-sm text-stone-400 font-normal">
            B.Tech Major Project Phase-I • <strong className="text-stone-300">K. Sanjana</strong> (23H51A05G5), B. Maheswari, P. Rajvarun • Under the guidance of <strong className="text-stone-300">Dr. S. Siva Skandha</strong>, Professor
          </p>
        </div>

        {/* Global Search Bar */}
        <SearchBar
          query={query}
          setQuery={setQuery}
          onSearch={handleSearch}
          isLoading={isLoading}
          searchMode={searchMode}
          setSearchMode={setSearchMode}
        />

        {/* Navigation Tabs (Slide 4, 21, 24) */}
        <div className="flex items-center justify-center border-b border-[#233327] mb-8">
          <div className="flex items-center gap-2 sm:gap-4 overflow-x-auto py-2">
            
            <button
              onClick={() => setActiveTab('answer')}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                activeTab === 'answer'
                  ? 'bg-emerald-600/90 text-white shadow-lg shadow-emerald-950/50 border border-emerald-500'
                  : 'text-stone-400 hover:text-white hover:bg-[#151f18]'
              }`}
            >
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Answer & Remedies</span>
            </button>

            <button
              onClick={() => setActiveTab('passages')}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                activeTab === 'passages'
                  ? 'bg-emerald-600/90 text-white shadow-lg shadow-emerald-950/50 border border-emerald-500'
                  : 'text-stone-400 hover:text-white hover:bg-[#151f18]'
              }`}
            >
              <FileText className="w-4 h-4 text-emerald-400" />
              <span>Original Passages ({response?.retrieved_passages?.length || 0})</span>
            </button>

            <button
              onClick={() => setActiveTab('comparison')}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                activeTab === 'comparison'
                  ? 'bg-emerald-600/90 text-white shadow-lg shadow-emerald-950/50 border border-emerald-500'
                  : 'text-stone-400 hover:text-white hover:bg-[#151f18]'
              }`}
            >
              <GitCompare className="w-4 h-4 text-amber-400" />
              <span>Comparison Table</span>
            </button>

            <button
              onClick={() => setActiveTab('corpus')}
              className={`flex items-center gap-2 px-4 py-2.5 text-xs sm:text-sm font-bold rounded-xl transition-all ${
                activeTab === 'corpus'
                  ? 'bg-emerald-600/90 text-white shadow-lg shadow-emerald-950/50 border border-emerald-500'
                  : 'text-stone-400 hover:text-white hover:bg-[#151f18]'
              }`}
            >
              <BookOpen className="w-4 h-4 text-teal-400" />
              <span>Corpus Explorer</span>
            </button>

          </div>
        </div>

        {/* Tab Content Rendering */}
        <div className="pb-16">
          {activeTab === 'answer' && (
            <AnswerView
              response={response}
              onCitationClick={handleCitationClick}
            />
          )}

          {activeTab === 'passages' && (
            <PassagesView
              passages={response?.retrieved_passages || []}
              onSelectChunk={handleSelectChunk}
            />
          )}

          {activeTab === 'comparison' && (
            <ComparisonView
              comparisons={response?.comparisons || []}
            />
          )}

          {activeTab === 'corpus' && (
            <CorpusExplorer
              onSelectChunk={handleSelectChunk}
              onReSeed={fetchHealth}
            />
          )}
        </div>

      </main>

      {/* Slide-out Citation Provenance Drawer */}
      <CitationDrawer
        isOpen={isCitationDrawerOpen}
        onClose={() => setIsCitationDrawerOpen(false)}
        citation={selectedCitation}
      />

      {/* Document Ingestion Upload Modal */}
      <UploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        onUploadSuccess={fetchHealth}
      />

      {/* Footer */}
      <footer className="border-t border-[#1e2b21] bg-[#090e0b] py-6 text-center text-xs text-stone-500">
        <p>
          AyurRAG: Cross-Textual Ayurvedic Knowledge Retrieval System • Dept of Computer Science & Engineering • CMRCET 2026-2027
        </p>
      </footer>

    </div>
  );
}
