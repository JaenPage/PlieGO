from sqlmodel import SQLModel, Field
from typing import Optional


class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    text: str
    resumen: Optional[str] = None
    procedimiento: Optional[str] = None
    lotes: Optional[int] = None
    deadline_iso: Optional[str] = None
    text_index: Optional[str] = None  # mapa de offsets compactado (opcional)
