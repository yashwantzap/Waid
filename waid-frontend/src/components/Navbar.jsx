import React from "react";
import "./navbar.css"

export default function Navbar({ activePage, onNavigate }) {
  return (
    <nav className="navbar">
      <div className="navbar-logo">Waid AI</div>
      <div className="navbar-buttons">
        <button
          className={`nav-btn ${activePage === "generate" ? "active" : ""}`}
          onClick={() => onNavigate("generate")}
        >
          Document Generator
        </button>
        <button
          className={`nav-btn ${activePage === "summarize" ? "active" : ""}`}
          onClick={() => onNavigate("summarize")}
        >
          PDF Summarizer
        </button>
        <button
          className={`nav-btn ${activePage === "debug" ? "active" : ""}`}
          onClick={() => onNavigate("debug")}
        >
          Python Debugger
        </button>
      </div>
    </nav>
  );
}
