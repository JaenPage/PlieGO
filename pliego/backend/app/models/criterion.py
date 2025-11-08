from sqlmodel import SQLModel, Field
from typing import Optional, Literal

class Criterion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int
    tipo: Literal["tecnico","economico"]
    descripcion: str
    ponderacion: Optional[float] = None
    juicio_valor: bool = False
