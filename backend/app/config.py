import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Financial Analyst & Report Generator"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/financial_analyst.db")
    
    # Qdrant Vector DB
    QDRANT_MODE: str = os.getenv("QDRANT_MODE", "local")  # "local" or "server"
    QDRANT_PATH: str = os.getenv("QDRANT_PATH", str(BASE_DIR / "data" / "qdrant_storage"))
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "localhost")
    QDRANT_PORT: int = int(os.getenv("QDRANT_PORT", "6333"))
    QDRANT_COLLECTION: str = os.getenv("QDRANT_COLLECTION", "financial_documents")
    
    # Embedding & Reranker
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    ENABLE_RERANKER: bool = os.getenv("ENABLE_RERANKER", "true").lower() == "true"
    DENSE_TOP_K: int = int(os.getenv("DENSE_TOP_K", "10"))
    BM25_TOP_K: int = int(os.getenv("BM25_TOP_K", "10"))
    RRF_K: int = int(os.getenv("RRF_K", "60"))
    FINAL_TOP_K: int = int(os.getenv("FINAL_TOP_K", "5"))
    
    # LLM Provider Configuration
    # Supported: "deterministic" (fallback/local), "gemini", "openai", "groq", "ollama"
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "deterministic")
    GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY", None)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY", None)
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY", None)
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "gemini-1.5-flash")
    
    # Storage Paths
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    REPORTS_DIR: Path = BASE_DIR / "data" / "reports"
    MAX_UPLOAD_SIZE_MB: int = 50
    ALLOWED_EXTENSIONS: list[str] = [".pdf", ".csv", ".xlsx", ".txt"]
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
Path(settings.QDRANT_PATH).mkdir(parents=True, exist_ok=True)
