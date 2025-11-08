import logging
import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session

from app.models.analysis import Analysis
from app.models.db import get_session
from app.services.extract import extract_text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_FILE_SIZE = 30 * 1024 * 1024

logger = logging.getLogger(__name__)

@router.post("/upload")
def upload(file: UploadFile = File(...), session: Session = Depends(get_session)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(400, "Formato no soportado")
    content = file.file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande (máx. 30 MB)")

    path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    with open(path, "wb") as f:
        f.write(content)

    try:
        text = extract_text(path)
    except Exception as exc:
        logger.exception("Error extrayendo texto del archivo %s", file.filename)
        raise HTTPException(status_code=422, detail=f"No se pudo extraer el texto: {exc}") from exc
    analysis = Analysis(filename=file.filename, text=text)
    session.add(analysis); session.commit(); session.refresh(analysis)
    return {"id": analysis.id}
