import React, { useRef } from 'react';
import { FileText, Upload, CheckSquare, Square, Layers, UserCircle, LogOut } from 'lucide-react';
import { PaperItem } from '../services/api';
import { UserProfile } from '../services/auth';

interface PaperSidebarProps {
  papers: PaperItem[];
  selectedPaperIds: string[];
  onToggleSelect: (id: string) => void;
  onSelectActivePaper: (paper: PaperItem) => void;
  activePaperId: string | null;
  onUpload: (file: File) => void;
  isUploading: boolean;
  user: UserProfile | null;
  onOpenAuth: () => void;
  onLogout: () => void;
}

export const PaperSidebar: React.FC<PaperSidebarProps> = ({
  papers,
  selectedPaperIds,
  onToggleSelect,
  onSelectActivePaper,
  activePaperId,
  onUpload,
  isUploading,
  user,
  onOpenAuth,
  onLogout,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  return (
    <div className="w-80 h-full bg-slate-900 border-r border-slate-800 flex flex-col p-4">
      <div className="flex items-center gap-2 mb-6">
        <Layers className="w-6 h-6 text-emerald-400" />
        <h1 className="text-lg font-bold text-slate-100">ReSearch_Mate</h1>
      </div>

      <div className="mb-4">
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept="application/pdf"
          className="hidden"
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={isUploading}
          className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white font-medium rounded-lg flex items-center justify-center gap-2 transition"
        >
          <Upload className="w-4 h-4" />
          {isUploading ? 'Extracting & Indexing...' : 'Upload Research PDF'}
        </button>
      </div>

      <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">
        Indexed Papers ({papers.length})
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {papers.length === 0 ? (
          <div className="text-sm text-slate-500 py-6 text-center border border-dashed border-slate-800 rounded-lg">
            No research papers uploaded yet. Upload PDFs to begin.
          </div>
        ) : (
          papers.map((p) => {
            const isSelected = selectedPaperIds.includes(p.id);
            const isActive = activePaperId === p.id;
            return (
              <div
                key={p.id}
                onClick={() => onSelectActivePaper(p)}
                className={`p-3 rounded-lg border cursor-pointer transition ${
                  isActive
                    ? 'bg-slate-800 border-emerald-500'
                    : 'bg-slate-950 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-start gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onToggleSelect(p.id);
                    }}
                    className="mt-0.5 text-slate-400 hover:text-emerald-400"
                  >
                    {isSelected ? (
                      <CheckSquare className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <Square className="w-4 h-4" />
                    )}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-slate-200 truncate">
                      {p.title}
                    </div>
                    <div className="text-xs text-slate-400 mt-1 flex items-center gap-2">
                      <FileText className="w-3.5 h-3.5" />
                      <span>{p.total_pages} pages</span>
                      <span>•</span>
                      <span>{p.chunk_count} chunks</span>
                    </div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      <div className="pt-4 border-t border-slate-800">
        {user ? (
          <div className="flex items-center justify-between text-xs text-slate-300">
            <div className="flex items-center gap-2 min-w-0">
              <UserCircle className="w-4 h-4 text-emerald-400 shrink-0" />
              <div className="truncate">
                <div className="font-semibold text-slate-200">{user.username}</div>
                <div className="text-[10px] text-slate-400">{user.workspace_id}</div>
              </div>
            </div>
            <button
              onClick={onLogout}
              className="p-1 hover:text-rose-400 text-slate-500 rounded transition"
              title="Sign Out"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <button
            onClick={onOpenAuth}
            className="w-full py-1.5 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg flex items-center justify-center gap-1.5 transition"
          >
            <UserCircle className="w-3.5 h-3.5 text-emerald-400" />
            <span>Sign In / Workspace</span>
          </button>
        )}
        <div className="mt-2 text-[10px] text-slate-500 text-center">
          Offline • pgvector • Ollama 8B
        </div>
      </div>
    </div>
  );
};
