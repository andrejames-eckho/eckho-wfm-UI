import sys
import os
from datetime import datetime, date, time
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base, get_db
from app.services import user_service, time_record_service
from app.models import Department, RecordType
from app.schemas import UserCreate, TimeRecordCreate

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Use in-memory database for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    return db

# Set up the database once for all tests
db = setup_db()

def cleanup_db():
    # Clean up after all tests
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_user_service():
    print("\n=== Testing User Service ===")
    # Use the global db session
    
    # Test create user
    user_data = UserCreate(
        username="testuser",
        first_name="Test",
        last_name="User",
        department=Department.FIELD
    )
    
    # Create user
    user = user_service.create(db, obj_in=user_data)
    print(f"✅ Created user: {user.username} (ID: {user.id})")
    
    # Test get user
    fetched_user = user_service.get(db, user.id)
    assert fetched_user is not None
    assert fetched_user.username == "testuser"
    print(f"✅ Fetched user: {fetched_user.username}")
    
    # Test get by username
    user_by_username = user_service.get_by_username(db, username="testuser")
    assert user_by_username is not None
    assert user_by_username.id == user.id
    print(f"✅ Found user by username: {user_by_username.username}")
    
    # Test get all users
    users = user_service.get_multi(db)
    assert len(users) == 1
    print(f"✅ Found {len(users)} users")
    
    # Test get with time records (initially should have none)
    user_with_records = user_service.get_with_time_records(db, user_id=user.id)
    assert user_with_records is not None
    assert len(user_with_records.time_records) == 0
    print("✅ User has no time records initially")
    
    return user

def test_time_record_service(user_id: int):
    print("\n=== Testing Time Record Service ===")
    # Use the global db session
    
    # Create a time record
    time_record_data = TimeRecordCreate(
        user_id=user_id,
        date=date.today(),
        time=datetime.now().time(),
        record_type=RecordType.TIME_IN
    )
    
    # Test create time record
    time_record = time_record_service.create(db, obj_in=time_record_data)
    print(f"✅ Created time record: {time_record.id}")
    
    # Test get time record
    fetched_record = time_record_service.get(db, time_record.id)
    assert fetched_record is not None
    assert fetched_record.user_id == user_id
    print(f"✅ Fetched time record: {fetched_record.id}")
    
    # Test get user time records
    user_records = time_record_service.get_user_time_records(db, user_id=user_id)
    assert len(user_records) == 1
    print(f"✅ Found {len(user_records)} time records for user")
    
    # Test get records for today
    today = date.today()
    today_records = time_record_service.get_user_records_for_date(db, user_id=user_id, target_date=today)
    assert len(today_records) == 1
    print(f"✅ Found {len(today_records)} time records for today")
    
    # Test get last record type
    last_type = time_record_service.get_last_record_type(db, user_id=user_id, target_date=today)
    assert last_type == RecordType.TIME_IN
    print(f"✅ Last record type: {last_type}")
    
    # Clean up
    time_record_service.delete(db, id=time_record.id)
    print("✅ Deleted time record")

if __name__ == "__main__":
    try:
        print("🚀 Starting service layer tests...")
        user = test_user_service()
        test_time_record_service(user.id)
        print("\n🎉 All tests passed successfully!")
    finally:
        # Clean up the database after all tests
        cleanup_db()
