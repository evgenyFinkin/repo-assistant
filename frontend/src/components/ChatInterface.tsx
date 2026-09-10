import { useState } from "react";

import { askQuestion } from "../services/api";
import type { ChatMessage } from "../types";

interface Props {
  repoId: string;
}

// Story 3: Chat Interface, Story 4: Source-Grounded Answers.
export default function ChatInterface({ repoId }: Props) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [question, setQuestion] = useState("");
  const [retrieving, setRetrieving] = useState(false);

  async function handleSend() {
    if (!question.trim()) return;
    const userMessage: ChatMessage = { role: "user", content: question };
    setMessages((prev) => [...prev, userMessage]);
    setQuestion("");
    setRetrieving(true);
    try {
      const res = await askQuestion(repoId, userMessage.content);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.answer, sources: res.sources },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${(err as Error).message}` },
      ]);
    } finally {
      setRetrieving(false);
    }
  }

  function handleClear() {
    setMessages([]);
  }

  return (
    <div>
      <div>
        {messages.map((m, i) => (
          <div key={i} data-role={m.role}>
            <p>{m.content}</p>
            {m.sources?.map((s, j) => (
              <div key={j}>
                <code>
                  {s.file_path}:{s.line_start}-{s.line_end}
                </code>{" "}
                (similarity: {s.similarity.toFixed(2)})
                <pre>{s.snippet}</pre>
              </div>
            ))}
          </div>
        ))}
        {retrieving && <p>retrieving...</p>}
      </div>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about this repo..."
      />
      <button onClick={handleSend} disabled={retrieving}>
        Send
      </button>
      <button onClick={handleClear} disabled={messages.length === 0}>
        Clear
      </button>
    </div>
  );
}
