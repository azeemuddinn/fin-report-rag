"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);
    setUploadStatus("Uploading and indexing...");

    try {
      const res = await fetch("http://127.0.0.1:8000/upload-pdf/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setUploadStatus(`Success! Stored ${data.chunks_stored} chunks.`);
      } else {
        setUploadStatus(`Error: ${data.detail || "Upload failed"}`);
      }
    } catch (err) {
      setUploadStatus("Error connecting to backend server.");
    }
  };

  const handleAsk = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, k: 4 }),
      });
      const data = await res.json();
      if (res.ok) {
        setAnswer(data.answer);
        setSources(data.sources);
      } else {
        setAnswer(`Error: ${data.detail || "Query failed"}`);
      }
    } catch (err) {
      setAnswer("Error connecting to backend server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="max-w-4xl mx-auto p-6 font-sans">
      <h1 className="text-3xl font-bold mb-6 text-gray-900">
        Financial Report RAG Assistant
      </h1>

      {/* Upload Section */}
      <div className="bg-white p-6 rounded-lg shadow-md mb-8 border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">1. Upload PDF Report</h2>
        <form onSubmit={handleUpload} className="flex gap-4 items-center">
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded-md font-medium hover:bg-blue-700 transition"
          >
            Upload
          </button>
        </form>
        {uploadStatus && (
          <p className="mt-3 text-sm text-gray-600">{uploadStatus}</p>
        )}
      </div>

      {/* Query Section */}
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
        <h2 className="text-xl font-semibold mb-4">2. Ask Questions</h2>
        <form onSubmit={handleAsk} className="flex gap-4 mb-6">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What is the financial summary?"
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-green-600 text-white px-6 py-2 rounded-md font-medium hover:bg-green-700 transition disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>

        {answer && (
          <div className="mt-6 p-4 bg-gray-50 rounded-md border border-gray-200">
            <h3 className="font-semibold text-gray-800 mb-2">Answer:</h3>
            <p className="text-gray-700 whitespace-pre-wrap">{answer}</p>

            {sources.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-200">
                <h4 className="text-sm font-semibold text-gray-600 mb-1">
                  Sources:
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-500">
                  {sources.map((src, idx) => (
                    <li key={idx}>{src}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
