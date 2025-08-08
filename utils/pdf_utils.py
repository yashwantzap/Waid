from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import fitz  # PyMuPDF

def save_as_pdf(doc_data, filename="output/document.pdf"):
    os.makedirs("output", exist_ok=True)
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(doc_data.get("title", "Untitled"), styles["Title"]))
    elements.append(Spacer(1, 12))

    for section in doc_data.get("sections", []):
        elements.append(Paragraph(section.get("heading", ""), styles["Heading2"]))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(section.get("content", ""), styles["BodyText"]))
        elements.append(Spacer(1, 12))

    doc.build(elements)
    return filename

def extract_text_by_page(file) -> list:
    """Extracts text from PDF page by page."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return [page.get_text().strip() for page in doc]
