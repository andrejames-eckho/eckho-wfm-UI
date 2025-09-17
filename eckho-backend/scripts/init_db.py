import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sqlalchemy.orm import Session
from app.models.db_models import Base, Admin, Employee, CurrentTimeTracking, TimeRecord, EmployeeStatusEnum
from app.services.database import engine, SessionLocal
from passlib.context import CryptContext
from datetime import datetime, timedelta
import random

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def init_admin_data(db: Session):
    """Initialize admin data"""
    # Check if admin already exists
    existing_admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not existing_admin:
        admin = Admin(
            username="admin",
            password_hash=hash_password("admin123")
        )
        db.add(admin)
        db.commit()
        print("Admin user created")

def init_employee_data(db: Session):
    """Initialize employee data with dummy employees"""
    
    # Warehouse employees
    warehouse_employees = [
        {"id": 1, "first_name": "John", "last_name": "Smith", "username": "john.smith"},
        {"id": 2, "first_name": "Sarah", "last_name": "Johnson", "username": "sarah.johnson"},
        {"id": 3, "first_name": "Mike", "last_name": "Davis", "username": "mike.davis"},
        {"id": 4, "first_name": "Emily", "last_name": "Wilson", "username": "emily.wilson"},
        {"id": 5, "first_name": "David", "last_name": "Brown", "username": "david.brown"},
        {"id": 6, "first_name": "Lisa", "last_name": "Anderson", "username": "lisa.anderson"},
    ]
    
    # Field employees
    field_employees = [
        {"id": 101, "first_name": "Ava", "last_name": "Martinez", "username": "ava.martinez", "expected_start_time": "11:30 PM"},
        {"id": 102, "first_name": "Noah", "last_name": "Clark", "username": "noah.clark", "expected_start_time": "09:00 AM"},
        {"id": 103, "first_name": "Mia", "last_name": "Lee", "username": "mia.lee", "expected_start_time": "07:00 AM"},
        {"id": 104, "first_name": "Ethan", "last_name": "Hernandez", "username": "ethan.hernandez", "expected_start_time": "10:00 AM"},
        {"id": 105, "first_name": "Isabella", "last_name": "Walker", "username": "isabella.walker", "expected_start_time": "09:30 PM"},
    ]
    
    # Create warehouse employees
    for emp_data in warehouse_employees:
        existing_emp = db.query(Employee).filter(Employee.id == emp_data["id"]).first()
        if not existing_emp:
            employee = Employee(
                id=emp_data["id"],
                first_name=emp_data["first_name"],
                last_name=emp_data["last_name"],
                username=emp_data["username"],
                password_hash=hash_password("emp123"),
                employee_type="warehouse"
            )
            db.add(employee)
    
    # Create field employees
    for emp_data in field_employees:
        existing_emp = db.query(Employee).filter(Employee.id == emp_data["id"]).first()
        if not existing_emp:
            employee = Employee(
                id=emp_data["id"],
                first_name=emp_data["first_name"],
                last_name=emp_data["last_name"],
                username=emp_data["username"],
                password_hash=hash_password("emp123"),
                employee_type="field",
                expected_start_time=emp_data["expected_start_time"]
            )
            db.add(employee)
    
    db.commit()
    print("Employee data initialized")

def init_current_tracking_data(db: Session):
    """Initialize current day tracking data with realistic statuses"""
    
    # Sample current tracking data
    tracking_data = [
        {"employee_id": 1, "time_in": "08:00 AM", "time_out": "05:00 PM", "break_in": "12:00 PM", "break_out": "01:00 PM", "status": EmployeeStatusEnum.ON_DUTY},
        {"employee_id": 2, "time_in": "08:15 AM", "time_out": "06:30 PM", "break_in": "12:30 PM", "break_out": "01:30 PM", "status": EmployeeStatusEnum.OVERTIME},
        {"employee_id": 3, "time_in": "09:30 AM", "break_in": "12:00 PM", "break_out": "01:00 PM", "status": EmployeeStatusEnum.LATE},
        {"employee_id": 4, "time_in": "08:00 AM", "time_out": "04:30 PM", "break_in": "02:00 PM", "status": EmployeeStatusEnum.ON_BREAK},
        {"employee_id": 5, "time_in": "08:00 AM", "time_out": "04:00 PM", "break_in": "12:00 PM", "break_out": "01:00 PM", "status": EmployeeStatusEnum.UNDERTIME},
        {"employee_id": 6, "time_in": "08:00 AM", "time_out": "06:00 PM", "break_in": "03:30 PM", "break_out": "04:30 PM", "status": EmployeeStatusEnum.ON_DUTY},
        {"employee_id": 101, "time_in": "11:30 PM", "break_in": "12:10 AM", "break_out": "12:50 AM", "status": EmployeeStatusEnum.ON_DUTY},
        {"employee_id": 102, "time_in": "09:10 AM", "time_out": "05:40 PM", "break_in": "01:00 PM", "status": EmployeeStatusEnum.ON_BREAK},
        {"employee_id": 103, "time_in": "07:55 AM", "time_out": "03:30 PM", "break_in": "11:30 AM", "break_out": "12:10 PM", "status": EmployeeStatusEnum.UNDERTIME},
        {"employee_id": 104, "time_in": "10:05 AM", "time_out": "07:20 PM", "break_in": "02:15 PM", "break_out": "02:55 PM", "status": EmployeeStatusEnum.OVERTIME},
        {"employee_id": 105, "time_in": "09:40 PM", "time_out": "06:30 AM", "break_in": "12:45 AM", "break_out": "01:25 AM", "status": EmployeeStatusEnum.LATE},
    ]
    
    for track_data in tracking_data:
        existing_tracking = db.query(CurrentTimeTracking).filter(
            CurrentTimeTracking.employee_id == track_data["employee_id"]
        ).first()
        
        if not existing_tracking:
            tracking = CurrentTimeTracking(
                employee_id=track_data["employee_id"],
                time_in=track_data.get("time_in"),
                time_out=track_data.get("time_out"),
                break_in=track_data.get("break_in"),
                break_out=track_data.get("break_out"),
                status=track_data["status"]
            )
            db.add(tracking)
    
    db.commit()
    print("Current tracking data initialized")

def generate_historical_records(db: Session):
    """Generate historical time records for all employees"""
    employees = db.query(Employee).all()
    
    for employee in employees:
        # Generate records for the last 3 months
        today = datetime.now()
        
        for month_offset in range(3):
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
                
                record_id = f"{employee.id}-{int(record_date.timestamp())}"
                
                # Check if record already exists
                existing_record = db.query(TimeRecord).filter(TimeRecord.id == record_id).first()
                if existing_record:
                    continue
                
                # Generate realistic time data
                if employee.employee_type == "field" and employee.expected_start_time:
                    expected_start = employee.expected_start_time
                    # Add variance for field employees
                    variance_minutes = random.randint(-30, 30)
                else:
                    expected_start = "08:00 AM"
                    variance_minutes = random.randint(-15, 60)
                
                # Calculate actual times with variance
                base_hour = 8 if "AM" in expected_start else 20
                if "11:30 PM" in expected_start:
                    base_hour = 23
                elif "09:30 PM" in expected_start:
                    base_hour = 21
                
                actual_start_minutes = base_hour * 60 + variance_minutes
                if actual_start_minutes < 0:
                    actual_start_minutes += 24 * 60
                elif actual_start_minutes >= 24 * 60:
                    actual_start_minutes -= 24 * 60
                
                start_hour = actual_start_minutes // 60
                start_minute = actual_start_minutes % 60
                
                time_in = f"{start_hour:02d}:{start_minute:02d}"
                if start_hour == 0:
                    time_in = f"12:{start_minute:02d} AM"
                elif start_hour < 12:
                    time_in = f"{start_hour}:{start_minute:02d} AM"
                elif start_hour == 12:
                    time_in = f"12:{start_minute:02d} PM"
                else:
                    time_in = f"{start_hour-12}:{start_minute:02d} PM"
                
                # Calculate end time (8-9 hours later)
                work_duration = random.randint(7*60, 9*60)  # 7-9 hours in minutes
                end_minutes = actual_start_minutes + work_duration
                if end_minutes >= 24 * 60:
                    end_minutes -= 24 * 60
                
                end_hour = end_minutes // 60
                end_min = end_minutes % 60
                
                if end_hour == 0:
                    time_out = f"12:{end_min:02d} AM"
                elif end_hour < 12:
                    time_out = f"{end_hour}:{end_min:02d} AM"
                elif end_hour == 12:
                    time_out = f"12:{end_min:02d} PM"
                else:
                    time_out = f"{end_hour-12}:{end_min:02d} PM"
                
                # Break times
                break_start_minutes = actual_start_minutes + random.randint(3*60, 5*60)
                if break_start_minutes >= 24 * 60:
                    break_start_minutes -= 24 * 60
                
                break_hour = break_start_minutes // 60
                break_min = break_start_minutes % 60
                
                if break_hour == 0:
                    break_in = f"12:{break_min:02d} AM"
                elif break_hour < 12:
                    break_in = f"{break_hour}:{break_min:02d} AM"
                elif break_hour == 12:
                    break_in = f"12:{break_min:02d} PM"
                else:
                    break_in = f"{break_hour-12}:{break_min:02d} PM"
                
                break_end_minutes = break_start_minutes + random.randint(30, 60)
                if break_end_minutes >= 24 * 60:
                    break_end_minutes -= 24 * 60
                
                break_end_hour = break_end_minutes // 60
                break_end_min = break_end_minutes % 60
                
                if break_end_hour == 0:
                    break_out = f"12:{break_end_min:02d} AM"
                elif break_end_hour < 12:
                    break_out = f"{break_end_hour}:{break_end_min:02d} AM"
                elif break_end_hour == 12:
                    break_out = f"12:{break_end_min:02d} PM"
                else:
                    break_out = f"{break_end_hour-12}:{break_end_min:02d} PM"
                
                # Determine status based on timing
                status = EmployeeStatusEnum.ON_TIME
                if variance_minutes > 15:
                    status = EmployeeStatusEnum.LATE
                elif work_duration > 8.5 * 60:
                    status = EmployeeStatusEnum.OVERTIME
                elif work_duration < 7.5 * 60:
                    status = EmployeeStatusEnum.UNDERTIME
                
                record = TimeRecord(
                    id=record_id,
                    employee_id=employee.id,
                    date=record_date,
                    expected_time_in=expected_start,
                    expected_time_out="05:00 PM" if employee.employee_type == "warehouse" else None,
                    time_in=time_in,
                    time_out=time_out,
                    break_in=break_in,
                    break_out=break_out,
                    status=status
                )
                db.add(record)
    
    db.commit()
    print("Historical time records generated")

def initialize_database():
    """Initialize the entire database with all data"""
    print("Creating database tables...")
    create_tables()
    
    db = SessionLocal()
    try:
        print("Initializing admin data...")
        init_admin_data(db)
        
        print("Initializing employee data...")
        init_employee_data(db)
        
        print("Initializing current tracking data...")
        init_current_tracking_data(db)
        
        print("Generating historical records...")
        generate_historical_records(db)
        
        print("Database initialization complete!")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    initialize_database()
