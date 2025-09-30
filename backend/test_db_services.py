import sys
import os
from datetime import datetime, date, time
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.models import User, TimeRecord, RecordType

def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def display_users_with_records():
    """Display all users and their time records"""
    print("\n=== Users and Their Time Records ===")
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all users with their time records count
        users = db.query(
            User,
            func.count(TimeRecord.id).label('record_count')
        ).outerjoin(
            TimeRecord, User.id == TimeRecord.user_id
        ).group_by(User.id).order_by(User.id).all()
        
        if not users:
            print("No users found in the database.")
            return
            
        print(f"\nFound {len(users)} users in the database.")
        
        # For each user, get their time records
        for user, record_count in users:
            print(f"\nUser: {user.first_name} {user.last_name} (ID: {user.id}, Username: {user.username})")
            print(f"Department: {user.department.value if hasattr(user, 'department') and user.department else 'Not specified'}")
            print(f"Total time records: {record_count}")
            
            # Get the 5 most recent time records
            recent_records = db.query(TimeRecord)\
                .filter(TimeRecord.user_id == user.id)\
                .order_by(TimeRecord.date.desc(), TimeRecord.time.desc())\
                .limit(5)\
                .all()
                
            if recent_records:
                print("  Most recent records:")
                for record in recent_records:
                    record_type = record.record_type.value if hasattr(record, 'record_type') and record.record_type else 'UNKNOWN'
                    time_str = record.time.strftime('%H:%M:%S') if hasattr(record, 'time') and record.time else 'N/A'
                    print(f"  - {record.date} {time_str} ({record_type})")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    print("🔍 Querying users and time records from the database...")
    display_users_with_records()
