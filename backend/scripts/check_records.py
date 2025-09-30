#!/usr/bin/env python3
"""
Script to check time records in the database.
"""
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.database import SessionLocal
    from app.models import User, TimeRecord, RecordType
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def list_all_records(db: Session, limit: int = 10):
    """List all time records in the database."""
    print("\n=== TIME RECORDS IN DATABASE ===")
    records = db.query(TimeRecord).order_by(TimeRecord.date.desc(), TimeRecord.time.desc()).limit(limit).all()
    
    if not records:
        print("No time records found in the database.")
        return
    
    print(f"{'ID':<5} {'User ID':<8} {'Date':<12} {'Time':<8} {'Type':<12}")
    print("-" * 50)
    for record in records:
        print(f"{record.id:<5} {record.user_id:<8} {record.date} {record.time} {record.record_type.value}")

def main():
    """Main function to run the script."""
    db = SessionLocal()
    
    try:
        # List all users
        users = db.query(User).all()
        print("\n=== USERS IN DATABASE ===")
        print(f"{'ID':<5} {'Username':<15} {'Name':<20} {'Department':<15}")
        print("-" * 60)
        for user in users:
            print(f"{user.id:<5} {user.username:<15} {user.first_name} {user.last_name:<15} {user.department.value}")
        
        # List recent time records
        list_all_records(db, limit=20)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
