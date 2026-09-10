import type {
  ChatResponse,
  RepositoryCreateResponse,
  RepositoryStatusResponse,
} from "../types";

const API_BASE = "/api";

export async function createRepository(url: string): Promise<RepositoryCreateResponse> {
  const res = await fetch(`${API_BASE}/repositories`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `request failed: ${res.status}`);
  }
  return res.json();
}

export async function getRepositoryStatus(repoId: string): Promise<RepositoryStatusResponse> {
  const res = await fetch(`${API_BASE}/repositories/${repoId}/status`);
  if (!res.ok) throw new Error(`request failed: ${res.status}`);
  return res.json();
}

export async function askQuestion(repoId: string, question: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat/${repoId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail ?? `request failed: ${res.status}`);
  }
  return res.json();
}
