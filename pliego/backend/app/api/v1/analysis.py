from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.db import get_session
from app.models.analysis import Analysis
from app.services.parse import parse_all

router = APIRouter()

@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int, session: Session = Depends(get_session)):
    analysis = session.exec(select(Analysis).where(Analysis.id == analysis_id)).first()
    if not analysis:
        raise HTTPException(404, "No existe")
    data = parse_all(analysis.text)

    # mapear sobres -> Requirement (no persistimos todavía para rapidez)
    sobres = data.get("sobres", {})
    # construir respuesta directa
    return {
        "plazos": data.get("plazos", {}),
        "sobres": sobres,
        "criterios": data.get("criterios", []),
        "resumen": data.get("resumen", {})
    }
