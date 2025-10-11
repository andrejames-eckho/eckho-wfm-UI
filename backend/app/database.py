from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from typing import AsyncGenerator

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "eckho_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "eckho_password")
DB_NAME = os.getenv("POSTGRES_DB", "eckho_wfm")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Construct the database URLs
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create SQLAlchemy engines
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create async engine for testing
async_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    future=True
)

# Create session factories
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()

# Dependency for synchronous database sessions
def get_db():
    """
    Dependency function that yields database sessions.
    Ensures the database connection is properly closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for async database sessions
async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Async dependency that yields database sessions.
    Ensures the database connection is properly closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Alias for backward compatibility
async_session = AsyncSessionLocal