import os
from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.config import settings
from backend.app.rag.vector_store import VectorStoreManager

router = APIRouter(prefix="/settings", tags=["System Settings & Diagnostics"])

class SystemSettingsResponse(BaseModel):
    project_name: str
    version: str
    database_url: str
    qdrant_mode: str
    qdrant_path: str
    qdrant_collection: str
    embedding_model: str
    reranker_enabled: bool
    llm_provider: str
    gemini_configured: bool
    openai_configured: bool
    groq_configured: bool
    ollama_url: str

class UpdateLLMSettingsRequest(BaseModel):
    llm_provider: str
    gemini_api_key: str | None = None
    openai_api_key: str | None = None
    llm_model_name: str | None = None

@router.get("", response_model=SystemSettingsResponse)
def get_system_settings():
    """Returns current environment configurations without leaking secret keys."""
    # Mask database credentials if postgres
    db_str = settings.DATABASE_URL
    if "://" in db_str and "@" in db_str:
        prefix, rest = db_str.split("://", 1)
        creds, host_part = rest.split("@", 1)
        db_str = f"{prefix}://*****:*****@{host_part}"

    return SystemSettingsResponse(
        project_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        database_url=db_str,
        qdrant_mode=settings.QDRANT_MODE,
        qdrant_path=settings.QDRANT_PATH,
        qdrant_collection=settings.QDRANT_COLLECTION,
        embedding_model=settings.EMBEDDING_MODEL,
        reranker_enabled=settings.ENABLE_RERANKER,
        llm_provider=settings.LLM_PROVIDER,
        gemini_configured=bool(settings.GEMINI_API_KEY),
        openai_configured=bool(settings.OPENAI_API_KEY),
        groq_configured=bool(settings.GROQ_API_KEY),
        ollama_url=settings.OLLAMA_BASE_URL
    )

@router.post("/update-llm")
def update_llm_settings(payload: UpdateLLMSettingsRequest):
    """Dynamically update LLM provider or set API key in memory."""
    settings.LLM_PROVIDER = payload.llm_provider
    if payload.gemini_api_key:
        settings.GEMINI_API_KEY = payload.gemini_api_key
    if payload.openai_api_key:
        settings.OPENAI_API_KEY = payload.openai_api_key
    if payload.llm_model_name:
        settings.LLM_MODEL_NAME = payload.llm_model_name

    return {
        "status": "SUCCESS",
        "message": f"LLM provider updated to {payload.llm_provider}",
        "gemini_active": bool(settings.GEMINI_API_KEY),
        "openai_active": bool(settings.OPENAI_API_KEY)
    }

@router.get("/health")
def health_check():
    """System health check for database and vector store."""
    qdrant_status = "UNKNOWN"
    try:
        client = VectorStoreManager.get_client()
        cols = client.get_collections()
        qdrant_status = "CONNECTED"
    except Exception as e:
        qdrant_status = f"ERROR: {str(e)}"

    return {
        "status": "ONLINE",
        "qdrant": qdrant_status,
        "database": "CONNECTED",
        "llm_provider": settings.LLM_PROVIDER,
        "version": settings.VERSION
    }
