export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function getDrafts(payload: any, userId: string) {
  const res = await fetch(`${API_URL}/drafts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Id': userId,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createPersona(payload: any, userId: string) {
  const res = await fetch(`${API_URL}/persona`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Id': userId,
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function sendFeedback(payload: any, userId: string) {
  const res = await fetch(`${API_URL}/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-Id': userId,
    },
    body: JSON.stringify(payload),
  });
  return res.ok;
}
