import React, { useState } from "react";



export default function PdfSummarizer() {
  const [file, setFile] = useState(null);
  const [byPage, setByPage] = useState(false);
  const [bullets, setBullets] = useState(false);
  const [insights, setInsights] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function summarizePdf(e) {
    e.preventDefault();
    if (!file) return alert("Please upload a PDF file");

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("by_page", byPage.toString());
    formData.append("bullets", bullets.toString());
    formData.append("insights", insights.toString());

    try {
      const res = await fetch("http://localhost:8000/summarize", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: err.message || "Error summarizing" });
    }
    setLoading(false);
  }

  return (
    <div className="container">
      <h2 className="title">PDF Summarizer</h2>
      <form onSubmit={summarizePdf} className="form">
        <input
          type="file"
          accept="application/pdf"
          className="input"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <br />
        <label className="label">
          <input
            type="checkbox"
            checked={byPage}
            onChange={() => setByPage(!byPage)}
          />{" "}
          Summarize by page
        </label>
        <br />
        <label className="label">
          <input
            type="checkbox"
            checked={bullets}
            onChange={() => {
              setBullets(!bullets);
              if (insights) setInsights(false);
            }}
          />{" "}
          Bullet points
        </label>
        <br />
        <label className="label">
          <input
            type="checkbox"
            checked={insights}
            onChange={() => {
              setInsights(!insights);
              if (bullets) setBullets(false);
            }}
          />{" "}
          Key insights
        </label>
        <br /><br></br>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? "Summarizing..." : "Summarize"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: 20, whiteSpace: "pre-wrap" }}>
          {result.error && <div style={{ color: "red" }}>Error: {result.error}</div>}

          {result.summary && <div><h3>Summary</h3><p>{result.summary}</p></div>}

          {result.by_page && (
            <>
              <h3>Summary by Page</h3>
              {result.by_page.map((pageSummary, i) => (
                <div key={i}>
                  <h4>Page {i + 1}</h4>
                  <p>{pageSummary}</p>
                </div>
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}
