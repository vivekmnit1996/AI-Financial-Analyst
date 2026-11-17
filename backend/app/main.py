import os
import logging
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.routes import (
    companies_router,
    financials_router,
    documents_router,
    esg_router,
    collectors_router,
    chat_router,
    reports_router,
    settings_router,
)
from backend.app.rag.vector_store import VectorStoreManager
from backend.app.collectors.company_catalog import DEFAULT_COMPANY_CATALOG
from backend.app.models.schema_models import Company

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Create database schema
    logger.info("Initializing relational database tables...")
    Base.metadata.create_all(bind=engine)

    # 2. Initialize Qdrant collection
    logger.info("Ensuring Qdrant vector database collection...")
    try:
        VectorStoreManager.ensure_collection()
        logger.info("Qdrant collection ready.")
    except Exception as e:
        logger.warning(f"Could not connect to Qdrant during startup: {e}")

    # 3. Seed initial companies if empty
    db = SessionLocal()
    try:
        comp_count = db.query(Company).count()
        if comp_count == 0:
            logger.info("Seeding default benchmark companies from catalog...")
            for c in DEFAULT_COMPANY_CATALOG[:4]:  # AAPL, MSFT, INFY, TCS
                comp_obj = Company(
                    ticker=c["ticker"],
                    name=c["name"],
                    sector=c["sector"],
                    industry=c["industry"],
                    description=c["description"],
                    currency=c["currency"],
                    units=c["units"],
                    exchange=c["exchange"],
                    cik=c.get("cik"),
                    isin=c.get("isin"),
                    nse_symbol=c.get("nse_symbol"),
                    bse_code=c.get("bse_code"),
                    ir_url=c.get("ir_url")
                )
                db.add(comp_obj)
            db.commit()
            logger.info("Seeded initial companies successfully.")
    except Exception as e:
        logger.error(f"Error seeding companies: {e}")
        db.rollback()
    finally:
        db.close()

    yield

    logger.info("Application shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="End-to-End AI Financial Analyst, Automated Ingestion, ESG Scorer & Report Generator",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
api_prefix = settings.API_V1_PREFIX
app.include_router(companies_router, prefix=api_prefix)
app.include_router(financials_router, prefix=api_prefix)
app.include_router(documents_router, prefix=api_prefix)
app.include_router(esg_router, prefix=api_prefix)
app.include_router(collectors_router, prefix=api_prefix)
app.include_router(chat_router, prefix=api_prefix)
app.include_router(reports_router, prefix=api_prefix)
app.include_router(settings_router, prefix=api_prefix)

@app.get("/api")
def api_root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_PREFIX,
        "status": "RUNNING"
    }

# Static files and Frontend SPA fallback
dist_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/assets", StaticFiles(directory=dist_dir / "assets"), name="assets")

    @app.get("/")
    def serve_frontend_root():
        index_file = dist_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return api_root()

    @app.get("/{full_path:path}")
    def serve_frontend_spa(full_path: str):
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return None
        index_file = dist_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return {"status": "Frontend build not found"}
else:
    @app.get("/")
    def serve_fallback_root():
        return api_root()
