# main.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi import Body, Form
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from services.generator_service import generate_with_llm
from services.summarizer_service import summarize_pdf_with_llm
from services.file_export import export_as_docx, export_as_pdf
from services.debugger import analyze_python_code
from utils.pdf_text_extractor import extract_text_by_page_bytes
import io

app = FastAPI(title="Waid - Write with Help of AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Waid"}

# Document generation endpoint
@app.post("/generate")
async def api_generate(doc_type: str = Form(...), prompt: str = Form("")):
    try:
        result = generate_with_llm(prompt, doc_type)  # fixed arg order
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Export generated doc as docx or pdf
@app.post("/generate/export")
async def api_generate_export(doc_type: str = Form(...), prompt: str = Form(""), fmt: str = Form("docx")):
    result = generate_with_llm(prompt, doc_type)  # fixed arg order
    if fmt.lower() == "docx":
        data = export_as_docx(result)
        return StreamingResponse(
            io.BytesIO(data),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={doc_type}.docx"}
        )
    else:
        data = export_as_pdf(result)
        return StreamingResponse(
            io.BytesIO(data),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={doc_type}.pdf"}
        )

# Summarize uploaded PDF
@app.post("/summarize")
async def api_summarize(
    file: UploadFile = File(...),
    by_page: bool = Form(False),
    bullets: bool = Form(False),
    insights: bool = Form(False)
):
    content = await file.read()
    pages = extract_text_by_page_bytes(content)
    if isinstance(pages, dict) and pages.get("error"):
        raise HTTPException(status_code=400, detail=pages["error"])

    # Determine summarization mode
    if bullets:
        mode = "bullets"
    elif insights:
        mode = "insights"
    else:
        mode = "summary"

    if by_page:
        summaries = []
        for p in pages:
            summaries.append(summarize_pdf_with_llm(p, mode=mode))
        return {"by_page": summaries}
    else:
        full_text = "\n".join(pages)
        return {"summary": summarize_pdf_with_llm(full_text, mode=mode)}

# Debugging endpoint
@app.post("/debug")
async def api_debug(file: UploadFile = File(...)):
    content = await file.read()
    code_str = content.decode("utf-8", errors="replace")
    result = analyze_python_code(code_str)
    return result



@app.post("/generate/export_from_json")
async def export_from_json(
    content: dict = Body(...),
    fmt: str = Form("docx")
):
    if fmt.lower() == "docx":
        data = export_as_docx(content)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ext = "docx"
    else:
        data = export_as_pdf(content)
        media_type = "application/pdf"
        ext = "pdf"

    return StreamingResponse(
        io.BytesIO(data),
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename=document.{ext}"}
    )
