import logging
import os
import subprocess
import tempfile

import pdfplumber
from docx import Document
from PIL import Image
import pytesseract


logger = logging.getLogger(__name__)


def clean_text(t: str) -> str:
    # quitar headers/footers repetidos y espacios raros
    import regex as re
    t = t.replace("\r", "\n")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def ocr_pdf_with_poppler(path: str, dpi: int = 200) -> str:
    # Renderiza cada página a PNG en un tmp y pasa OCR con Tesseract
    tmpdir = tempfile.mkdtemp(prefix="pliego_ocr_")
    try:
        prefix = os.path.join(tmpdir, "page")
        subprocess.run(["pdftoppm", "-png", "-r", str(dpi), path, prefix], check=True)
        texts = []
        for fname in sorted(os.listdir(tmpdir)):
            if not fname.endswith(".png"):
                continue
            fp = os.path.join(tmpdir, fname)
            texts.append(pytesseract.image_to_string(Image.open(fp), lang="spa+eng"))
        return clean_text("\n".join(texts))
    except subprocess.CalledProcessError:
        return ""
    finally:
        try:
            for f_name in os.listdir(tmpdir):
                os.remove(os.path.join(tmpdir, f_name))
            os.rmdir(tmpdir)
        except Exception:  # pragma: no cover - best effort cleanup
            pass


def extract_pdf_text(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text(x_tolerance=2, y_tolerance=2) or ""
            text += "\n"
    text = clean_text(text)
    if len(text) > 200:
        return text

    ocr_text = ocr_pdf_with_poppler(path, dpi=200)
    return clean_text(ocr_text)


def extract_docx_text(path: str) -> str:
    doc = Document(path)
    return clean_text("\n".join(p.text for p in doc.paragraphs))


def extract_text(path: str) -> str:
    try:
        if path.lower().endswith(".pdf"):
            return extract_pdf_text(path)
        if path.lower().endswith(".docx"):
            return extract_docx_text(path)
    except Exception as exc:
        logger.exception("Fallo extrayendo texto del archivo %s", path)
        raise RuntimeError("Error durante la extracción/OCR") from exc
    raise ValueError("Formato no soportado")
