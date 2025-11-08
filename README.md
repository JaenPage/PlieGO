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

## 🧪 Uso

1. Levanta el stack:

   ```bash
   docker-compose up --build
   ```

2. Abre `http://localhost:5173` y sube un PDF o DOCX.
3. El flujo de la app: `/upload` → `/analysis/{id}/persist` → vista de resumen y checklist.
4. Marca cada requisito como **Pendiente** u **OK** desde la UI.
5. Usa el botón **Exportar JSON** para descargar el análisis (la exportación a PDF llegará en el siguiente sprint).
