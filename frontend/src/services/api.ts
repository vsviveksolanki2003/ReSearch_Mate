export interface PaperItem {
  id: string;
  title: string;
  filename: string;
  total_pages: number;
  chunk_count: number;
}

export interface CitationItem {
  paper_id: string;
  paper_title: string;
  page_number: number;
  quote: string;
  confidence?: number;
}

export interface ResearchGapItem {
  area: string;
  description: string;
  potential_direction: string;
}

export async function fetchPapers(): Promise<PaperItem[]> {
  try {
    const res = await fetch('/api/papers');
    if (!res.ok) return [];
    return await res.json();
  } catch (err) {
    console.error('Failed to fetch papers:', err);
    return [];
  }
}

export async function uploadPaperFile(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('/api/papers/upload', {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Upload failed');
  }
  return await res.json();
}
