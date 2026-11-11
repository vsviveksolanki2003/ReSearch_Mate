"""Aggregated API router mounting all sub-routes."""
from fastapi import APIRouter
from backend.app.api.health import router as health_router
from backend.app.api.papers import router as papers_router
from backend.app.api.chat import router as chat_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router)
api_router.include_router(papers_router)
api_router.include_router(chat_router)
