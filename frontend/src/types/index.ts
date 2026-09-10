// Mirrors backend/app/models/schemas.py — keep in sync.

export type AnalysisStatus =
  | "pending"
  | "cloning"
  | "parsing"
  | "embedding"
  | "ready"
  | "failed";

export interface RepositoryCreateResponse {
  id: string;
  status: AnalysisStatus;
}

export interface RepositoryStatusResponse {
  id: string;
  status: AnalysisStatus;
  error?: string | null;
  files_indexed?: number | null;
}

export interface SourceReference {
  file_path: string;
  line_start: number;
  line_end: number;
  snippet: string;
  similarity: number;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  sources?: SourceReference[];
}

export interface ChatResponse {
  answer: string;
  sources: SourceReference[];
}
