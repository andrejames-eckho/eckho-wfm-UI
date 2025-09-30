#!/usr/bin/env python3
"""
Script to test the daily summary service with a specific date.
"""
import sys
import os
from datetime import date, datetime
from sqlalchemy.orm import Session

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import app modules
try:
    from app.database import SessionLocal
    from app.models import User, TimeRecord, RecordType
    from app.services.time_record_service import TimeRecordService
    from app.services.user_service import UserService
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running this script from the backend directory and the app module is in your PYTHONPATH.")
    sys.exit(1)

def test_daily_summary(user_id: int, target_date: date):
    """Test getting daily summary for a specific user and date."""
    db = SessionLocal()
    try:
        # Get user info
        user_service = UserService()
        user = user_service.get(db, user_id)
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

        print("=" * 50)
        
        # Print raw summary for debugging
        print("\n=== RAW SUMMARY DATA ===")
        print(summary)
        print("=" * 50)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Test with test_user1 (ID: 1) for September 26, 2025
    test_date = date(2025, 9, 26)
    test_user_id = 1  # test_user1
    
    print(f"Testing daily summary for user ID {test_user_id} on {test_date}...")
    test_daily_summary(test_user_id, test_date)
