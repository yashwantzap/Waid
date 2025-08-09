import io
from PyPDF2 import PdfReader

def extract_text_by_page_bytes(file_bytes: bytes) -> list[str]:
    """
    Extract text from each page of a PDF given its bytes.
    
    Args:
        file_bytes (bytes): The PDF file content in bytes.

    Returns:
        list[str]: A list where each item is the text from one page.
    """
    pages_text = []
    try:
        pdf_stream = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_stream)

        for page in reader.pages:
            text = page.extract_text() or ""
            pages_text.append(text.strip())
    except Exception as e:
        raise RuntimeError(f"Error reading PDF: {e}")

    return pages_text
