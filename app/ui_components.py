import streamlit as st
import io
from docx import Document
from generators import generate_document, summarize_uploaded_pdf
from file_utils import export_as_docx, export_as_pdf
from constants import DOCUMENT_TYPES
from agent.code_debugger import analyze_python_code


def show_debugger_ui():
    st.header("🐞 Python Code Debugger")
    uploaded_file = st.file_uploader("Upload a Python (.py) file to debug", type=["py"])

    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
        st.text_area("📄 Uploaded Code", value=code, height=300)

        if st.button("🧪 Analyze & Fix"):
            with st.spinner("Analyzing code with LLM..."):
                result = analyze_python_code(code)

            if "error" in result:
                st.error("❌ Error during analysis")
                st.code(result["error"])
            else:
                st.success("✅ Analysis Complete")
                st.markdown("### 🐛 Errors Found:")
                st.code(result.get("errors", "No errors found"))

                st.markdown("### 🛠️ Fixed Code:")
                st.code(result.get("fixed_code", ""))

                st.download_button(
                    label="💾 Download Fixed Code",
                    data=result["fixed_code"],
                    file_name="fixed_code.py",
                    mime="text/x-python"
                )

def show_document_generator_ui():
    doc_type = st.selectbox("📄 Document Type", DOCUMENT_TYPES)

    if doc_type == "Other":
        doc_type = st.text_input("Enter custom document type:")

    custom_prompt = st.text_area("🛠️ Custom Instructions", height=200)

    if st.button("🚀 Generate"):
        with st.spinner("🔍 Generating document using LLM..."):
            try:
                result = generate_document(doc_type, custom_prompt)

                st.success("✅ Document Generated")
                st.markdown(f"### 📝 {result['title']}")
                full_doc = f"# {result['title']}\n\n"

                for section in result["sections"]:
                    st.markdown(f"#### {section['heading']}")
                    st.write(section["content"])
                    full_doc += f"## {section['heading']}\n{section['content']}\n\n"

                download_format = st.selectbox("📤 Select Download Format", ["DOCX", "PDF"])

                if download_format == "DOCX":
                    doc_io = export_as_docx(result)
                    st.download_button(
                        label="💾 Download DOCX",
                        data=doc_io,
                        file_name=f"{doc_type}_document.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                else:
                    pdf_io = export_as_pdf(result)
                    st.download_button(
                        label="💾 Download PDF",
                        data=pdf_io,
                        file_name=f"{doc_type}_document.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error(f"❌ Document generation failed: {e}")


def show_pdf_summarizer_ui():
    uploaded_pdf = st.file_uploader("📄 Upload a PDF for summarization", type=["pdf"])

    if uploaded_pdf is not None:
        summary, bullets, insights, error = summarize_uploaded_pdf(uploaded_pdf)

        if error:
            st.error(f"❌ {error}")
        else:
            st.markdown("## 📚 Summary:")
            st.write(summary)

            st.markdown("## 🔹 Bullet Points:")
            st.write(bullets)

            st.markdown("## 💡 Key Insights:")
            st.write(insights)
