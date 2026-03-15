from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "book_library"
    db_port: int = 5432
    db_host: str = "localhost"
    
    # API
    api_title: str = "Book Library API"
    api_version: str = "1.0.0"
    api_description: str = "A FastAPI application for managing a book library"
    api_port: int = 8000
    
    # Borrowing Configuration
    borrowing_duration_days: int = 14  # Number of days a book can be borrowed
    fine_per_day: float = 10.0  # Fine amount per day (late fee)
    max_fine: float = 500.0  # Maximum fine that can be charged
    
    # Environment
    environment: str = "development"
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # Logging
    log_level: str = "INFO"
    
    # Optional: PostgreSQL connection pool settings
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 3600  # 1 hour
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "env_file_encoding": "utf-8"
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
