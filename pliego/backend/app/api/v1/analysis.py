from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select

from app.models.analysis import Analysis
from app.models.criterion import Criterion
from app.models.db import get_session
from app.models.requirement import Requirement
from app.services.parse import parse_all

router = APIRouter()


def _delete_previous_data(session: Session, analysis_id: int) -> None:
    existing_requirements = session.exec(
        select(Requirement).where(Requirement.analysis_id == analysis_id)
    ).all()
    for req in existing_requirements:
        session.delete(req)

    existing_criteria = session.exec(
        select(Criterion).where(Criterion.analysis_id == analysis_id)
    ).all()
    for criterion in existing_criteria:
        session.delete(criterion)


@router.post("/analysis/{analysis_id}/persist")
def persist_analysis(analysis_id: int, session: Session = Depends(get_session)):
    analysis = session.exec(select(Analysis).where(Analysis.id == analysis_id)).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No existe")

    data = parse_all(analysis.text)

    _delete_previous_data(session, analysis_id)

    for sobre in ["A", "B", "C"]:
        for item in data.get("sobres", {}).get(sobre, []):
            session.add(
                Requirement(
                    analysis_id=analysis_id,
                    sobre=sobre,
                    descripcion=item.get("text", ""),
                    obligatorio=item.get("obligatorio", True),
                    estado=item.get("estado", "pending"),
                    source_start=item.get("start"),
                    source_end=item.get("end"),
                )
            )

    for criterion in data.get("criterios", []):
        session.add(
            Criterion(
                analysis_id=analysis_id,
                tipo=criterion["tipo"],
                descripcion=criterion["descripcion"],
                ponderacion=criterion.get("ponderacion"),
                juicio_valor=criterion.get("juicio_valor", False),
                source_start=criterion.get("start"),
                source_end=criterion.get("end"),
            )
        )

    if data.get("resumen"):
        resumen = data["resumen"]
        analysis.procedimiento = resumen.get("procedimiento")
        analysis.lotes = resumen.get("lotes")
    else:
        analysis.procedimiento = None
        analysis.lotes = None

    if data.get("plazos"):
        analysis.deadline_iso = data["plazos"].get("presentacion")
    else:
        analysis.deadline_iso = None

    session.add(analysis)
    session.commit()

    return {"status": "ok"}


@router.get("/analysis/{analysis_id}")
def get_analysis(analysis_id: int, session: Session = Depends(get_session)):
    analysis = session.exec(select(Analysis).where(Analysis.id == analysis_id)).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="No existe")

    requirements = session.exec(
        select(Requirement).where(Requirement.analysis_id == analysis_id)
    ).all()
    criteria = session.exec(
        select(Criterion).where(Criterion.analysis_id == analysis_id)
    ).all()

    sobres = {"A": [], "B": [], "C": []}
    for req in requirements:
        sobres[req.sobre].append(
            {
                "id": req.id,
                "descripcion": req.descripcion,
                "obligatorio": req.obligatorio,
                "estado": req.estado,
                "start": req.source_start,
                "end": req.source_end,
            }
        )

    return {
        "plazos": {"presentacion": analysis.deadline_iso}
        if analysis.deadline_iso
        else {},
        "sobres": sobres,
        "criterios": [
            {
                "id": criterion.id,
                "tipo": criterion.tipo,
                "descripcion": criterion.descripcion,
                "ponderacion": criterion.ponderacion,
                "juicio_valor": criterion.juicio_valor,
                "start": criterion.source_start,
                "end": criterion.source_end,
            }
            for criterion in criteria
        ],
        "resumen": {
            "procedimiento": analysis.procedimiento,
            "lotes": analysis.lotes,
        },
    }


@router.patch("/requirement/{req_id}")
def update_requirement(
    req_id: int,
    payload: dict = Body(...),
    session: Session = Depends(get_session),
):
    requirement = session.get(Requirement, req_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="No existe")

    if "estado" in payload:
        if payload["estado"] not in ("pending", "ok"):
            raise HTTPException(status_code=400, detail="Estado inválido")
        requirement.estado = payload["estado"]

    session.add(requirement)
    session.commit()
    session.refresh(requirement)
    return {"id": requirement.id, "estado": requirement.estado}


@router.get("/analysis/{analysis_id}/export")
def export_analysis(analysis_id: int, session: Session = Depends(get_session)):
    return get_analysis(analysis_id, session)


@router.get("/health")
def health():
    return {"status": "ok"}
