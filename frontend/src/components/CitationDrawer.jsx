import React from 'react';
import { X, BookOpen, Layers, CheckCircle2, Bookmark, ExternalLink } from 'lucide-react';

export default function CitationDrawer({ isOpen, onClose, citation }) {
  if (!isOpen || !citation) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden animate-fadeIn">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/70 backdrop-blur-sm transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-md bg-[#111913] border-l border-[#273a2c] shadow-2xl p-6 flex flex-col justify-between overflow-y-auto">
          
          <div>
            {/* Header */}
            <div className="flex items-center justify-between pb-4 border-b border-[#233327]">
              <div className="flex items-center gap-2 text-emerald-400">
                <Bookmark className="w-5 h-5" />
                <h3 className="font-bold text-white text-base">Citation Provenance</h3>
              </div>
              <button
                onClick={onClose}
                className="p-1.5 rounded-lg text-stone-400 hover:text-white hover:bg-[#1a271e] transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Metadata Badges */}
            <div className="my-5 space-y-3">
              <div className="p-4 rounded-xl bg-[#17231b] border border-[#273a2c]">
                <h4 className="text-lg font-bold text-emerald-300 font-serif">
                  {citation.book_title}
                </h4>
                <p className="text-xs text-stone-300 mt-1 font-medium">
                  {citation.chapter}
                </p>
                <div className="mt-3 flex items-center gap-2 text-xs">
                  <span className="px-2 py-0.5 rounded bg-[#101712] text-emerald-400 border border-emerald-800/40 font-semibold">
                    Page {citation.page_number}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-[#101712] text-amber-300 border border-amber-800/30 font-semibold">
                    Chunk #{citation.chunk_index}
                  </span>
                </div>
              </div>

              {/* Exact Evidence Text */}
              <div className="space-y-2">
                <h5 className="text-xs font-bold uppercase tracking-wider text-stone-400 flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4 text-emerald-400" />
                  Original Classical Passage
                </h5>
                <div className="p-4 rounded-xl bg-[#0e1410] border border-[#223325] text-stone-200 text-sm leading-relaxed font-serif">
                  "{citation.text || citation.excerpt}"
                </div>
              </div>
            </div>
          </div>

          {/* Footer Validation Notice */}
          <div className="pt-4 border-t border-[#233327]">
            <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-800/40 text-[11px] text-emerald-300/90 leading-relaxed">
              <span className="font-semibold block mb-0.5">Ground-Truth Verification:</span>
              This excerpt is extracted directly from the indexed edition. Researchers should cross-reference with Sanskrit original commentaries for therapeutic confirmation.
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
