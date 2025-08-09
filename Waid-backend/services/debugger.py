import subprocess
import tempfile
from pathlib import Path

def analyze_python_code(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # First check syntax
        syntax_check = subprocess.run(
            ["python", "-m", "py_compile", tmp_path],
            capture_output=True,
            text=True
        )

        if syntax_check.returncode != 0:
            error_output = syntax_check.stderr.strip()
            issue_type = "Syntax Error"
        else:
            # Then check for runtime errors
            runtime_check = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True
            )

            if runtime_check.returncode != 0:
                error_output = runtime_check.stderr.strip()
                issue_type = "Runtime Error"
            else:
                return {
                    "errors": "✅ No syntax or runtime errors found.",
                    "fixed_code": code
                }

        # If error found, use LLM to fix
        prompt = f"""
You are a Python debugging assistant. The following code has a {issue_type}:

```python
{code}
```

The error message is:

```
{error_output}
```

Please fix the code and return the corrected version only.
"""

        llm_response = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "errors": error_output,
            "fixed_code": llm_response.stdout.strip()
        }

    except Exception as e:
        return {
            "errors": f"Exception during analysis: {str(e)}",
            "fixed_code": ""
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)