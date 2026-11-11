import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, FileText, CheckCircle2 } from 'lucide-react';
import { PaperItem } from '../services/api';

interface PDFViewerPanelProps {
  activePaper: PaperItem | null;
  targetPage: number;
}

export const PDFViewerPanel: React.FC<PDFViewerPanelProps> = ({
  activePaper,
  targetPage,
}) => {
  const [currentPage, setCurrentPage] = useState(1);
  const [zoom, setZoom] = useState(100);

  useEffect(() => {
    if (targetPage > 0) {
      setCurrentPage(targetPage);
    }
  }, [targetPage]);

  if (!activePaper) {
    return (
      <div className="w-96 h-full bg-slate-900 border-l border-slate-800 flex flex-col items-center justify-center p-6 text-center text-slate-500">
        <FileText className="w-12 h-12 mb-3 text-slate-700" />
        <div className="font-medium text-slate-400">PDF Viewer</div>
        <div className="text-xs mt-1">Select an indexed research paper from the sidebar to view documents and citations.</div>
      </div>
    );
  }

  const totalPages = activePaper.total_pages || 10;

  return (
    <div className="w-[420px] h-full bg-slate-900 border-l border-slate-800 flex flex-col">
      {/* Viewer Header */}
      <div className="h-14 px-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2 min-w-0">
          <FileText className="w-4 h-4 text-emerald-400 shrink-0" />
          <span className="text-sm font-semibold text-slate-200 truncate">{activePaper.title}</span>
        </div>
        <div className="flex items-center gap-1 text-slate-400">
          <button
            onClick={() => setZoom((z) => Math.max(50, z - 10))}
            className="p-1 hover:text-slate-200 hover:bg-slate-800 rounded"
            title="Zoom Out"
          >
            <ZoomOut className="w-3.5 h-3.5" />
          </button>
          <span className="text-xs font-mono">{zoom}%</span>
          <button
            onClick={() => setZoom((z) => Math.min(150, z + 10))}
            className="p-1 hover:text-slate-200 hover:bg-slate-800 rounded"
            title="Zoom In"
          >
            <ZoomIn className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Page Navigation Toolbar */}
      <div className="h-10 px-4 bg-slate-950/40 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
            disabled={currentPage <= 1}
            className="p-1 hover:text-slate-200 disabled:opacity-30 rounded"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>
          <span className="font-mono">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
            disabled={currentPage >= totalPages}
            className="p-1 hover:text-slate-200 disabled:opacity-30 rounded"
          >
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {targetPage === currentPage && (
          <div className="flex items-center gap-1 text-emerald-400 text-xs font-medium">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Cited Page</span>
          </div>
        )}
      </div>

      {/* PDF View Mock Canvas */}
      <div className="flex-1 bg-slate-950 p-4 overflow-y-auto flex items-center justify-center">
        <div
          style={{ transform: `scale(${zoom / 100})`, transformOrigin: 'top center' }}
          className="w-full max-w-sm aspect-[1/1.414] bg-white text-slate-900 rounded shadow-2xl p-6 transition-transform relative select-none"
        >
          <div className="text-[10px] text-slate-400 uppercase tracking-widest border-b pb-1 mb-3 flex justify-between">
            <span>{activePaper.filename}</span>
            <span>Page {currentPage}</span>
          </div>

          <div className="font-serif text-xs font-bold text-slate-900 mb-2">
            Section {currentPage}: Experimental Evaluation & Architecture
          </div>

          <div className="space-y-2 text-[10px] leading-relaxed text-slate-700 font-serif">
            <p>
              In this section, we present the empirical results on multi-paper evaluation.
              The experimental methodology was executed across 15 standard academic benchmarks.
            </p>
            <div className={`p-2 rounded border transition ${
              targetPage === currentPage
                ? 'bg-emerald-50 border-emerald-400 ring-2 ring-emerald-300'
                : 'bg-slate-50 border-slate-200'
            }`}>
              <div className="text-[9px] font-bold text-slate-600 mb-0.5">
                {targetPage === currentPage ? '⚡ Grounded Evidence Chunk' : 'Source Evidence Block'}
              </div>
              <p className="italic text-slate-800">
                &ldquo;The proposed framework achieves superior grounded citation retrieval with zero external API dependencies.&rdquo;
              </p>
            </div>
            <p>
              Evaluation scores confirm significant reduction in hallucination rates compared to baseline general-purpose LLMs.
            </p>
          </div>

          <div className="absolute bottom-3 right-4 text-[9px] text-slate-400 font-mono">
            {currentPage}
          </div>
        </div>
      </div>
    </div>
  );
};
