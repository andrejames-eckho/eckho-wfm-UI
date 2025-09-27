import requests
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

# API base URL
BASE_URL = "http://localhost:8000"

# Test user data
test_users = [
    {
        "username": "test_user1",
        "first_name": "Test",
        "last_name": "User1",
        "department": "Field"
    },
    {
        "username": "test_user2",
        "first_name": "Test",
        "last_name": "User2",
        "department": "Warehouse"
    }
]

def create_test_users() -> List[Dict[str, Any]]:
    """Create test users and return their data."""
    created_users = []
    for user_data in test_users:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            created_users.append(response.json())
            print(f"Created user: {user_data['username']}")
        else:
            print(f"Error creating user {user_data['username']}: {response.text}")
    return created_users

def create_time_records(user_id: int, username: str, days_ago: int = 4):
    """Create time records for a user for the last 'days_ago' days."""
    record_types = ["Time In", "Time Out", "Break In", "Break Out"]
    
    for day in range(days_ago, 0, -1):
        record_date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
        
        # Create Time In (morning)
        time_record = {
            "user_id": user_id,
            "date": record_date,
            "time": "09:00:00",
            "record_type": "Time In"
        }
        response = requests.post(f"{BASE_URL}/time-records/", json=time_record)
        print(f"Created Time In for {username} on {record_date}")
        
        # Create Break In (mid-morning)
        time_record.update({
            "time": "12:00:00",
            "record_type": "Break In"
        })
        response = requests.post(f"{BASE_URL}/time-records/", json=time_record)
        print(f"Created Break In for {username} on {record_date}")
        
        # Create Break Out (after lunch)
        time_record.update({
            "time": "13:00:00",
            "record_type": "Break Out"
        })
        response = requests.post(f"{BASE_URL}/time-records/", json=time_record)
        print(f"Created Break Out for {username} on {record_date}")
        
        # Create Time Out (end of day)
        time_record.update({
            "time": "17:00:00",
            "record_type": "Time Out"
        })
        response = requests.post(f"{BASE_URL}/time-records/", json=time_record)
        print(f"Created Time Out for {username} on {record_date}")

def display_user_records():
    """Display all users and their time records."""
    # Get all users
    response = requests.get(f"{BASE_URL}/users/")
    users = response.json()
    
    for user in users:
        print(f"\nUser: {user['first_name']} {user['last_name']} ({user['department']})")
        print("-" * 50)
        
        # Get user's time records
        response = requests.get(f"{BASE_URL}/time-records/user/{user['id']}")
        records = response.json()
        
        # Group records by date
        records_by_date = {}
        for record in records:
            date_str = record['date']
            if date_str not in records_by_date:
                records_by_date[date_str] = []
            records_by_date[date_str].append(record)
        
        # Display records by date
        for date_str, date_records in records_by_date.items():
            print(f"\n{date_str}:")
            for record in sorted(date_records, key=lambda x: x['time']):
                print(f"  {record['time'][:5]} - {record['record_type']}")

def main():
    print("=== Starting API Test ===\n")
    
    # Step 1: Create test users
    print("Creating test users...")
    users = create_test_users()
    
    # Step 2: Create time records for each user
    print("\nCreating time records...")
    for user in users:
        create_time_records(user['id'], user['username'])
    
    # Step 3: Display all users and their records
    print("\n=== User Time Records ===\n")
    display_user_records()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
