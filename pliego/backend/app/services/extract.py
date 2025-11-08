import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
from pypdf import PdfReader


def clean_text(t: str) -> str:
    # quitar headers/footers repetidos y espacios raros
    import regex as re
    t = t.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def extract_pdf_text(path: str) -> str:
    # intenta texto directo
    text = ""
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            text += p.extract_text(x_tolerance=2, y_tolerance=2) or ""
            text += "\n"
    if text and len(text.strip()) > 200:
        return clean_text(text)

    # fallback OCR página a página (rápido pero robusto)
    reader = PdfReader(path)
    ocr_text = []
    for i in range(len(reader.pages)):
        with pdfplumber.open(path) as pdf:
            img = pdf.pages[i].to_image(resolution=200).original
        ocr_text.append(pytesseract.image_to_string(Image.fromarray(img)))
    return clean_text("\n".join(ocr_text))


def extract_docx_text(path: str) -> str:
    doc = Document(path)
    return clean_text("\n".join(p.text for p in doc.paragraphs))


def extract_text(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return extract_pdf_text(path)
    if path.lower().endswith(".docx"):
        return extract_docx_text(path)
    raise ValueError("Formato no soportado")
