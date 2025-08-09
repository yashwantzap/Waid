# backend/services/generator_service.py
import subprocess
import json
import time
    
def run_ollama(prompt: str, model: str = "mistral", timeout: int = 300) -> str:
    start = time.time()
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout
        )
        output = (result.stdout or result.stderr).strip()
    except Exception as e:
        output = f"Error running Ollama: {e}"
    end = time.time()
    print(f"[DEBUG] Ollama call took {end - start:.2f} seconds")
    return output


def get_default_template(doc_type: str) -> dict:
    """Default doc template if generation fails."""
    return {
        "title": f"{doc_type} Template",
        "sections": [
            {"heading": "Introduction", "content": f"Intro for {doc_type}."},
            {"heading": "Body", "content": "Main content goes here."},
            {"heading": "Conclusion", "content": "Closing remarks."}
        ]
    }


def generate_with_llm(custom_prompt: str, doc_type: str) -> dict:
    """Generate structured doc content with Ollama LLM."""
    prompt = f"""
You are a document planning assistant.
Document type: {doc_type}
Instructions: {custom_prompt}

Produce a JSON object with:
- title: string
- sections: array of objects with 'heading' and 'content'

Return only valid JSON.
"""
    response = run_ollama(prompt, timeout=300)
    try:
        # Extract first JSON object from response
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            parsed = json.loads(response[start:end+1])
            if "title" in parsed and "sections" in parsed:
                return parsed
    except Exception:
        pass

    return {
        "title": "Document Generation Error",
        "sections": [
            {"heading": "LLM Output (raw)", "content": response}
        ]
    }
