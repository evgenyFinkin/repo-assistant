import { useState } from "react";

import ChatInterface from "../components/ChatInterface";
import RepoUrlForm from "../components/RepoUrlForm";
import { createRepository, getRepositoryStatus } from "../services/api";

export default function Home() {
  const [repoId, setRepoId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(url: string) {
    setLoading(true);
    setError(null);
    try {
      const { id } = await createRepository(url);
      // TODO: poll getRepositoryStatus until "ready"/"failed" instead of
      // assuming immediate readiness (Story 1 loading state).
      await getRepositoryStatus(id);
      setRepoId(id);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <h1>repo-assistant</h1>
      <RepoUrlForm onSubmit={handleSubmit} loading={loading} />
      {error && <p role="alert">{error}</p>}
      {repoId && <ChatInterface repoId={repoId} />}
    </main>
  );
}
