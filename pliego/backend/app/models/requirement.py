from sqlmodel import SQLModel, Field
from typing import Optional, Literal

class Requirement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int
    sobre: Literal["A","B","C"]
    descripcion: str
    obligatorio: bool = True
    estado: Literal["pending","ok"] = "pending"
    source_span: Optional[str] = None  # offsets del texto
