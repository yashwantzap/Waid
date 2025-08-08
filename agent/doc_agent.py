import subprocess
import json


def run_ollama(prompt: str, model: str = "mistral", max_tokens: int = 1024) -> str:
    """
    Runs the Ollama model with the given prompt and returns the response as a string.
    Handles timeouts and decoding errors.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=1200  # ⏳ 20 minutes – safe for cold starts
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: Ollama LLM took too long to respond. Please try again after confirming the model is loaded."
    except Exception as e:
        return f"Error running Ollama: {str(e)}"


def get_default_template(doc_type: str) -> dict:
    """
    Returns a default template for a given document type.
    """
    return {
        "title": f"{doc_type} Template",
        "sections": [
            {
                "heading": f"Section 1 of {doc_type}",
                "content": "This is a default section."
            }
        ]
    }


def generate_with_llm(custom_prompt: str, doc_type: str) -> dict:
    """
    Generates a document structure using LLM based on a prompt and document type.
    Returns a dictionary with 'title' and 'sections' (list of dicts).
    """
    prompt = f"""
Act as a professional AI document generator.
Document Type: {doc_type}
Instructions: {custom_prompt}

Return output as JSON with keys:
- title: string
- sections: list of dicts with keys 'heading' and 'content'
"""
    response = run_ollama(prompt)
    try:
        parsed = json.loads(response)
        # ✅ Optional strict validation
        if "title" in parsed and "sections" in parsed:
            return parsed
        else:
            raise ValueError("Missing keys")
    except Exception:
        return {
            "title": "Document Generation Error",
            "sections": [{
                "heading": "JSON Decode Error",
                "content": response.strip()
            }]
        }


def summarize_pdf_with_llm(text: str, mode: str = "summary") -> str:
    """
    Summarizes the given text using the mode: 'summary', 'bullets', or 'insights'.
    Returns a string with the LLM response.
    """
    if not text.strip():
        return "(No content to summarize)"

    if mode == "summary":
        prompt = f"Summarize the following text:\n\n{text}"
    elif mode == "bullets":
        prompt = f"Convert the following text into bullet points:\n\n{text}"
    elif mode == "insights":
        prompt = f"Extract key insights from the following text:\n\n{text}"
    else:
        return "(Invalid summarization mode)"

    print(f"🔍 Prompt Sent to LLM ({mode}):\n{prompt[:500]}...\n")

    try:
        response = run_ollama(prompt)
        print(f"✅ LLM Response ({mode}):\n{response[:500]}...\n")
        return response.strip() or f"(No {mode} generated)"
    except Exception as e:
        print(f"❌ Error in summarize_pdf_with_llm: {e}")
        return f"(Error during {mode} generation)"
