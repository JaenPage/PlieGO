from pydantic import BaseModel
from typing import List, Literal, Optional


class CriterionOut(BaseModel):
    tipo: Literal["tecnico", "economico"]
    descripcion: str
    ponderacion: Optional[float] = None
    juicio_valor: bool


class AnalysisOut(BaseModel):
    plazos: dict
    sobres: dict  # {"A":[...], "B":[...], "C":[...]}
    criterios: List[CriterionOut]
    resumen: dict
