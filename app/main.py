import streamlit as st
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui_components import show_document_generator_ui, show_pdf_summarizer_ui, show_debugger_ui

st.set_page_config(page_title="DocuGenAI", layout="centered")
st.title("📄 DocuGenAI - Document Generator with Local LLM")
st.markdown("---")

st.sidebar.header("🧠 Choose a Mode")
mode = st.sidebar.selectbox("Select Action", ["Generate Document", "Summarize PDF","Debugger"])

if mode == "Generate Document":
    show_document_generator_ui()
elif mode == "Summarize PDF":
    show_pdf_summarizer_ui()
else:
    show_debugger_ui()
