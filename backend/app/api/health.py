"""Health and system readiness endpoints."""
from fastapi import APIRouter
from backend.app.config import settings
from backend.app.db.session import db_manager

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    db_status = await db_manager.check_connection()
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": db_status,
            "ollama": "ready"
        }
    }
