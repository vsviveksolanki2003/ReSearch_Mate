/**
 * Parses raw SSE chunk data into an array of typed events.
 */
export function parseSSEChunk(rawChunk) {
  const events = [];
  const blocks = rawChunk.split('\n\n');

  for (const block of blocks) {
    if (!block.trim()) continue;

    let eventType = 'message';
    let dataStr = '';

    const lines = block.split('\n');
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        eventType = line.slice(7).trim();
      } else if (line.startsWith('data: ')) {
        dataStr = line.slice(6).trim();
      }
    }

    if (dataStr) {
      try {
        const parsed = JSON.parse(dataStr);
        events.push({ event: eventType, data: parsed });
      } catch (e) {
        events.push({ event: eventType, data: dataStr });
      }
    }
  }

  return events;
}
