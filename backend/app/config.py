"""Application configuration using Pydantic Settings."""
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    APP_NAME: str = "ReSearch_Mate"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Network and Host
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # Storage
    STORAGE_DIR: Path = BASE_DIR / "storage"
    UPLOAD_DIR: Path = BASE_DIR / "storage" / "uploads"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/research_mate"
    DB_POOL_MIN: int = 1
    DB_POOL_MAX: int = 10
    
    # Vector Search & Local AI
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIMENSION: int = 384
    HNSW_M: int = 16
    HNSW_EF_CONSTRUCTION: int = 64
    
    # Ollama Local LLM
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b-instruct"
    
    # Retrieval Hyperparameters
    RETRIEVAL_TOP_K: int = 5
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 100

    model_config = {"env_file": ".env", "extra": "allow"}

settings = Settings()
