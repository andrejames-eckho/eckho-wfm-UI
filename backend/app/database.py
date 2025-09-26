from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "eckho_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "eckho_password")
DB_NAME = os.getenv("POSTGRES_DB", "eckho_wfm")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Construct the database URL
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # Recommended settings for production
    pool_pre_ping=True,  # Verify connection before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

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