import logging
import os
import uuid

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session

from app.models.db import get_session
from app.models.analysis import Analysis
from app.services.extract import extract_text


logger = logging.getLogger(__name__)
router = APIRouter()
UPLOAD_DIR = "uploads"

MAX_BYTES = 30 * 1024 * 1024  # 30 MB

os.makedirs(UPLOAD_DIR, exist_ok=True)


def _save_with_limit(upfile: UploadFile, dest_path: str):
    total = 0
    with open(dest_path, "wb") as dest:
        while True:
            chunk = upfile.file.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > MAX_BYTES:
                try:
                    dest.close()
                    os.remove(dest_path)
                except Exception:  # pragma: no cover - cleanup best effort
                    pass
                raise HTTPException(status_code=413, detail="Archivo supera 30 MB")
            dest.write(chunk)


@router.post("/upload")
def upload(file: UploadFile = File(...), session: Session = Depends(get_session)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(400, detail="Formato no soportado (usa .pdf o .docx)")
    try:
        dest = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
        _save_with_limit(file, dest)
        if hasattr(file.file, "seek"):
            file.file.seek(0)

        text = extract_text(dest)
        if not text or len(text) < 20:
            raise HTTPException(422, detail="No se pudo extraer texto (PDF escaneado ilegible o corrupto)")

        analysis = Analysis(filename=file.filename, text=text)
        session.add(analysis)
        session.commit()
        session.refresh(analysis)
        return {"id": analysis.id}
    except HTTPException as exc:
        logger.warning("Upload error: %s", exc.detail)
        raise
    except Exception as exc:  # pragma: no cover - unexpected runtime errors
        logger.exception("Fallo inesperado en /upload")
        raise HTTPException(500, detail=f"Fallo interno en subida: {type(exc).__name__}")
