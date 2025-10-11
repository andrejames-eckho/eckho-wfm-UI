import requests
import json
from datetime import datetime, timedelta, time, date
import random
import time as time_module
from typing import List, Dict, Any, Optional
import os

# Base URL of your API
BASE_URL = "http://localhost:8000"  # Update if your API is running on a different URL

def get_users() -> List[Dict[str, Any]]:
    """Get all users from the API"""
    url = f"{BASE_URL}/users/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting users: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code} - {e.response.text}")
        return []

def get_user_time_records(user_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Dict[str, Any]]:
    """Get time records for a specific user"""
    url = f"{BASE_URL}/users/{user_id}/time-records"
    params = {}
    
    if start_date:
        params["start_date"] = start_date.isoformat()
    if end_date:
        params["end_date"] = end_date.isoformat()
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting time records for user {user_id}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code} - {e.response.text}")
        return []

def create_time_record(record_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a time record via the API"""
    url = f"{BASE_URL}/time-records/"
    
    try:
        # Convert date and time to string format expected by the API
        record_data = record_data.copy()
        record_data['date'] = record_data['date'].isoformat()
        record_data['time'] = record_data['time'].isoformat()
        
        response = requests.post(url, json=record_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating time record: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.status_code} - {e.response.text}")
        return None

def generate_workday_records(user_id: int, work_date: datetime) -> List[Dict[str, Any]]:
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
    break_out = (datetime.combine(work_date, break_in) + timedelta(minutes=break_duration)).time()
    
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
    print("Starting time record generation test...")
    
    # Get all existing users
    print("Fetching existing users...")
    users = get_users()
    
    if not users:
        print("No users found in the system. Please create users first.")
        return
    
    print(f"Found {len(users)} users in the system.")
    
    # Filter users to only include active ones if needed
    active_users = [user for user in users if user.get('is_active', True)]
    
    if not active_users:
        print("No active users found. Please activate users first.")
        return
    
    print(f"Found {len(active_users)} active users.")
    
    # Limit to first 2 users if there are more
    selected_users = active_users[:2]
    
    print("\nSelected users for time record generation:")
    for user in selected_users:
        print(f"- {user['username']} (ID: {user['id']}, Department: {user.get('department', 'N/A')})")
    
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
    for user in selected_users:
        print(f"\nGenerating time records for user: {user['username']} (ID: {user['id']})")
        
        # Check if user already has records for these dates
        existing_records = get_user_time_records(
            user_id=user['id'],
            start_date=workdays[0],
            end_date=workdays[-1]
        )
        
        if existing_records:
            existing_dates = set(record['date'] for record in existing_records)
            print(f"Found {len(existing_dates)} days with existing records")
        else:
            existing_dates = set()
        
        for workday in workdays:
            workday_str = workday.isoformat()
            if workday_str in existing_dates:
                print(f"Skipping {workday_str} - records already exist")
                continue
                
            print(f"\nCreating records for {workday.strftime('%A, %Y-%m-%d')}")
            records = generate_workday_records(user['id'], workday)
            
            for record in records:
                print(f"  - {record['record_type']} at {record['time'].strftime('%H:%M')}")
                created = create_time_record(record)
                if created:
                    print(f"    ✓ Created record ID: {created.get('id', 'unknown')}")
                else:
                    print(f"    ✗ Failed to create {record['record_type']} record")
                # Small delay to avoid overwhelming the API
                time_module.sleep(0.5)
    
    print("\nTime record generation completed!")
    
    # Generate time records for the last 4 workdays (excluding weekends)
    today = datetime.now().date()
    workdays = []
    days_back = 1
    
    while len(workdays) < 4:
        date_to_check = today - timedelta(days=days_back)
        # Skip weekends (5=Saturday, 6=Sunday)
        if date_to_check.weekday() < 5:  # 0-4 = Monday-Friday
            workdays.append(date_to_check)
        days_back += 1
    
    # Sort workdays in chronological order
    workdays.sort()
    
    # Create time records for each user
    for user in created_users:
        print(f"\nGenerating time records for user: {user['username']}")
        
        for workday in workdays:
            print(f"\nWorkday: {workday.strftime('%A, %Y-%m-%d')}")
            records = generate_workday_records(user['id'], workday)
            
            for record in records:
                print(f"Creating record: {record['record_type']} at {record['time'].strftime('%H:%M')}")
                created = create_time_record(record)
                if created:
                    print(f"  ✓ Created: {created}")
                else:
                    print(f"  ✗ Failed to create record")
                # Small delay to avoid overwhelming the API
                time_module.sleep(0.5)
    
    print("\nTest completed successfully!")
    print("\nCreated users:")
    for user in created_users:
        print(f"- {user['username']} (ID: {user['id']})")

if __name__ == "__main__":
    main()
