import pdfplumber
import docx
from fastapi import UploadFile

async def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        return extract_pdf(file)
    elif file.filename.endswith(".docx"):
        return extract_docx(file)
    else:
        return (await file.read()).decode("utf-8")

def extract_pdf(file):
    with pdfplumber.open(file.file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def extract_docx(file):
    doc = docx.Document(file.file)
    return "\n".join(p.text for p in doc.paragraphs)
