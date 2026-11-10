import React from 'react';
import { GitCompare, BookOpen, Layers } from 'lucide-react';

export default function ComparisonView({ comparisons }) {
  if (!comparisons || comparisons.length === 0) {
    return (
      <div className="ayur-card p-12 text-center text-stone-400">
        <GitCompare className="w-12 h-12 mx-auto mb-3 opacity-40 text-amber-400" />
        <p className="text-base font-medium">No comparison data available yet.</p>
        <p className="text-xs text-stone-500 mt-1">Submit a search query to generate cross-textual matrix comparisons.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fadeIn">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white uppercase tracking-wide flex items-center gap-2">
            <GitCompare className="w-5 h-5 text-amber-400" />
            Cross-Textual Comparative Analysis
          </h3>
          <p className="text-xs text-stone-400 mt-0.5">
            Synthesis across the four primary Ayurvedic treatises: Charaka, Sushruta, Ashtanga Hridaya, and Bhavaprakasha.
          </p>
        </div>
      </div>

      <div className="ayur-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs md:text-sm border-collapse">
            <thead>
              <tr className="bg-[#17231b] border-b border-[#283b2d] text-stone-300 font-bold uppercase tracking-wider text-[11px]">
                <th className="p-4 w-1/5 min-w-[140px]">Aspect</th>
                <th className="p-4 w-1/5 min-w-[180px] text-emerald-300">
                  <div className="flex items-center gap-1.5">
                    <span>Charaka Samhita</span>
                  </div>
                </th>
                <th className="p-4 w-1/5 min-w-[180px] text-teal-300">
                  <div className="flex items-center gap-1.5">
                    <span>Sushruta Samhita</span>
                  </div>
                </th>
                <th className="p-4 w-1/5 min-w-[180px] text-amber-300">
                  <div className="flex items-center gap-1.5">
                    <span>Ashtanga Hridaya</span>
                  </div>
                </th>
                <th className="p-4 w-1/5 min-w-[180px] text-rose-300">
                  <div className="flex items-center gap-1.5">
                    <span>Bhavaprakasha</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1e2c22]">
              {comparisons.map((item, idx) => (
                <tr key={idx} className="hover:bg-[#162119] transition-colors">
                  <td className="p-4 font-bold text-stone-200 bg-[#121914] border-r border-[#1e2c22]">
                    {item.aspect}
                  </td>
                  <td className="p-4 text-stone-300 leading-relaxed border-r border-[#1e2c22]">
                    {item.charaka_samhita}
                  </td>
                  <td className="p-4 text-stone-300 leading-relaxed border-r border-[#1e2c22]">
                    {item.sushruta_samhita}
                  </td>
                  <td className="p-4 text-stone-300 leading-relaxed border-r border-[#1e2c22]">
                    {item.ashtanga_hridaya}
                  </td>
                  <td className="p-4 text-stone-300 leading-relaxed">
                    {item.bhavaprakasha_nighantu}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
