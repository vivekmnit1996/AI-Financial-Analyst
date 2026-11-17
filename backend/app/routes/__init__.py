from backend.app.routes.companies import router as companies_router
from backend.app.routes.financials import router as financials_router
from backend.app.routes.documents import router as documents_router
from backend.app.routes.esg import router as esg_router
from backend.app.routes.collectors import router as collectors_router
from backend.app.routes.chat import router as chat_router
from backend.app.routes.reports import router as reports_router
from backend.app.routes.settings import router as settings_router

__all__ = [
    "companies_router",
    "financials_router",
    "documents_router",
    "esg_router",
    "collectors_router",
    "chat_router",
    "reports_router",
    "settings_router",
]
