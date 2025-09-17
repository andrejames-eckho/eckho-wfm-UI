from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.models.db_models import Base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database URL from environment variable - using asyncpg driver
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://eckho_user:eckho_password@localhost:5432/eckho_wfm")

# For synchronous operations, use psycopg2 URL format but we'll handle it differently
SYNC_DATABASE_URL = "postgresql://eckho_user:eckho_password@127.0.0.1:5432/eckho_wfm"

# Create SQLAlchemy engine for sync operations
engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is imported from db_models, no need to recreate

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
