import React, { useState } from 'react';
import { X, Upload, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';

export default function UploadModal({ isOpen, onClose, onUploadSuccess }) {
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [category, setCategory] = useState('Classical Ayurvedic Treatise');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [statusMessage, setStatusMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const f = e.target.files[0];
      setFile(f);
      if (!title) {
        // Pre-fill title without extension
        const rawName = f.name.replace(/\.[^/.]+$/, "").replace(/_/g, " ");
        setTitle(rawName);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !title.trim()) return;

    setIsUploading(true);
    setStatusMessage(null);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title.trim());
    formData.append('author', author.trim() || 'Ancient Acharya');
    formData.append('category', category.trim());

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        setStatusMessage(`Successfully processed ${data.pages_processed} pages and created ${data.chunks_created} embedded chunks!`);
        if (onUploadSuccess) onUploadSuccess();
        setTimeout(() => {
          onClose();
          setStatusMessage(null);
          setFile(null);
          setTitle('');
        }, 2200);
      } else {
        const err = await res.json();
        setErrorMessage(err.detail || 'Failed to process document');
      }
    } catch (err) {
      setErrorMessage(err.message || 'Network error occurred');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fadeIn">
      <div className="ayur-card w-full max-w-lg p-6 sm:p-8 bg-[#111812] border border-[#2b3e30] shadow-2xl relative">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-[#233327]">
          <div className="flex items-center gap-2 text-emerald-400">
            <Upload className="w-5 h-5" />
            <h3 className="font-bold text-white text-base">Ingest New Ayurvedic Document</h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-stone-400 hover:text-white hover:bg-[#1a271e]">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="mt-5 space-y-4">
          
          <div>
            <label className="block text-xs font-semibold text-stone-300 uppercase tracking-wider mb-1.5">
              Document File (.PDF, .TXT, .MD) *
            </label>
            <div className="relative border-2 border-dashed border-[#2b3e30] hover:border-emerald-500/50 rounded-xl p-5 text-center cursor-pointer bg-[#0e1410] transition-colors">
              <input
                type="file"
                accept=".pdf,.txt,.md"
                onChange={handleFileChange}
                required
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <FileText className="w-8 h-8 mx-auto text-emerald-400/80 mb-2" />
              {file ? (
                <p className="text-sm font-semibold text-emerald-300">{file.name}</p>
              ) : (
                <>
                  <p className="text-xs text-stone-300 font-medium">Click or drag & drop textbook file</p>
                  <p className="text-[11px] text-stone-500 mt-1">Supports Charaka, Sushruta, Nighantu treatises or custom PDFs</p>
                </>
              )}
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-stone-300 uppercase tracking-wider mb-1">
              Treatise Title *
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Ashtanga Samgraha / Madhava Nidana"
              required
              className="w-full px-3.5 py-2.5 rounded-lg bg-[#141d16] border border-[#263729] text-white text-sm focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-stone-300 uppercase tracking-wider mb-1">
                Author / Sage
              </label>
              <input
                type="text"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
                placeholder="e.g. Acharya Madhava"
                className="w-full px-3.5 py-2.5 rounded-lg bg-[#141d16] border border-[#263729] text-white text-sm focus:border-emerald-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-stone-300 uppercase tracking-wider mb-1">
                Category
              </label>
              <input
                type="text"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="e.g. Pathology / Pharmacology"
                className="w-full px-3.5 py-2.5 rounded-lg bg-[#141d16] border border-[#263729] text-white text-sm focus:border-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Feedback messages */}
          {statusMessage && (
            <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-700/60 text-xs text-emerald-300 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 shrink-0" />
              <span>{statusMessage}</span>
            </div>
          )}

          {errorMessage && (
            <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-700/60 text-xs text-rose-300 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Action Buttons */}
          <div className="pt-3 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-stone-400 hover:text-white"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isUploading || !file || !title.trim()}
              className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-semibold text-xs shadow-lg shadow-emerald-950/50 disabled:opacity-50"
            >
              {isUploading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Processing & Chunking...</span>
                </>
              ) : (
                <>
                  <Upload className="w-4 h-4" />
                  <span>Ingest Document</span>
                </>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
}
