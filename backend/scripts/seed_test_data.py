import sys
import os
from datetime import datetime, time, timedelta, date
import random
from typing import List, Dict, Any

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app import models, schemas
from app.services.user_service import UserService
from app.services.time_record_service import TimeRecordService

# Initialize services
user_service = UserService()
time_record_service = TimeRecordService()

def create_test_user(db, username: str, first_name: str, last_name: str, department: str) -> models.User:
    """Create a test user if they don't already exist"""
    # Check if user exists
    user = db.query(models.User).filter(
        models.User.username == username
    ).first()
    
    if user:
        print(f"User {username} already exists with ID {user.id}")
        return user
    
    # Create new user
    user_data = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "department": department.upper()
    }
    
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Created user {username} with ID {user.id}")
    return user

def generate_workday_records(user_id: int, work_date: date) -> List[Dict[str, Any]]:
    """Generate time records for a single workday"""
    # Generate random work hours between 8-10 hours with 30-60 minute lunch break
    start_hour = random.randint(8, 9)  # Start between 8-9 AM
    start_minute = random.choice([0, 15, 30, 45])
    
    # Create time in
    time_in = time(hour=start_hour, minute=start_minute)
    
    # Create break in (4-5 hours after start)
    break_in_hour = start_hour + 4
    break_in_minute = random.choice([0, 15, 30, 45])
    break_in = time(hour=break_in_hour, minute=break_in_minute)
    
    # Create break out (30-60 minutes after break in)
    break_duration = random.randint(30, 60)
    break_out_dt = datetime.combine(work_date, break_in) + timedelta(minutes=break_duration)
    break_out = break_out_dt.time()
    
    # Create time out (4-5 hours after break out)
    time_out_hour = break_out.hour + 4
    time_out_minute = break_out.minute
    if time_out_hour >= 24:
        time_out_hour = 23
        time_out_minute = 45
    time_out = time(hour=time_out_hour, minute=time_out_minute)
    
    # Create records list
    records = [
        {"user_id": user_id, "date": work_date, "time": time_in, "record_type": "Time In"},
        {"user_id": user_id, "date": work_date, "time": break_in, "record_type": "Break In"},
        {"user_id": user_id, "date": work_date, "time": break_out, "record_type": "Break Out"},
        {"user_id": user_id, "date": work_date, "time": time_out, "record_type": "Time Out"},
    ]
    
    return records

def main():
    print("Starting test data generation...")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Create test users
        users = [
            {"username": "test_warehouse1", "first_name": "Warehouse", "last_name": "Worker1", "department": "Warehouse"},
            {"username": "test_field1", "first_name": "Field", "last_name": "Worker1", "department": "Field"}
        ]
        
        created_users = []
        for user_data in users:
            user = create_test_user(
                db,
                username=user_data["username"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                department=user_data["department"]
            )
            created_users.append(user)
        
        # Generate time records for the last 4 workdays (excluding weekends)
        today = date.today()
        workdays = []
        days_back = 1
        
        while len(workdays) < 4:
            target_date = today - timedelta(days=days_back)
            # Skip weekends (5=Saturday, 6=Sunday)
            if target_date.weekday() < 5:  # 0-4 = Monday-Friday
                workdays.append(target_date)
            days_back += 1
        
        # Sort workdays in chronological order
        workdays.sort()
        
        print("\nGenerating time records for the following workdays:")
        for day in workdays:
            print(f"- {day.strftime('%A, %Y-%m-%d')}")
        
        # Create time records for each user
        for user in created_users:
            print(f"\nGenerating time records for user: {user.username} (ID: {user.id})")
            
            for workday in workdays:
                print(f"\nCreating records for {workday.strftime('%A, %Y-%m-%d')}")
                records = generate_workday_records(user.id, workday)
                
                for record in records:
                    print(f"  - {record['record_type']} at {record['time'].strftime('%H:%M')}")
                    
                    # Create time record
                    time_record = models.TimeRecord(
                        user_id=record['user_id'],
                        date=record['date'],
                        time=record['time'],
                        record_type=record['record_type']
                    )
                    
                    db.add(time_record)
                    db.commit()
                    db.refresh(time_record)
                    print(f"    ✓ Created record ID: {time_record.id}")
                    
                    # Small delay to avoid potential timestamp issues
                    import time as time_module
                    time_module.sleep(0.1)
        
        print("\nTest data generation completed successfully!")
        
    except Exception as e:
        print(f"\nError generating test data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
