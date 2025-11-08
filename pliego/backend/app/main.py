from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.db import init_db
from app.api.v1.upload import router as upload_router
from app.api.v1.analysis import router as analysis_router

app = FastAPI(title="PlieGO API", version="0.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(upload_router, prefix="/api/v1")
app.include_router(analysis_router, prefix="/api/v1")

@app.on_event("startup")
def startup():
    init_db()
