import React, { useState } from "react";
import '../app.css';

export default function CodeDebugger() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function debugCode(e) {
    e.preventDefault();
    if (!file) return alert("Please upload a Python (.py) file");

    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/debug", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ errors: err.message || "Debugging failed" });
    }
    setLoading(false);
  }

  return (
    <div class="container">
      <h2 className="title">Python Code Debugger</h2>
      <form onSubmit={debugCode} className="form">
        <input
          type="file"
          accept=".py"
          className="input"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <br /><br />
        <button type="submit" className="btn" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Code"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Errors / Messages</h3>
          <pre
            style={{
              backgroundColor: "#eee",
              padding: 10,
              whiteSpace: "pre-wrap",
              maxHeight: 300,
              overflowY: "auto",
            }}
          >
            {result.errors}
          </pre>

          {result.fixed_code && (
            <>
              <h3>Fixed Code</h3>
              <pre
                style={{
                  backgroundColor: "#f9f9f9",
                  padding: 10,
                  whiteSpace: "pre-wrap",
                  maxHeight: 400,
                  overflowY: "auto",
                  border: "1px solid #ccc",
                }}
              >
                {result.fixed_code}
              </pre>
            </>
          )}
        </div>
      )}
    </div>
  );
}
