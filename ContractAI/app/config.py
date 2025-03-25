"""
Configuration module for ContractAI.

This module provides configuration settings loaded from environment variables.
"""

import os
from typing import Dict, List, Optional, Union
from pydantic import BaseSettings, Field, validator

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    APP_NAME: str = Field(default="DocMatrix ContractAI")
    API_PREFIX: str = Field(default="/api")
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="development")
    
    # Database settings
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="contractai")
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="")
    DATABASE_URL: Optional[str] = None
    
    # Redis settings
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Storage settings
    STORAGE_TYPE: str = Field(default="local")  # local, minio, azure, s3
    STORAGE_ENDPOINT: Optional[str] = None
    STORAGE_ACCESS_KEY: Optional[str] = None
    STORAGE_SECRET_KEY: Optional[str] = None
    STORAGE_BUCKET: str = Field(default="contractai")
    
    # JWT settings
    JWT_SECRET: str = Field(default="")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # LLM API keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    
    @validator("DATABASE_URL", pre=True)
    def assemble_db_url(cls, v, values):
        """Assemble database URL from components if not provided."""
        if v:
            return v
        
        user = values.get("DB_USER", "")
        password = values.get("DB_PASSWORD", "")
        host = values.get("DB_HOST", "localhost")
        port = values.get("DB_PORT", 5432)
        db = values.get("DB_NAME", "contractai")
        
        if user and password:
            return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        return f"postgresql://{host}:{port}/{db}"
    
    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, v, values):
        """Validate JWT secret in production environment."""
        if values.get("ENVIRONMENT") == "production" and not v:
            raise ValueError("JWT_SECRET must be set in production environment")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
