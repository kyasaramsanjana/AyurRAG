import React from 'react';
import { BookMarked, Layers, Award, FileText, ArrowUpRight } from 'lucide-react';

export default function PassagesView({ passages, onSelectChunk }) {
  if (!passages || passages.length === 0) {
    return (
      <div className="ayur-card p-12 text-center text-stone-400">
        <BookMarked className="w-12 h-12 mx-auto mb-3 opacity-40 text-emerald-400" />
        <p className="text-base font-medium">No passages retrieved yet.</p>
        <p className="text-xs text-stone-500 mt-1">Submit a search query above to view evidence chunks.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white uppercase tracking-wide">
            Retrieved Evidence Passages ({passages.length} Chunks)
          </h3>
          <p className="text-xs text-stone-400 mt-0.5">
            Ranked by Reciprocal Rank Fusion (RRF) combining Dense Vector (BGE 768-d) and Sparse Lexical search.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {passages.map((chunk, idx) => (
          <div key={chunk.id || idx} className="ayur-card p-6 border-l-4 border-l-emerald-500 transition-all">
            {/* Header / Provenance */}
            <div className="flex flex-wrap items-center justify-between gap-2 pb-3 mb-3 border-b border-[#233327]">
              <div className="flex items-center gap-2.5">
                <span className="w-6 h-6 rounded-md bg-emerald-950 text-emerald-400 border border-emerald-700/60 flex items-center justify-center text-xs font-bold">
                  #{idx + 1}
                </span>
                <span className="font-bold text-emerald-300 text-sm md:text-base">
                  {chunk.book_title}
                </span>
                <span className="text-stone-500">•</span>
                <span className="text-xs font-medium text-stone-300">
                  {chunk.chapter}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <span className="px-2 py-0.5 text-xs bg-[#19261d] text-emerald-400 rounded border border-emerald-800/40">
                  Page {chunk.page_number}
                </span>
                <span className="px-2 py-0.5 text-xs bg-[#1f2821] text-amber-300 rounded border border-amber-800/30">
                  Chunk {chunk.chunk_index}
                </span>
              </div>
            </div>

            {/* Chunk Text Passage */}
            <p className="text-stone-200 text-sm md:text-base leading-relaxed bg-[#101712] p-4 rounded-xl border border-[#1e2c22] font-serif">
              "{chunk.text}"
            </p>

            {/* Ranking Metrics (Dense, Sparse, RRF) */}
            <div className="mt-4 pt-3 flex flex-wrap items-center justify-between gap-3 text-xs text-stone-400">
              <div className="flex flex-wrap items-center gap-3">
                {chunk.rrf_score !== null && chunk.rrf_score !== undefined && (
                  <div className="flex items-center gap-1 font-semibold text-emerald-400">
                    <Award className="w-3.5 h-3.5" />
                    <span>RRF Score: {chunk.rrf_score}</span>
                  </div>
                )}
                {chunk.score !== null && chunk.score !== undefined && (
                  <div className="flex items-center gap-1 text-stone-400">
                    <Layers className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Cosine Similarity: {(chunk.score * 100).toFixed(1)}%</span>
                  </div>
                )}
                {chunk.rank_dense && (
                  <span className="text-stone-400">Dense Rank: #{chunk.rank_dense}</span>
                )}
                {chunk.rank_sparse && (
                  <span className="text-stone-400">Sparse Rank: #{chunk.rank_sparse}</span>
                )}
              </div>

              <button
                onClick={() => onSelectChunk(chunk)}
                className="flex items-center gap-1 text-xs text-emerald-400 hover:text-emerald-300 font-medium hover:underline"
              >
                <span>Inspect in Drawer</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
