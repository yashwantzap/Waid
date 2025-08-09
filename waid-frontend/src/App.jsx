import React, { useState } from "react";
import Navbar from "./components/Navbar";
import DocGenerator from "./components/DocGenerator";
import PdfSummarizer from "./components/PdfSummarizer";
import PythonDebugger from "./components/CodeDebugger";
import "./app.css";


function App() {
  const [page, setPage] = useState("generate");

  return (
    <>
      <Navbar activePage={page} onNavigate={setPage} />
      <main>
        {page === "generate" && <DocGenerator />}
        {page === "summarize" && <PdfSummarizer />}
        {page === "debug" && <PythonDebugger />}
      </main>
    </>
  );
}

export default App;
