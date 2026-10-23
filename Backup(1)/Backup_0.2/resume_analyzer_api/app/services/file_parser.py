import pdfplumber
import docx
from fastapi import UploadFile

async def extract_text(file: UploadFile) -> str:
    name = (file.filename or "").lower()

    if name.endswith(".pdf"):
        return extract_pdf(file)
    elif name.endswith(".docx"):
        return extract_docx(file)
    else:
        return (await file.read()).decode("utf-8", errors="ignore")

def extract_pdf(file):
    text = []
    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)

def extract_docx(file):
    doc = docx.Document(file.file)
    return "\n".join(p.text for p in doc.paragraphs)
