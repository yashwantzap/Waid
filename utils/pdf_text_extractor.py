import fitz
from io import BytesIO

def extract_text_from_stream(stream_bytes):
    try:
        doc = fitz.open(stream=stream_bytes, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        return f"Error reading PDF: {e}"
