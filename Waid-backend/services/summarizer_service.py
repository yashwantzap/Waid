# backend/services/summarizer_service.py
import subprocess

def run_ollama(prompt: str, model: str = "mistral", timeout: int = 120) -> str:
    """Call local Ollama for summarization."""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout
        )
        return (result.stdout or result.stderr).strip()
    except subprocess.TimeoutExpired:
        return "Error: Ollama LLM timed out."
    except Exception as e:
        return f"Error running Ollama: {e}"


def summarize_pdf_with_llm(text: str, mode: str = "summary") -> str:
    """
    Summarizes PDF text based on mode:
    - summary → short paragraph
    - bullets → bullet points
    - insights → key takeaways
    """
    if not text.strip():
        return "(No content)"

    if mode == "summary":
        prompt = f"Summarize the following text concisely:\n\n{text}"
    elif mode == "bullets":
        prompt = f"Convert the following text into concise bullet points:\n\n{text}"
    elif mode == "insights":
        prompt = f"Extract the key insights from the following text:\n\n{text}"
    else:
        return "(Invalid mode)"

    return run_ollama(prompt, timeout=300)
