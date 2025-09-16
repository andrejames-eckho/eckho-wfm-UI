from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models import Employee, FieldEmployee, EmployeeCredentials, AdminCredentials, TimeTrackingData, EmployeeStatus, TimeRecord
import random
from dateutil.parser import parse

# Admin credentials
admin_credentials = AdminCredentials(
    username="admin",
    password="admin123"
)

# Employee credentials
employee_credentials = [
    EmployeeCredentials(id=1, username="john.smith", password="emp123", employeeId=1),
    EmployeeCredentials(id=2, username="sarah.johnson", password="emp123", employeeId=2),
    EmployeeCredentials(id=3, username="mike.davis", password="emp123", employeeId=3),
    EmployeeCredentials(id=4, username="emily.wilson", password="emp123", employeeId=4),
    EmployeeCredentials(id=5, username="david.brown", password="emp123", employeeId=5),
    EmployeeCredentials(id=6, username="lisa.anderson", password="emp123", employeeId=6),
    EmployeeCredentials(id=101, username="ava.martinez", password="emp123", employeeId=101),
    EmployeeCredentials(id=102, username="noah.clark", password="emp123", employeeId=102),
    EmployeeCredentials(id=103, username="mia.lee", password="emp123", employeeId=103),
    EmployeeCredentials(id=104, username="ethan.hernandez", password="emp123", employeeId=104),
    EmployeeCredentials(id=105, username="isabella.walker", password="emp123", employeeId=105),
]

# Warehouse employees (regular schedule 8AM-5PM)
warehouse_employees = [
    Employee(id=1, firstName="John", lastName="Smith", timeIn="08:00 AM", timeOut="05:00 PM", 
             breakIn="12:00 PM", breakOut="01:00 PM", status=EmployeeStatus.ON_DUTY),
    Employee(id=2, firstName="Sarah", lastName="Johnson", timeIn="08:15 AM", timeOut="06:30 PM", 
             breakIn="12:30 PM", breakOut="01:30 PM", status=EmployeeStatus.OVERTIME),
    Employee(id=3, firstName="Mike", lastName="Davis", timeIn="09:30 AM", timeOut=None, 
             breakIn="12:00 PM", breakOut="01:00 PM", status=EmployeeStatus.LATE),
    Employee(id=4, firstName="Emily", lastName="Wilson", timeIn="08:00 AM", timeOut="04:30 PM", 
             breakIn="02:00 PM", breakOut=None, status=EmployeeStatus.ON_BREAK),
    Employee(id=5, firstName="David", lastName="Brown", timeIn="08:00 AM", timeOut="04:00 PM", 
             breakIn="12:00 PM", breakOut="01:00 PM", status=EmployeeStatus.UNDERTIME),
    Employee(id=6, firstName="Lisa", lastName="Anderson", timeIn="08:00 AM", timeOut="06:00 PM", 
             breakIn="03:30 PM", breakOut="4:30 PM", status=EmployeeStatus.ON_DUTY),
]

# Field employees (flexible schedule)
field_employees = [
    FieldEmployee(id=101, firstName="Ava", lastName="Martinez", timeIn="11:30 PM", timeOut=None, 
                  breakIn="12:10 AM", breakOut="12:50 AM", expectedStartTime="11:30 PM", status=EmployeeStatus.ON_DUTY),
    FieldEmployee(id=102, firstName="Noah", lastName="Clark", timeIn="09:10 AM", timeOut="05:40 PM", 
                  breakIn="01:00 PM", breakOut=None, expectedStartTime="09:00 AM", status=EmployeeStatus.ON_BREAK),
    FieldEmployee(id=103, firstName="Mia", lastName="Lee", timeIn="07:55 AM", timeOut="03:30 PM", 
                  breakIn="11:30 AM", breakOut="12:10 PM", expectedStartTime="07:00 AM", status=EmployeeStatus.UNDERTIME),
    FieldEmployee(id=104, firstName="Ethan", lastName="Hernandez", timeIn="10:05 AM", timeOut="07:20 PM", 
                  breakIn="02:15 PM", breakOut="02:55 PM", expectedStartTime="10:00 AM", status=EmployeeStatus.OVERTIME),
    FieldEmployee(id=105, firstName="Isabella", lastName="Walker", timeIn="09:40 PM", timeOut="06:30 AM", 
                  breakIn="12:45 AM", breakOut="01:25 AM", expectedStartTime="09:30 PM", status=EmployeeStatus.LATE),
]

# Combine all employees
all_employees = warehouse_employees + field_employees

# Current day time tracking storage
current_day_tracking: Dict[int, TimeTrackingData] = {}

# Status colors mapping
status_colors = {
    EmployeeStatus.ON_DUTY: "bg-green-500",
    EmployeeStatus.ON_BREAK: "bg-gray-500",
    EmployeeStatus.OVERTIME: "bg-blue-500",
    EmployeeStatus.LATE: "bg-red-500",
    EmployeeStatus.UNDERTIME: "bg-yellow-500",
    EmployeeStatus.ON_TIME: "bg-teal-500",
    EmployeeStatus.NO_RECORD: "bg-gray-600"
}

def parse_time_to_minutes(time_str: Optional[str]) -> Optional[int]:
    """Parse time string to minutes since midnight"""
    if not time_str or not isinstance(time_str, str):
        return None
    
    try:
        time_str = time_str.strip()
        if not time_str or time_str == '-':
            return None
            
        parts = time_str.split(' ')
        if len(parts) != 2:
            return None
            
        time_part, meridiem = parts
        if ':' not in time_part:
            return None
            
        hour_str, minute_str = time_part.split(':')
        hour = int(hour_str)
        minute = int(minute_str)
        
        is_pm = meridiem.upper() == 'PM'
        
        if hour == 12:
            hour = 12 if is_pm else 0
        elif is_pm:
            hour += 12
            
        return hour * 60 + minute
    except (ValueError, IndexError):
        return None

def diff_minutes_wrap_midnight(start_min: Optional[int], end_min: Optional[int]) -> int:
    """Calculate minutes difference, wrapping around midnight if needed"""
    if start_min is None or end_min is None:
        return 0
    
    ONE_DAY = 24 * 60
    raw = end_min - start_min
    return raw if raw >= 0 else raw + ONE_DAY

def get_employee_status(employee: Employee) -> EmployeeStatus:
    """Calculate employee status based on time data"""
    time_in_min = parse_time_to_minutes(employee.timeIn)
    time_out_min = parse_time_to_minutes(employee.timeOut)
    break_in_min = parse_time_to_minutes(employee.breakIn)
    break_out_min = parse_time_to_minutes(employee.breakOut)
    
    # Incomplete states first
    if break_in_min is not None and break_out_min is None:
        return EmployeeStatus.ON_BREAK
    if time_in_min is not None and time_out_min is None:
        return EmployeeStatus.ON_DUTY
    
    # If we don't have complete required data, return existing status
    if time_in_min is None or time_out_min is None or break_in_min is None or break_out_min is None:
        return employee.status
    
    # Constants
    EXPECTED_START_TIME = "08:00 AM"
    EXPECTED_END_TIME = "05:00 PM"
    EXPECTED_WORK_MINUTES = 8 * 60  # 8 hours
    GRACE_MINUTES = 15
    
    expected_start_min = parse_time_to_minutes(getattr(employee, 'expectedStartTime', None) or EXPECTED_START_TIME)
    
    # For warehouse employees (no expectedStartTime)
    if not hasattr(employee, 'expectedStartTime') or not employee.expectedStartTime:
        expected_end_min = parse_time_to_minutes(EXPECTED_END_TIME)
        
        if expected_start_min is not None and expected_end_min is not None:
            is_late_beyond_grace = time_in_min > (expected_start_min + GRACE_MINUTES)
            is_early_departure = time_out_min < (expected_end_min - GRACE_MINUTES)
            is_overtime = time_out_min > (expected_end_min + GRACE_MINUTES)
            
            if is_late_beyond_grace:
                return EmployeeStatus.LATE
            if is_early_departure:
                return EmployeeStatus.UNDERTIME
            if is_overtime:
                return EmployeeStatus.OVERTIME
            return EmployeeStatus.ON_TIME
    else:
        # Field employees - calculate based on actual time worked
        break_duration = diff_minutes_wrap_midnight(break_in_min, break_out_min)
        gross_duration = diff_minutes_wrap_midnight(time_in_min, time_out_min)
        net_worked = max(0, gross_duration - break_duration)
        
        expected_work_minutes = EXPECTED_WORK_MINUTES
        
        is_late_beyond_grace = expected_start_min is not None and time_in_min > (expected_start_min + GRACE_MINUTES)
        within_work_grace = abs(net_worked - expected_work_minutes) <= GRACE_MINUTES
        
        if not is_late_beyond_grace and within_work_grace:
            return EmployeeStatus.ON_TIME
        if is_late_beyond_grace:
            return EmployeeStatus.LATE
        if net_worked > expected_work_minutes + GRACE_MINUTES:
            return EmployeeStatus.OVERTIME
        if net_worked < expected_work_minutes - GRACE_MINUTES:
            return EmployeeStatus.UNDERTIME
        return EmployeeStatus.ON_TIME
    
    return EmployeeStatus.ON_TIME

def initialize_employee_tracking(employee_id: int) -> TimeTrackingData:
    """Initialize time tracking for an employee"""
    if employee_id not in current_day_tracking:
        current_day_tracking[employee_id] = TimeTrackingData()
    return current_day_tracking[employee_id]

def get_employee_by_id(employee_id: int) -> Optional[Employee]:
    """Get employee by ID"""
    for emp in all_employees:
        if emp.id == employee_id:
            return emp
    return None

def get_employee_credentials(username: str) -> Optional[EmployeeCredentials]:
    """Get employee credentials by username"""
    for cred in employee_credentials:
        if cred.username == username:
            return cred
    return None

def generate_time_records(employee: Employee, months_back: int = 3) -> List[TimeRecord]:
    """Generate historical time records for an employee"""
    records = []
    today = datetime.now()
    
    for month_offset in range(months_back):
        current_month = datetime(today.year, today.month - month_offset, 1)
        if current_month.month <= 0:
            current_month = datetime(current_month.year - 1, current_month.month + 12, 1)
        
        # Get last day of month
        if current_month.month == 12:
            next_month = datetime(current_month.year + 1, 1, 1)
        else:
            next_month = datetime(current_month.year, current_month.month + 1, 1)
        
        last_day = (next_month - timedelta(days=1)).day
        
        for day in range(1, last_day + 1):
            record_date = datetime(current_month.year, current_month.month, day)
            
            # Skip future dates and weekends
            if record_date > today or record_date.weekday() >= 5:
                continue
            
            # Generate realistic time data
            expected_start_time = getattr(employee, 'expectedStartTime', '08:00 AM')
            expected_time_in_min = parse_time_to_minutes(expected_start_time)
            
            if expected_time_in_min is not None:
                # Add variance to start time
                variance_minutes = random.randint(-120, 120)  # ±2 hours
                actual_time_in_min = expected_time_in_min + variance_minutes
                
                # Normalize for day rollover
                if actual_time_in_min < 0:
                    actual_time_in_min += 24 * 60
                elif actual_time_in_min >= 24 * 60:
                    actual_time_in_min -= 24 * 60
                
                actual_hour = actual_time_in_min // 60
                actual_minute = actual_time_in_min % 60
                
                time_in = datetime.combine(record_date.date(), datetime.min.time().replace(hour=actual_hour, minute=actual_minute))
            else:
                # Fallback
                time_in_hour = random.randint(7, 9)
                time_in_minute = random.randint(0, 59)
                time_in = datetime.combine(record_date.date(), datetime.min.time().replace(hour=time_in_hour, minute=time_in_minute))
            
            # Calculate work duration
            if hasattr(employee, 'expectedStartTime') and employee.expectedStartTime:
                # Field employees - variable hours
                work_hours = 7.5 + random.random() * 2  # 7.5-9.5 hours
            else:
                # Warehouse employees - work until 5 PM with variance
                base_work_minutes = parse_time_to_minutes('05:00 PM') - parse_time_to_minutes(time_in.strftime('%I:%M %p'))
                if base_work_minutes:
                    variance_minutes = random.randint(-30, 30)
                    work_hours = max(4, (base_work_minutes + variance_minutes) / 60)
                else:
                    work_hours = 8
            
            time_out = time_in + timedelta(hours=work_hours)
            break_start = time_in + timedelta(hours=4)
            break_end = break_start + timedelta(minutes=30)
            
            # Create time record
            temp_employee = Employee(
                id=employee.id,
                firstName=employee.firstName,
                lastName=employee.lastName,
                timeIn=time_in.strftime('%I:%M %p'),
                timeOut=time_out.strftime('%I:%M %p'),
                breakIn=break_start.strftime('%I:%M %p'),
                breakOut=break_end.strftime('%I:%M %p'),
                expectedStartTime=getattr(employee, 'expectedStartTime', None)
            )
            
            record = TimeRecord(
                id=f"{employee.id}-{record_date.timestamp()}",
                employeeId=employee.id,
                date=record_date,
                expectedTimeIn=expected_start_time,
                expectedTimeOut='05:00 PM' if not hasattr(employee, 'expectedStartTime') or not employee.expectedStartTime else None,
                timeIn=time_in.strftime('%I:%M %p'),
                timeOut=time_out.strftime('%I:%M %p'),
                breakIn=break_start.strftime('%I:%M %p'),
                breakOut=break_end.strftime('%I:%M %p'),
                status=get_employee_status(temp_employee)
            )
            
            records.append(record)
    
    return sorted(records, key=lambda x: x.date, reverse=True)

def get_employees_with_time_records_for_date(target_date: datetime) -> List[Employee]:
    """Get all employees with their time records for a specific date"""
    result = []
    
    for employee in all_employees:
        records = generate_time_records(employee, 3)
        target_date_str = target_date.date()
        
        # Find record for target date
        time_record = None
        for record in records:
            if record.date.date() == target_date_str:
                time_record = record
                break
        
        if time_record:
            # Return employee with time record data
            updated_employee = Employee(
                id=employee.id,
                firstName=employee.firstName,
                lastName=employee.lastName,
                timeIn=time_record.timeIn,
                timeOut=time_record.timeOut,
                breakIn=time_record.breakIn,
                breakOut=time_record.breakOut,
                status=time_record.status,
                expectedStartTime=getattr(employee, 'expectedStartTime', None)
            )
        else:
            # Return employee without time record
            updated_employee = Employee(
                id=employee.id,
                firstName=employee.firstName,
                lastName=employee.lastName,
                timeIn='-',
                timeOut='-',
                breakIn='-',
                breakOut='-',
                status=EmployeeStatus.NO_RECORD,
                expectedStartTime=getattr(employee, 'expectedStartTime', None)
            )
        
        result.append(updated_employee)
    
    return result
