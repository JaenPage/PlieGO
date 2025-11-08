from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session
import os, uuid
from app.models.db import get_session
from app.models.analysis import Analysis
from app.services.extract import extract_text

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload(file: UploadFile = File(...), session: Session = Depends(get_session)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(400, "Formato no soportado")
    path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}{ext}")
    with open(path, "wb") as f:
        f.write(file.file.read())
    text = extract_text(path)
    analysis = Analysis(filename=file.filename, text=text)
    session.add(analysis); session.commit(); session.refresh(analysis)
    return {"id": analysis.id}
