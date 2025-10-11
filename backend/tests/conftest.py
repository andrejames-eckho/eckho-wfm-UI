import os
import pytest
import asyncio
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_async_db
from app.models import User, TimeRecord, RecordType, Department

# Use SQLite in-memory database for testing
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for testing
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def engine():
    """Create a test database engine"""
    engine = create_async_engine(
        TEST_DB_URL,
        echo=True,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest.fixture
def override_get_db(engine):
    """Override the get_db dependency for testing"""
    async def _get_db():
        async with async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )() as session:
            try:
                yield session
            finally:
                await session.close()
    return _get_db

@pytest.fixture
def app(override_get_db):
    """Create a test FastAPI application"""
    from app.main import app
    from app.database import get_async_db
    
    app.dependency_overrides[get_async_db] = override_get_db
    return app

@pytest.fixture
async def async_client(app):
    """Create a test client that can be used to make requests to the application."""
    from fastapi.testclient import TestClient
    
    async with TestClient(app) as client:
        yield client

@pytest.fixture
async def db_session(engine):
    """Create a new database session for a test"""
    async with async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@pytest.fixture
async def test_user(db_session):
    """Create a test user"""
    user = User(
        username="test_user",
        first_name="Test",
        last_name="User",
        department=Department.WAREHOUSE
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def test_records(db_session, test_user):
    """Create test time records"""
    from datetime import date, time, timedelta
    
    # Create records for the past week
    records = []
    for day in range(7):
        current_date = date.today() - timedelta(days=6-day)  # Last 7 days
        
        records.extend([
            TimeRecord(
                user_id=test_user.id,
                date=current_date,
                time=time(9, 0),
                record_type=RecordType.TIME_IN
            ),
            TimeRecord(
                user_id=test_user.id,
                date=current_date,
                time=time(12, 0),
                record_type=RecordType.BREAK_IN
            ),
            TimeRecord(
                user_id=test_user.id,
                date=current_date,
                time=time(13, 0),
                record_type=RecordType.BREAK_OUT
            ),
            TimeRecord(
                user_id=test_user.id,
                date=current_date,
                time=time(18, 0),
                record_type=RecordType.TIME_OUT
            )
        ])
    
    db_session.add_all(records)
    db_session.commit()
    return records
