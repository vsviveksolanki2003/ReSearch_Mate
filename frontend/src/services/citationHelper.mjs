/**
 * Helper for generating and interacting with citation badges.
 */
export function createCitationBadge(citation) {
  return {
    displayText: `[p. ${citation.page_number}]`,
    targetPage: citation.page_number,
    paperId: citation.paper_id,
    quote: citation.quote,
    confidence: citation.confidence || 1.0
  };
}
