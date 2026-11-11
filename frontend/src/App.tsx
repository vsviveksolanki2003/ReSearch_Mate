import React, { useState, useEffect } from 'react';
import { PaperSidebar } from './components/PaperSidebar';
import { ChatPanel } from './components/ChatPanel';
import { PDFViewerPanel } from './components/PDFViewerPanel';
import { fetchPapers, uploadPaperFile, PaperItem } from './services/api';

export const App: React.FC = () => {
  const [papers, setPapers] = useState<PaperItem[]>([]);
  const [selectedPaperIds, setSelectedPaperIds] = useState<string[]>([]);
  const [activePaper, setActivePaper] = useState<PaperItem | null>(null);
  const [targetCitationPage, setTargetCitationPage] = useState<number>(1);
  const [isUploading, setIsUploading] = useState(false);

  const loadPapers = async () => {
    const list = await fetchPapers();
    setPapers(list);
    if (list.length > 0 && !activePaper) {
      setActivePaper(list[0]);
    }
  };

  useEffect(() => {
    loadPapers();
  }, []);

  const handleToggleSelect = (id: string) => {
    setSelectedPaperIds((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const handleSelectActivePaper = (paper: PaperItem) => {
    setActivePaper(paper);
    setTargetCitationPage(1);
  };

  const handleUpload = async (file: File) => {
    setIsUploading(true);
    try {
      await uploadPaperFile(file);
      await loadPapers();
    } catch (err: any) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleNavigateCitation = (page: number, paperId: string) => {
    const matched = papers.find((p) => p.id === paperId);
    if (matched) {
      setActivePaper(matched);
    }
    setTargetCitationPage(page);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 select-none">
      <PaperSidebar
        papers={papers}
        selectedPaperIds={selectedPaperIds}
        onToggleSelect={handleToggleSelect}
        onSelectActivePaper={handleSelectActivePaper}
        activePaperId={activePaper ? activePaper.id : null}
        onUpload={handleUpload}
        isUploading={isUploading}
      />
      <ChatPanel
        selectedPaperIds={selectedPaperIds}
        onNavigateCitation={handleNavigateCitation}
      />
      <PDFViewerPanel
        activePaper={activePaper}
        targetPage={targetCitationPage}
      />
    </div>
  );
};

export default App;
