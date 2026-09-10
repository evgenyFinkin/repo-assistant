import { useState } from "react";

interface Props {
  onSubmit: (url: string) => void;
  loading: boolean;
}

// Story 1: Accept Repository URL — input + validation + loading state.
const GITHUB_URL_RE = /^https:\/\/github\.com\/[\w.-]+\/[\w.-]+\/?$/;

export default function RepoUrlForm({ onSubmit, loading }: Props) {
  const [url, setUrl] = useState("");
  const [error, setError] = useState<string | null>(null);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!GITHUB_URL_RE.test(url.trim())) {
      setError("Enter a valid public GitHub repo URL, e.g. https://github.com/owner/repo");
      return;
    }
    setError(null);
    onSubmit(url.trim());
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://github.com/owner/repo"
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
      {error && <p role="alert">{error}</p>}
    </form>
  );
}
