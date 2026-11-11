/**
 * Helper to generate literature review export URLs and download triggers.
 */
export function createExportUrl(topic, format = 'markdown') {
  const encTopic = encodeURIComponent(topic || 'Research Synthesis');
  return `/api/chat/export?format=${format}&topic=${encTopic}`;
}

export function triggerDownload(url, filename) {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
