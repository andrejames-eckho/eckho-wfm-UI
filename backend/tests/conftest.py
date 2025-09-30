import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import User, TimeRecord, RecordType, Department

# Use the main database for testing
TEST_DB_URL = "postgresql://eckho_user:eckho_password@localhost:5432/eckho_wfm"

@pytest.fixture(scope="session")
def engine():
    """Create a test database engine"""
    engine = create_engine(TEST_DB_URL)
    
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # No cleanup needed - we're using the main database

@pytest.fixture
def db_session(engine):
    """Create a new database session for a test"""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def test_user(db_session):
    """Create a test user"""
    user = User(
        username="test_user",
        first_name="Test",
        last_name="User",
        department=Department.WAREHOUSE
    )
    db_session.add(user)
    db_session.commit()
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
