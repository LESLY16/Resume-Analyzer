import io
import fitz  # PyMuPDF
import docx
from docx.opc.exceptions import PackageNotFoundError
from fastapi import UploadFile, HTTPException

from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image


async def parse_file(file: UploadFile) -> str:
    filename = (file.filename or "").lower()
    content = await file.read()

    # ---------------------------------------------------------
    # PDF EXTRACTION (Text → OCR fallback)
    # ---------------------------------------------------------
    if filename.endswith(".pdf"):

        # 1) Try normal text extraction via PyMuPDF
        try:
            pdf_doc: fitz.Document = fitz.open(stream=content, filetype="pdf")
            text_parts: list[str] = []

            for page_number in range(pdf_doc.page_count):
                page = pdf_doc.load_page(page_number)
                page_text = page.get_text("text")

                if isinstance(page_text, str) and page_text.strip():
                    text_parts.append(page_text)

            extracted_text = "".join(text_parts).strip()

            if extracted_text:
                return extracted_text

        except Exception:
            pass

        # 2) OCR fallback for scanned PDFs
        try:
            images = convert_from_bytes(content)
            ocr_text_parts: list[str] = []

            for img in images:
                if not isinstance(img, Image.Image):
                    img = img.convert("RGB")

                ocr_text = pytesseract.image_to_string(img)

                if isinstance(ocr_text, str) and ocr_text.strip():
                    ocr_text_parts.append(ocr_text)

            ocr_text = "\n".join(ocr_text_parts).strip()

            if ocr_text:
                return ocr_text

            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from PDF (even with OCR)."
            )

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted PDF file."
            )

    # ---------------------------------------------------------
    # DOCX EXTRACTION (paragraphs + tables)
    # ---------------------------------------------------------
    if filename.endswith(".docx"):
        try:
            word_doc = docx.Document(io.BytesIO(content))

            # Extract paragraphs
            paragraph_text = "\n".join([p.text for p in word_doc.paragraphs])

            # Extract tables
            table_text_parts: list[str] = []

            for table in word_doc.tables:
                for row in table.rows:
                    row_cells = [cell.text.strip() for cell in row.cells]
                    row_text = " | ".join([c for c in row_cells if c])
                    if row_text:
                        table_text_parts.append(row_text)

            table_text = "\n".join(table_text_parts)

            # Combine both
            combined_text = (paragraph_text + "\n" + table_text).strip()

            return combined_text

        except PackageNotFoundError:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted DOCX file."
            )

        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Unable to read DOCX file."
            )

    # ---------------------------------------------------------
    # TXT fallback
    # ---------------------------------------------------------
    try:
        return content.decode("utf-8", errors="ignore")
    except Exception:
        return str(content)
