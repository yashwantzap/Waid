import React, { useState } from "react";

 // We'll create this file next

function RenderContent({ content }) {
  if (typeof content === "string") {
    return <p className="content-text">{content}</p>;
  } else if (typeof content === "object" && content !== null) {
    return (
      <ul className="content-list">
        {Object.entries(content).map(([key, value]) => (
          <li key={key}>
            <strong>{key}:</strong>{" "}
            {typeof value === "object" ? (
              <RenderContent content={value} />
            ) : (
              value?.toString()
            )}
          </li>
        ))}
      </ul>
    );
  } else {
    return null;
  }
}

export default function DocGenerator() {
  const [docType, setDocType] = useState("Resume");
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [downloading, setDownloading] = useState(false);

  async function generateDoc(e) {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append("doc_type", docType);
    formData.append("prompt", prompt);

    try {
      const res = await fetch("http://localhost:8000/generate", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error(`HTTP error ${res.status}`);

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Unknown error");
    }
    setLoading(false);
  }

  async function downloadFileFromJson(format) {
    setDownloading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/generate/export_from_json", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: result, fmt: format }),
      });

      if (!res.ok) throw new Error(`Download failed: ${res.status}`);

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${docType}.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Unknown error during download");
    }
    setDownloading(false);
  }

  return (
    <div className="container">
      <h2 className="title">Document Generator</h2>

      <form onSubmit={generateDoc} className="form">
        <label className="label">Document Type:</label>
        <input
          type="text"
          value={docType}
          onChange={(e) => setDocType(e.target.value)}
          required
          className="input"
          placeholder="Resume"
        />

        <label className="label">Prompt / Instructions:</label>
        <textarea
          rows={5}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="generate a resume for a painter"
          className="textarea"
        />

        <button type="submit" className="btn" disabled={loading || downloading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </form>

      {loading && (
        <div className="loading-container">
          <div className="spinner" />
          <p className="loading-text">Generating document, please wait...</p>
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {result && !error && (
        <div className="result">
          <h3 className="result-title">Result</h3>

          {result.sections && Array.isArray(result.sections) ? (
            result.sections.map((section, i) => (
              <div key={i} className="section">
                <h4 className="section-heading">{section.heading}</h4>
                <RenderContent content={section.content} />
              </div>
            ))
          ) : (
            <pre className="preformatted">{JSON.stringify(result, null, 2)}</pre>
          )}

          <div className="download-buttons">
            <button
              onClick={() => downloadFileFromJson("docx")}
              disabled={downloading}
              className="btn download-btn"
            >
              {downloading ? "Downloading DOCX..." : "Download as DOCX"}
            </button>

            <button
              onClick={() => downloadFileFromJson("pdf")}
              disabled={downloading}
              className="btn download-btn"
            >
              {downloading ? "Downloading PDF..." : "Download as PDF"}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
