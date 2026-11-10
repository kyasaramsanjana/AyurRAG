import React from 'react';
import { BookOpen, Upload, Database, Sparkles, RefreshCw, Layers } from 'lucide-react';

export default function Navbar({ systemHealth, onOpenUpload, onOpenCorpus, onReSeed, activeTab, setActiveTab }) {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#233327] bg-[#0c110e]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo & Academic Branding */}
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-emerald-600 via-teal-700 to-emerald-950 flex items-center justify-center shadow-lg shadow-emerald-950/50 border border-emerald-500/30">
              <span className="text-2xl">🌿</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xl font-bold tracking-tight text-white" style={{ fontFamily: 'Cinzel, serif' }}>
                  Ayur<span className="text-emerald-400">RAG</span>
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold bg-emerald-950/80 text-emerald-300 border border-emerald-800/60 rounded-full">
                  v1.0 • Phase-I
                </span>
              </div>
              <p className="text-xs text-stone-400 font-medium hidden sm:block">
                CMR College of Engg & Tech • Dept. of CSE
              </p>
            </div>
          </div>

          {/* Architecture Badges (Slide 4, 10, 21) */}
          <div className="hidden md:flex items-center gap-2 text-xs">
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#151f18] border border-[#26382a] text-stone-300">
              <Database className="w-3.5 h-3.5 text-emerald-400" />
              <span>{systemHealth.dialect === 'postgresql' ? 'PostgreSQL + pgvector' : 'PostgreSQL (pgvector schema ready)'}</span>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#151f18] border border-[#26382a] text-stone-300">
              <Sparkles className="w-3.5 h-3.5 text-amber-400" />
              <span>BGE-Base (768-d)</span>
            </div>
            <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#151f18] border border-[#26382a] text-stone-300">
              <Layers className="w-3.5 h-3.5 text-cyan-400" />
              <span>RRF (k=60)</span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('corpus')}
              className={`flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg border transition-all ${
                activeTab === 'corpus'
                  ? 'bg-emerald-600 text-white border-emerald-500 shadow-lg shadow-emerald-900/40'
                  : 'bg-[#151f18] text-stone-300 border-[#2b3e30] hover:bg-[#1d2a21] hover:text-white'
              }`}
            >
              <BookOpen className="w-4 h-4 text-emerald-400" />
              <span>Corpus ({systemHealth.total_chunks || 0} Chunks)</span>
            </button>

            <button
              onClick={onOpenUpload}
              className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 text-white hover:from-emerald-500 hover:to-teal-500 shadow-md shadow-emerald-950/60 border border-emerald-400/30 transition-all hover:scale-[1.02]"
            >
              <Upload className="w-4 h-4" />
              <span className="hidden sm:inline">Upload Text</span>
            </button>
          </div>

        </div>
      </div>
    </header>
  );
}
