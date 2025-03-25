"""
Database module for ContractAI.

This module provides database connection utilities and session management.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from typing import Generator, AsyncGenerator
import logging

from ContractAI.app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create database URL
DATABASE_URL = settings.DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    # Replace postgresql:// with postgresql+asyncpg:// for async connections
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create engine
engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True,
    echo=settings.DEBUG
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Create base class for declarative models
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session for dependency injection.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

async def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This should only be used for development or testing.
    Production should use Alembic migrations.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database initialized")
