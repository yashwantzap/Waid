from agent.doc_agent import generate_with_llm, get_default_template, summarize_pdf_with_llm
import fitz
import io

def generate_document(doc_type, custom_prompt):
    if custom_prompt.strip():
        return generate_with_llm(custom_prompt, doc_type)
    else:
        return get_default_template(doc_type)


def summarize_uploaded_pdf(uploaded_pdf):
    try:
        pdf_bytes = uploaded_pdf.read()
        doc = fitz.open(stream=io.BytesIO(pdf_bytes), filetype="pdf")
        pdf_text = "".join([page.get_text() for page in doc])
        doc.close()

        if not pdf_text.strip():
            return None, None, None, "No text found in PDF. It may be a scanned image."

        summary = summarize_pdf_with_llm(pdf_text, mode="summary")
        bullets = summarize_pdf_with_llm(pdf_text, mode="bullets")
        insights = summarize_pdf_with_llm(pdf_text, mode="insights")
        return summary, bullets, insights, None
    except Exception as e:
        return None, None, None, str(e)
