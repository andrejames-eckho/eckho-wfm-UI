import sys
import os
from datetime import datetime, date, time, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import Base
from app.models import User, RecordType, Department
from app.services.time_record_service import TimeRecordService
from app.services.user_service import UserService

# Test database setup
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    # Create all tables
    Base.metadata.create_all(bind=engine)

def teardown_module():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

def test_get_daily_summary():
    # Setup test data
    db = TestingSessionLocal()
    
    # Create a test user
    from app.schemas import UserCreate
    
    user_service = UserService()
    user_data = UserCreate(
        username="test_user",
        first_name="Test",
        last_name="User",
        department=Department.WAREHOUSE
    )
    test_user = user_service.create(db, user_data)
    
    # Create time record service
    time_service = TimeRecordService()
    
    # Today's date
    today = date.today()
    
    # Add some time records for today
    records = [
        {"time": time(9, 0), "record_type": RecordType.TIME_IN},
        {"time": time(12, 0), "record_type": RecordType.BREAK_IN},
        {"time": time(12, 30), "record_type": RecordType.BREAK_OUT},
        {"time": time(17, 0), "record_type": RecordType.TIME_OUT}
    ]
    
    for record in records:
        time_service.create(
            db=db,
            obj_in={
                "user_id": test_user.id,
                "date": today,
                "time": record["time"],
                "record_type": record["record_type"]
            }
        )
    
    # Add a record from a different day to ensure it's filtered out
    yesterday = today - timedelta(days=1)
    time_service.create(
        db=db,
        obj_in={
            "user_id": test_user.id,
            "date": yesterday,
            "time": time(9, 0),
            "record_type": RecordType.TIME_IN
        }
    )
    
    # Test 1: Get today's summary
    result = time_service.get_daily_summary(db, test_user.id, today)
    
    # Print the daily summary output
    print("\n=== DAILY SUMMARY OUTPUT ===")
    print(f"Date: {result['date']}")
    print(f"Total Records: {result['total_records']}")
    print("Records:")
    for record in result['records']:
        print(f"  - {record['time']} - {record['record_type']} (ID: {record['id']})")
    print("==========================\n")
    
    # Verify the results
    assert result["date"] == today.isoformat()
    assert result["total_records"] == 4  # Should have 4 records for today
    
    # Verify record types and order (should be in reverse chronological order)
    record_types = [r["record_type"] for r in result["records"]]
    assert record_types == [
        RecordType.TIME_OUT,
        RecordType.BREAK_OUT,
        RecordType.BREAK_IN,
        RecordType.TIME_IN
    ]
    
    # Verify times are in reverse chronological order
    times = [r["time"] for r in result["records"]]
    assert times == ["17:00:00", "12:30:00", "12:00:00", "09:00:00"]
    
    # Test 2: Get empty summary for a day with no records
    future_date = today + timedelta(days=30)
    empty_result = time_service.get_daily_summary(db, test_user.id, future_date)
    assert empty_result["date"] == future_date.isoformat()
    assert empty_result["total_records"] == 0
    assert empty_result["records"] == []
    
    # Cleanup
    db.close()

if __name__ == "__main__":
    setup_module()
    try:
        test_get_daily_summary()
        print("✅ All tests passed!")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    finally:
        teardown_module()
