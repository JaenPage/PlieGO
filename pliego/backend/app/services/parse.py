import logging
from datetime import datetime
from typing import Dict, List, Optional

import regex as re

PATTERNS = {
    "sobres": r"(SOBRE\s+(A|B|C)[^\n]*)(?s)(.*?)(?=(SOBRE\s+[ABC]\b)|\Z)",
    "criterios": r"(?P<full>(?P<desc>[^\n]{5,}?)(?:hasta\s+)?(?P<p>\d{1,3})(?:\s*puntos?|%))",
    "plazo": r"(plazo\s+de\s+presentación.*?)(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}.*?(?:\d{1,2}:\d{2}))",
}

logger = logging.getLogger(__name__)


def parse_deadline(text: str) -> Dict[str, object]:
    match = re.search(PATTERNS["plazo"], text, re.I | re.S)
    if not match:
        return {}
    date_match = re.search(r"(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4}).*?(\d{1,2}):(\d{2})", match.group(0))
    if not date_match:
        return {}
    day, month, year, hour, minute = map(int, date_match.groups())
    year = 2000 + year if year < 100 else year
    deadline = datetime(year, month, day, hour, minute)
    return {
        "presentacion": deadline.isoformat(),
        "start": match.start(0),
        "end": match.end(0),
    }


def parse_sobres(text: str) -> Dict[str, List[Dict[str, object]]]:
    sobres = {"A": [], "B": [], "C": []}
    section_pattern = re.compile(PATTERNS["sobres"], re.I)
    item_pattern = re.compile(r"(?:^|\n)[•\-\*]?\s*(?P<item>[A-ZÁÉÍÓÚÑ][^\n]{5,120})")

    for match in section_pattern.finditer(text):
        label = match.group(2).upper()
        body = match.group(3)
        body_offset = match.start(3)
        for item_match in item_pattern.finditer(body):
            raw_full = item_match.group("item")
            trimmed_text = raw_full.strip(" .;")
            leading_trim = len(raw_full) - len(raw_full.lstrip(" .;"))
            trailing_trim = len(raw_full) - len(raw_full.rstrip(" .;"))
            start = body_offset + item_match.start("item") + leading_trim
            end = body_offset + item_match.end("item") - trailing_trim
            sobres[label].append(
                {
                    "text": trimmed_text,
                    "obligatorio": True,
                    "start": start,
                    "end": end,
                }
            )
    return sobres


def parse_criterios(text: str) -> List[Dict[str, object]]:
    resultados: List[Dict[str, object]] = []
    for match in re.finditer(PATTERNS["criterios"], text, re.I):
        line = match.group("full")
        desc = match.group("desc").strip(" :;-.")
        puntos = float(match.group("p"))
        if re.search(r"t[ée]cnic", line, re.I):
            tipo = "tecnico"
        elif re.search(r"econ", line, re.I):
            tipo = "economico"
        else:
            tipo = "tecnico"
        juicio = bool(re.search(r"juicio\s+de\s+valor", line, re.I))
        resultados.append(
            {
                "tipo": tipo,
                "descripcion": desc,
                "ponderacion": puntos,
                "juicio_valor": juicio,
                "start": match.start("full"),
                "end": match.end("full"),
            }
        )
    return resultados


def parse_summary(text: str):
    procedimiento = re.search(
        r"(procedimiento|tipo):?\s*(abierto.*?|negociado.*?|simplificado.*)", text, re.I
    )
    lotes = re.search(r"\blotes?:?\s*(\d+)", text, re.I)
    return {
        "procedimiento": procedimiento.group(2).strip() if procedimiento else None,
        "lotes": int(lotes.group(1)) if lotes else None,
        "procedimiento_start": procedimiento.start(2) if procedimiento else None,
        "procedimiento_end": procedimiento.end(2) if procedimiento else None,
        "lotes_start": lotes.start(1) if lotes else None,
        "lotes_end": lotes.end(1) if lotes else None,
    }


def parse_all(text: str):
    sobres = parse_sobres(text)
    criterios = parse_criterios(text)
    deadline = parse_deadline(text)
    resumen = parse_summary(text)
    return {
        "plazos": deadline if deadline else {},
        "sobres": sobres,
        "criterios": criterios,
        "resumen": resumen,
    }
