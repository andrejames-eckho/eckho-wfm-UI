#!/usr/bin/env python3
"""
Script to show daily time tracking summary for a user from the PostgreSQL database.
"""
import sys
import os
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import app modules
try:
    from app.database import SessionLocal, engine
    from app.models import User, TimeRecord, RecordType
    from app.services.time_record_service import TimeRecordService
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this script from the backend directory and the app module is in your PYTHONPATH.")
    sys.exit(1)

def list_users(db: Session):
    """List all users in the database."""
    users = db.query(User).all()
    if not users:
        print("No users found in the database.")
        return []
    
    print("\nAvailable Users:")
    print("ID  | Username           | Name")
    print("-" * 50)
    for user in users:
        print(f"{user.id:3d} | {user.username:18} | {user.first_name} {user.last_name}")
    print()
    return users

def get_daily_summary(db: Session, user_id: int, target_date: date = None):
    """Get and display daily summary for a user."""
    if target_date is None:
        target_date = date.today()
    
    # Get user info
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        print(f"Error: User with ID {user_id} not found.")
        return
    
    # Get daily summary using the service
    time_service = TimeRecordService()
    summary = time_service.get_daily_summary(db, user_id, target_date)
    
    # Display results
    print(f"\n=== DAILY TIME SUMMARY ===")
    print(f"Date: {summary['date']}")
    print(f"User: {user.first_name} {user.last_name} (@{user.username})")
    print(f"Department: {user.department}")
    print("\nTime Records:")
    
    if not summary['records']:
        print("  No time records found for this date.")
    else:
        for record in summary['records']:
            print(f"  - {record['time']} - {record['record_type']}")
    
    print("=" * 50 + "\n")
    return summary

def main():
    """Main function to run the script."""
    db = SessionLocal()
    
    try:
        # List all users first
        users = list_users(db)
        if not users:
            return
        
        # Get user ID from command line or prompt
        if len(sys.argv) > 1:
            try:
                user_id = int(sys.argv[1])
            except ValueError:
                print("Error: User ID must be a number.")
                return
        else:
            user_id = input("Enter User ID: ")
            try:
                user_id = int(user_id)
            except ValueError:
                print("Error: User ID must be a number.")
                return
        
        # Get date from command line or use today
        target_date = None
        if len(sys.argv) > 2:
            try:
                target_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return
        
        # Get and display the daily summary
        get_daily_summary(db, user_id, target_date)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Add the parent directory to the Python path
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    
    main()
