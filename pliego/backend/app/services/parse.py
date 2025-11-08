import regex as re
from datetime import datetime
from typing import Dict, List, Optional

PATTERNS = {
    "sobres": r"(SOBRE\s+(A|B|C)[^\n]*)(?s)(.*?)(?=(SOBRE\s+[ABC]\b)|\Z)",
    "criterios": r"criterios?\s+de\s+adjudicación|criterios?\s+técnicos|criterios?\s+económicos",
    "plazo": r"(plazo\s+de\s+presentación.*?)(\d{1,2}[/\-\.]\d{1,2}[/\-\.]\d{2,4}.*?(?:\d{1,2}:\d{2}))",
}


def parse_deadline(text: str) -> Optional[str]:
    match = re.search(PATTERNS["plazo"], text, re.I | re.S)
    if not match:
        return None
    date_match = re.search(r"(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4}).*?(\d{1,2}):(\d{2})", match.group(0))
    if not date_match:
        return None
    day, month, year, hour, minute = map(int, date_match.groups())
    year = 2000 + year if year < 100 else year
    deadline = datetime(year, month, day, hour, minute)
    return deadline.isoformat()


def parse_sobres(text: str) -> Dict[str, List[str]]:
    sobres = {"A": [], "B": [], "C": []}
    for match in re.finditer(PATTERNS["sobres"], text, re.I):
        label = match.group(2).upper()
        body = match.group(3)
        items = re.findall(r"(?:^|\n)[•\-\*]?\s*([A-ZÁÉÍÓÚÑ][^\n]{5,120})", body)
        sobres[label].extend([item.strip(" .;") for item in items])
    return sobres


def parse_criterios(text: str):
    bloques = re.split(PATTERNS["criterios"], text, flags=re.I)
    resultados = []
    for bloque in bloques:
        for line in bloque.split("\n"):
            match = re.search(r"(?P<desc>.+?)\s+(?:hasta\s+)?(?P<p>\d{1,3})(?:\s*puntos?|%)", line, re.I)
            if match:
                desc = match.group("desc").strip(" :;-")
                puntos = float(match.group("p"))
                if re.search(r"técnic", line, re.I):
                    tipo = "tecnico"
                elif re.search(r"econ", line, re.I):
                    tipo = "economico"
                else:
                    tipo = "tecnico"
                juicio = bool(re.search(r"juicio\s+de\s+valor", line, re.I))
                resultados.append({
                    "tipo": tipo,
                    "descripcion": desc,
                    "ponderacion": puntos,
                    "juicio_valor": juicio,
                })
    return resultados


def parse_summary(text: str):
    procedimiento = re.search(r"(procedimiento|tipo):?\s*(abierto.*?|negociado.*?|simplificado.*)", text, re.I)
    lotes = re.search(r"\blotes?:?\s*(\d+)", text, re.I)
    return {
        "procedimiento": procedimiento.group(2).strip() if procedimiento else None,
        "lotes": int(lotes.group(1)) if lotes else None,
    }


def parse_all(text: str):
    sobres = parse_sobres(text)
    criterios = parse_criterios(text)
    deadline = parse_deadline(text)
    resumen = parse_summary(text)
    return {
        "plazos": {"presentacion": deadline} if deadline else {},
        "sobres": sobres,
        "criterios": criterios,
        "resumen": resumen,
    }
