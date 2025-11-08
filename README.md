# PlieGO

Este repositorio contiene el MVP del proyecto PlieGO, compuesto por un backend en FastAPI y un frontend en React (Vite + TypeScript + CSS Modules). El objetivo es permitir la subida de pliegos en PDF/DOCX, extraer el contenido relevante y presentar un resumen con checklist por sobres.

## 🚀 Puesta en marcha con Docker

```bash
cd pliego
docker-compose up --build
```

- API disponible en `http://localhost:8000`.
- Frontend disponible en `http://localhost:5173`.

## 🧩 Estructura

```
pliego/
  backend/
    app/
      api/v1/
      core/
      models/
      schemas/
      services/
    requirements.txt
    Dockerfile
  frontend/
    src/
      api/
      components/
      pages/
      styles/
    package.json
    Dockerfile
  docker-compose.yml
```

Consulta los archivos dentro de cada directorio para ver la implementación completa del MVP.
