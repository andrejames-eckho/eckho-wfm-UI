import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models, crud, schemas
from app.models import Department

def test_db_integration():
    db = SessionLocal()
    
    try:
        print("Starting database integration test...")
        
        # Clean up any existing test data
        test_username = "test_user_001"
        existing_user = crud.get_user_by_username(db, username=test_username)
        if existing_user:
            print(f"Cleaning up existing test user: {test_username}")
            # Delete any time records first (due to foreign key constraint)
            db.query(models.TimeRecord).filter(models.TimeRecord.user_id == existing_user.id).delete()
            # Then delete the user
            db.delete(existing_user)
            db.commit()
        
        # Create a test user
        test_user = schemas.UserCreate(
            username=test_username,
            first_name="Test",
            last_name="User",
            department=Department.WAREHOUSE
        )
        
        print("Creating test user...")
        db_user = crud.create_user(db, test_user)
        print(f"Created user: {db_user.username} (ID: {db_user.id})")
        
        # Create test time records (for today)
        now = datetime.now()
        test_date = now.date()
        
        # Time In (9:00 AM)
        time_in = now.replace(hour=9, minute=0, second=0, microsecond=0)
        time_in_record = schemas.TimeRecordCreate(
            user_id=db_user.id,
            date=test_date,
            time=time_in,
            record_type=models.RecordType.TIME_IN
        )
        
        # Break In (12:00 PM)
        break_in = now.replace(hour=12, minute=0, second=0, microsecond=0)
        break_in_record = schemas.TimeRecordCreate(
            user_id=db_user.id,
            date=test_date,
            time=break_in,
            record_type=models.RecordType.BREAK_IN
        )
        
        # Break Out (12:30 PM)
        break_out = now.replace(hour=12, minute=30, second=0, microsecond=0)
        break_out_record = schemas.TimeRecordCreate(
            user_id=db_user.id,
            date=test_date,
            time=break_out,
            record_type=models.RecordType.BREAK_OUT
        )
        
        # Time Out (5:00 PM)
        time_out = now.replace(hour=17, minute=0, second=0, microsecond=0)
        time_out_record = schemas.TimeRecordCreate(
            user_id=db_user.id,
            date=test_date,
            time=time_out,
            record_type=models.RecordType.TIME_OUT
        )
        
        # Add all records to database
        print("Creating time records...")
        records = [
            time_in_record,
            break_in_record,
            break_out_record,
            time_out_record
        ]
        
        created_records = []
        for record in records:
            created = crud.create_time_record(db, record)
            created_records.append(created)
            print(f"Created {record.record_type} record at {record.time.time()}")
        
        # Verify the records were created
        print("\nVerifying records...")
        user_records = crud.get_user_time_records(db, user_id=db_user.id)
        
        if len(user_records) == 4:
            print("✅ Success: All 4 time records were created successfully!")
            for record in user_records:
                print(f"- {record.record_type}: {record.time.time()}")
        else:
            print(f"❌ Error: Expected 4 records, but found {len(user_records)}")
        
        return True
        
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")
        db.rollback()
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    # Create all tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    
    # Run the test
    success = test_db_integration()
    
    if success:
        print("\n✅ Database integration test completed successfully!")
    else:
        print("\n❌ Database integration test failed!")
        sys.exit(1)
