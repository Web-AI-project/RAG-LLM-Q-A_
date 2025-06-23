import React, { useState } from "react";

export default function ChatInterface() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    setLoading(true);
    setResponse("");
    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setResponse(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      setResponse("Error fetching response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={handleSend} disabled={loading}>
        {loading ? "Loading..." : "Ask"}
      </button>
      <div>
        <p><strong>Answer:</strong> {response}</p>
        <p><strong>Sources:</strong></p>
        <ul>{sources.map((src, idx) => <li key={idx}>{src}</li>)}</ul>
      </div>
    </div>
  );
}
