import React from 'react';
import { Sparkles, Pill, CheckCircle2, BookOpen, Clock, Cpu, ExternalLink } from 'lucide-react';

export default function AnswerView({ response, onCitationClick }) {
  if (!response) return null;

  return (
    <div className="space-y-8 animate-fadeIn">
      
      {/* Top Meta Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-5 py-3.5 rounded-xl bg-[#131b15] border border-[#243428] text-xs text-stone-400">
        <div className="flex items-center gap-2">
          <Cpu className="w-4 h-4 text-emerald-400" />
          <span className="font-medium text-stone-300">{response.model_used}</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-emerald-400 font-medium">
            {response.retrieval_method}
          </span>
          {response.stats?.latency_ms && (
            <div className="flex items-center gap-1 text-stone-400">
              <Clock className="w-3.5 h-3.5" />
              <span>{response.stats.latency_ms} ms</span>
            </div>
          )}
        </div>
      </div>

      {/* Narrative Synthesis Section */}
      <div className="ayur-card p-6 sm:p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>
        <div className="flex items-center gap-2.5 mb-4 text-emerald-400">
          <Sparkles className="w-5 h-5" />
          <h2 className="text-base font-bold tracking-wide uppercase text-stone-200">
            Synthesized Ayurvedic Intelligence
          </h2>
        </div>

        <div className="text-stone-200 leading-relaxed space-y-4 text-sm md:text-base font-normal">
          {response.answer_text.split('\n\n').map((para, idx) => {
            if (para.startsWith('>')) {
              return (
                <div key={idx} className="p-4 rounded-lg bg-amber-950/20 border border-amber-900/40 text-amber-200/90 text-xs leading-relaxed italic">
                  {para.replace(/^>\s*/, '')}
                </div>
              );
            }
            return <p key={idx}>{para}</p>;
          })}
        </div>

        {/* Citations Badges */}
        {response.citations && response.citations.length > 0 && (
          <div className="mt-6 pt-5 border-t border-[#233327] flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-stone-400 mr-2 flex items-center gap-1">
              <BookOpen className="w-3.5 h-3.5 text-emerald-400" />
              Cited Evidence Passages:
            </span>
            {response.citations.map((cit, idx) => (
              <button
                key={idx}
                onClick={() => onCitationClick(cit)}
                className="citation-chip"
                title="Click to view supporting original passage in citation drawer"
              >
                <span>[{cit.book_title}, p. {cit.page_number}]</span>
                <ExternalLink className="w-2.5 h-2.5 opacity-70" />
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Classical Remedies Grid (Slide 24) */}
      {response.remedies && response.remedies.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center gap-2 text-stone-200">
            <Pill className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold tracking-wide uppercase">
              Prescribed Classical Formulations & Remedies
            </h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {response.remedies.map((rem, idx) => (
              <div key={idx} className="ayur-card p-5 border-l-4 border-l-amber-500 flex flex-col justify-between">
                <div>
                  <div className="flex items-start justify-between gap-2 mb-2">
                    <h4 className="font-bold text-white text-sm md:text-base">{rem.title}</h4>
                    <span className="px-2 py-0.5 text-[11px] font-semibold bg-[#1e2d22] text-emerald-300 rounded border border-emerald-700/50">
                      {rem.source_book}
                    </span>
                  </div>

                  {/* Ingredients Tags */}
                  <div className="flex flex-wrap gap-1.5 my-3">
                    {rem.ingredients.map((ing, i) => (
                      <span key={i} className="px-2 py-0.5 text-xs bg-[#19241b] text-stone-300 rounded border border-[#2b3e30]">
                        🌿 {ing}
                      </span>
                    ))}
                  </div>

                  <p className="text-xs md:text-sm text-stone-300 leading-relaxed mb-3">
                    <strong className="text-amber-300/90 font-medium">Preparation: </strong>
                    {rem.method}
                  </p>
                </div>

                <div className="pt-3 border-t border-[#233327] text-xs text-stone-400">
                  <strong className="text-stone-300">Action: </strong>
                  {rem.indications}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Takeaways Section */}
      {response.key_takeaways && response.key_takeaways.length > 0 && (
        <div className="ayur-card p-6">
          <div className="flex items-center gap-2 mb-4 text-emerald-400">
            <CheckCircle2 className="w-5 h-5" />
            <h3 className="text-sm font-bold tracking-wide uppercase text-stone-200">
              Key Scholarly Takeaways
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {response.key_takeaways.map((point, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3.5 rounded-xl bg-[#17221a] border border-[#263729]">
                <div className="w-5 h-5 rounded-full bg-emerald-950 text-emerald-400 flex items-center justify-center text-xs font-bold shrink-0 mt-0.5 border border-emerald-800">
                  {idx + 1}
                </div>
                <p className="text-xs md:text-sm text-stone-300 leading-relaxed">{point}</p>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
}
