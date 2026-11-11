export interface UserProfile {
  id: string;
  email: string;
  username: string;
  workspace_id: string;
}

export function getStoredUser(): UserProfile | null {
  const data = localStorage.getItem('research_mate_user');
  if (!data) return null;
  try {
    return JSON.parse(data);
  } catch {
    return null;
  }
}

export function getAuthToken(): string | null {
  return localStorage.getItem('research_mate_token');
}

export function logoutUser(): void {
  localStorage.removeItem('research_mate_user');
  localStorage.removeItem('research_mate_token');
}

export async function loginUser(email: string, password: string): Promise<UserProfile> {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(err.detail || 'Login failed');
  }
  const data = await res.json();
  localStorage.setItem('research_mate_token', data.access_token);
  localStorage.setItem('research_mate_user', JSON.stringify(data.user));
  return data.user;
}

export async function registerUser(email: string, username: string, password: string): Promise<UserProfile> {
  const res = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, username, password })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Registration failed' }));
    throw new Error(err.detail || 'Registration failed');
  }
  const data = await res.json();
  localStorage.setItem('research_mate_token', data.access_token);
  localStorage.setItem('research_mate_user', JSON.stringify(data.user));
  return data.user;
}
