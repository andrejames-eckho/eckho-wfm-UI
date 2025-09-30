from datetime import date, time, timedelta
import pytest
from app.services.time_record_service import TimeRecordService
from app.models import RecordType

def test_get_weekly_summary(db_session, test_user, test_records):
    """Test getting weekly summary of time records"""
    print("\n=== Testing get_weekly_summary ===")
    
    # Create time record service
    time_service = TimeRecordService()
    
    # Get today's date and find the start of the week (Monday)
    today = date(2025, 9, 30)  # Using a fixed date for consistent testing
    monday = today - timedelta(days=today.weekday())  # Get Monday of the current week
    
    print(f"\nTesting week of {monday} to {monday + timedelta(days=6)}")
    
    # Test getting current week's summary
    result = time_service.get_weekly_summary(db_session, today)
    
    # Print the full response for inspection
    print("\nWeekly Summary Response:")
    print("-" * 50)
    print(f"Week Start: {result['week_start']}")
    print(f"Week End: {result['week_end']}")
    print(f"Users with records: {len(result['records'])}")
    
    # Verify the structure of the response
    assert "week_start" in result
    assert "week_end" in result
    assert "records" in result
    
    # Verify the week range (should be Monday to Sunday)
    assert result["week_start"] == monday.isoformat()
    assert result["week_end"] == (monday + timedelta(days=6)).isoformat()
    
    # Verify records for the user exist
    user_id_str = str(test_user.id)
    assert user_id_str in result["records"]
    
    print(f"\nRecords for user {user_id_str}:")
    print("-" * 50)
    
    # Verify we have records for each day of the current week
    for day in range(7):
        current_date = (monday + timedelta(days=day)).isoformat()
        if today >= (monday + timedelta(days=day)):  # Only check past and current days
            assert current_date in result["records"][user_id_str]
            
            # Get records for this date
            date_records = result["records"][user_id_str][current_date]
            print(f"\n{current_date} - {len(date_records)} records:")
            
            # Print each record for this date
            for record in date_records:
                print(f"  - {record['time']} {record['record_type']} (ID: {record['id']})")
            
            # Verify all record types exist for each day
            record_types = {r["record_type"] for r in date_records}
            print(f"  Record types: {', '.join(sorted(record_types))}")
    
    print("\n✅ Weekly summary test passed!")

def test_get_monthly_summary(db_session, test_user, test_records):
    """Test getting monthly summary of time records"""
    print("\n=== Testing get_monthly_summary ===")
    
    # Create time record service
    time_service = TimeRecordService()
    
    # Get current year and month
    today = date.today()
    year = today.year
    month = today.month
    
    print(f"\nTesting month: {year}-{month:02d}")
    
    # Test getting current month's summary
    result = time_service.get_monthly_summary(db_session, year, month)
    
    # Print the full response for inspection
    print("\nMonthly Summary Response:")
    print("-" * 50)
    print(f"Month: {result['month']}")
    print(f"Month Start: {result.get('month_start', 'N/A')}")
    print(f"Month End: {result.get('month_end', 'N/A')}")
    print(f"Users with records: {len(result['records'])}")
    
    # Verify the month and year
    assert result["year"] == year
    assert result["month"] == month
    
    # Verify records for the user exist
    user_id_str = str(test_user.id)
    assert user_id_str in result["records"]
    
    # Get all unique dates from test records
    test_dates = {record.date for record in test_records}
    
    print("-" * 50)
    
    # Verify we have records for each test date in the current month
    for test_date in sorted(test_dates):
        if test_date.month == month and test_date.year == year:
            date_str = test_date.isoformat()
            assert date_str in result["records"][user_id_str]
            
            # Get records for this date
            date_records = result["records"][user_id_str][date_str]
            print(f"\n{date_str} - {len(date_records)} records:")
            
            # Print each record for this date
            for record in date_records:
                print(f"  - {record['time']} {record['record_type']} (ID: {record['id']})")
            
            # Verify we have the expected record types for each day
            record_types = {r["record_type"] for r in date_records}
            print(f"  Record types: {', '.join(sorted(record_types))}")
            assert len(record_types) >= 2  # At least time in and time out
    
    print("\n✅ Monthly summary test passed!")

# This file uses pytest fixtures and should be run with pytest, not directly
