/**
 * Helper for authorization header formatting.
 */
export function formatAuthHeader(token) {
  if (!token) return '';
  return `Bearer ${token}`;
}
