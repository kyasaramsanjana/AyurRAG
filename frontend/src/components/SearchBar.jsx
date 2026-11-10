import React from 'react';
import { Search, Loader2, Sparkles, Filter } from 'lucide-react';

const EXAMPLE_QUERIES = [
  "What are the classical herbal remedies for fever (Jwara)?",
  "How to get relief from cough and cold according to Charaka Samhita?",
  "What does Sushruta Samhita describe about wound healing and Haridra (Turmeric)?",
  "Daily regimen (Dinacharya) and morning routine in Ashtanga Hridaya",
  "What are the pharmacological properties of Ashwagandha in Bhavaprakasha Nighantu?"
];

export default function SearchBar({ query, setQuery, onSearch, isLoading, searchMode, setSearchMode }) {
  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query);
    }
  };

  const handleChipClick = (q) => {
    setQuery(q);
    onSearch(q);
  };

  return (
    <div className="w-full max-w-4xl mx-auto mb-8">
      {/* Search Input Bar */}
      <form onSubmit={handleSubmit} className="relative group">
        <div className="absolute -inset-1 bg-gradient-to-r from-emerald-600 via-teal-600 to-amber-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition duration-300"></div>
        <div className="relative flex items-center bg-[#131b15] border border-[#2b3e30] rounded-2xl shadow-2xl overflow-hidden focus-within:border-emerald-500/80 transition-all">
          <div className="pl-5 text-emerald-400">
            <Search className="w-5 h-5" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask anything across Charaka, Sushruta, Ashtanga Hridaya & Bhavaprakasha..."
            className="w-full py-4 px-4 bg-transparent text-stone-100 placeholder-stone-500 text-sm md:text-base focus:outline-none"
          />

          <div className="flex items-center gap-2 pr-3">
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs md:text-sm shadow-lg shadow-emerald-950/60 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Retrieving...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  <span>Search RAG</span>
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Query Suggestions Pills */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="text-[11px] font-semibold uppercase tracking-wider text-stone-400 flex items-center gap-1">
          💡 Try Sample Queries:
        </span>
        {EXAMPLE_QUERIES.map((eq, idx) => (
          <button
            key={idx}
            onClick={() => handleChipClick(eq)}
            className="text-xs px-3 py-1.5 rounded-lg bg-[#162119] border border-[#26382a] text-stone-300 hover:text-emerald-300 hover:border-emerald-500/40 hover:bg-[#1c2c21] transition-all text-left"
          >
            {eq}
          </button>
        ))}
      </div>
    </div>
  );
}
