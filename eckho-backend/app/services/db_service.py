from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.db_models import Admin, Employee, CurrentTimeTracking, TimeRecord, EmployeeStatusEnum
from app.models.models import Employee as EmployeeModel, TimeRecord as TimeRecordModel, TimeTrackingData, EmployeeStatus, EmployeeUpdateRequest
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import List, Optional
import random

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_admin_db(db: Session, username: str, password: str) -> bool:
    """Authenticate admin against database"""
    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin and verify_password(password, admin.password_hash):
        return True
    return False

def authenticate_employee_db(db: Session, username: str, password: str) -> Optional[int]:
    """Authenticate employee against database and return employee ID"""
    employee = db.query(Employee).filter(Employee.username == username).first()
    if employee and verify_password(password, employee.password_hash):
        return employee.id
    return None

def get_all_employees_db(db: Session) -> List[EmployeeModel]:
    """Get all employees from database"""
    employees = db.query(Employee).all()
    result = []
    
    for emp in employees:
        # Get current tracking data
        tracking = db.query(CurrentTimeTracking).filter(
            CurrentTimeTracking.employee_id == emp.id
        ).first()
        
        if tracking:
            employee_model = EmployeeModel(
                id=emp.id,
                firstName=emp.first_name,
                lastName=emp.last_name,
                username=emp.username,
                type=emp.employee_type,
                phoneNumber=getattr(emp, 'phone_number', None),
                timeIn=tracking.time_in,
                timeOut=tracking.time_out,
                breakIn=tracking.break_in,
                breakOut=tracking.break_out,
                status=EmployeeStatus(tracking.status.value),
                expectedStartTime=emp.expected_start_time
            )
        else:
            employee_model = EmployeeModel(
                id=emp.id,
                firstName=emp.first_name,
                lastName=emp.last_name,
                username=emp.username,
                type=emp.employee_type,
                phoneNumber=getattr(emp, 'phone_number', None),
                timeIn=None,
                timeOut=None,
                breakIn=None,
                breakOut=None,
                status=EmployeeStatus.NOT_STARTED,
                expectedStartTime=emp.expected_start_time
            )
        
        result.append(employee_model)
    
    return result

def get_employee_by_id_db(db: Session, employee_id: int) -> Optional[EmployeeModel]:
    """Get employee by ID from database"""
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        return None
    
    # Get current tracking data
    tracking = db.query(CurrentTimeTracking).filter(
        CurrentTimeTracking.employee_id == emp.id
    ).first()
    
    if tracking:
        return EmployeeModel(
            id=emp.id,
            firstName=emp.first_name,
            lastName=emp.last_name,
            username=emp.username,
            type=emp.employee_type,
            phoneNumber=getattr(emp, 'phone_number', None),
            timeIn=tracking.time_in,
            timeOut=tracking.time_out,
            breakIn=tracking.break_in,
            breakOut=tracking.break_out,
            status=EmployeeStatus(tracking.status.value),
            expectedStartTime=emp.expected_start_time
        )
    else:
        return EmployeeModel(
            id=emp.id,
            firstName=emp.first_name,
            lastName=emp.last_name,
            username=emp.username,
            type=emp.employee_type,
            phoneNumber=getattr(emp, 'phone_number', None),
            timeIn=None,
            timeOut=None,
            breakIn=None,
            breakOut=None,
            status=EmployeeStatus.NOT_STARTED,
            expectedStartTime=emp.expected_start_time
        )

def get_or_create_current_tracking(db: Session, employee_id: int) -> CurrentTimeTracking:
    """Get or create current day tracking for employee"""
    tracking = db.query(CurrentTimeTracking).filter(
        CurrentTimeTracking.employee_id == employee_id
    ).first()
    
    if not tracking:
        tracking = CurrentTimeTracking(
            employee_id=employee_id,
            status=EmployeeStatusEnum.NOT_STARTED
        )
        db.add(tracking)
        db.commit()
        db.refresh(tracking)
    
    return tracking

def update_time_tracking_db(db: Session, employee_id: int, action: str, current_time: str) -> tuple[bool, str, Optional[TimeTrackingData]]:
    """Update time tracking in database"""
    tracking = get_or_create_current_tracking(db, employee_id)
    
    if action == "time_in":
        if tracking.time_in:
            return False, "Already timed in for today", None
        tracking.time_in = current_time
        tracking.status = EmployeeStatusEnum.ON_DUTY
        message = f"Timed in at {current_time}"
        
    elif action == "time_out":
        if not tracking.time_in:
            return False, "Must time in first", None
        if tracking.time_out:
            return False, "Already timed out for today", None
        tracking.time_out = current_time
        tracking.status = EmployeeStatusEnum.COMPLETED
        message = f"Timed out at {current_time}"
        
    elif action == "break_in":
        if not tracking.time_in:
            return False, "Must time in first", None
        if tracking.break_in and not tracking.break_out:
            return False, "Already on break", None
        tracking.break_in = current_time
        tracking.status = EmployeeStatusEnum.ON_BREAK
        message = f"Break started at {current_time}"
        
    elif action == "break_out":
        if not tracking.break_in:
            return False, "Must start break first", None
        if tracking.break_out:
            return False, "Break already ended", None
        tracking.break_out = current_time
        tracking.status = EmployeeStatusEnum.ON_DUTY
        message = f"Break ended at {current_time}"
    else:
        return False, "Invalid action", None
    
    tracking.updated_at = datetime.utcnow()
    db.commit()
    
    # Return tracking data
    tracking_data = TimeTrackingData(
        timeIn=tracking.time_in,
        timeOut=tracking.time_out,
        breakIn=tracking.break_in,
        breakOut=tracking.break_out,
        status=EmployeeStatus(tracking.status.value)
    )
    
    return True, message, tracking_data

def get_current_tracking_db(db: Session, employee_id: int) -> TimeTrackingData:
    """Get current tracking data for employee"""
    tracking = get_or_create_current_tracking(db, employee_id)
    
    return TimeTrackingData(
        timeIn=tracking.time_in,
        timeOut=tracking.time_out,
        breakIn=tracking.break_in,
        breakOut=tracking.break_out,
        status=EmployeeStatus(tracking.status.value)
    )

def get_time_records_db(db: Session, employee_id: int, months: int = 3) -> List[TimeRecordModel]:
    """Get historical time records for employee"""
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=months * 30)
    
    records = db.query(TimeRecord).filter(
        and_(
            TimeRecord.employee_id == employee_id,
            TimeRecord.date >= start_date,
            TimeRecord.date <= end_date
        )
    ).order_by(TimeRecord.date.desc()).all()
    
    result = []
    for record in records:
        time_record = TimeRecordModel(
            id=record.id,
            employeeId=record.employee_id,
            date=record.date,
            expectedTimeIn=record.expected_time_in,
            expectedTimeOut=record.expected_time_out,
            timeIn=record.time_in,
            timeOut=record.time_out,
            breakIn=record.break_in,
            breakOut=record.break_out,
            status=EmployeeStatus(record.status.value)
        )
        result.append(time_record)
    
    return result

def get_employees_for_date_db(db: Session, target_date: datetime) -> List[EmployeeModel]:
    """Get all employees with their time records for a specific date"""
    employees = db.query(Employee).all()
    result = []
    
    for emp in employees:
        # Find time record for the target date
        record = db.query(TimeRecord).filter(
            and_(
                TimeRecord.employee_id == emp.id,
                TimeRecord.date >= target_date.replace(hour=0, minute=0, second=0, microsecond=0),
                TimeRecord.date < target_date.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            )
        ).first()
        
        if record:
            employee_model = EmployeeModel(
                id=emp.id,
                firstName=emp.first_name,
                lastName=emp.last_name,
                timeIn=record.time_in,
                timeOut=record.time_out,
                breakIn=record.break_in,
                breakOut=record.break_out,
                status=EmployeeStatus(record.status.value),
                expectedStartTime=emp.expected_start_time
            )
        else:
            employee_model = EmployeeModel(
                id=emp.id,
                firstName=emp.first_name,
                lastName=emp.last_name,
                timeIn="-",
                timeOut="-",
                breakIn="-",
                breakOut="-",
                status=EmployeeStatus.NO_RECORD,
                expectedStartTime=emp.expected_start_time
            )
        
        result.append(employee_model)
    
    return result

def update_employee_status_db(db: Session, employee_id: int, status: EmployeeStatus) -> bool:
    """Update employee status in current tracking"""
    tracking = get_or_create_current_tracking(db, employee_id)
    tracking.status = EmployeeStatusEnum(status.value)
    tracking.updated_at = datetime.utcnow()
    db.commit()
    return True

def get_dashboard_summary_db(db: Session) -> dict:
    """Get dashboard summary statistics"""
    total_employees = db.query(Employee).count()
    
    # Get status counts from current tracking
    status_counts = {}
    trackings = db.query(CurrentTimeTracking).all()
    
    for tracking in trackings:
        status = EmployeeStatus(tracking.status.value)
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Count employees without tracking as NOT_STARTED
    employees_with_tracking = len(trackings)
    employees_without_tracking = total_employees - employees_with_tracking
    if employees_without_tracking > 0:
        status_counts[EmployeeStatus.NOT_STARTED] = status_counts.get(EmployeeStatus.NOT_STARTED, 0) + employees_without_tracking
    
    return {
        "total_employees": total_employees,
        "status_breakdown": {status.value: count for status, count in status_counts.items()},
        "active_employees": status_counts.get(EmployeeStatus.ON_DUTY, 0),
        "on_break": status_counts.get(EmployeeStatus.ON_BREAK, 0),
        "overtime": status_counts.get(EmployeeStatus.OVERTIME, 0),
        "late": status_counts.get(EmployeeStatus.LATE, 0)
    }

def update_employee_db(db: Session, employee_id: int, update_data: EmployeeUpdateRequest) -> Optional[EmployeeModel]:
    """Update employee details in database"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        return None
    
    # If password change is requested, verify old password first
    if update_data.password:
        if not update_data.oldPassword:
            raise ValueError("Current password is required to change password")
        
        if not verify_password(update_data.oldPassword, employee.password_hash):
            raise ValueError("Current password is incorrect")
    
    # Update employee fields
    employee.first_name = update_data.firstName
    employee.last_name = update_data.lastName
    employee.username = update_data.username
    employee.employee_type = update_data.type
    employee.expected_start_time = update_data.expectedStartTime
    
    # Update password if provided and verified
    if update_data.password:
        employee.password_hash = hash_password(update_data.password)
    
    # Note: phoneNumber is not in the current database schema
    # If you want to add it, you'll need to create a migration
    
    try:
        db.commit()
        db.refresh(employee)
        
        # Return updated employee data
        tracking = db.query(CurrentTimeTracking).filter(
            CurrentTimeTracking.employee_id == employee.id
        ).first()
        
        if tracking:
            return EmployeeModel(
                id=employee.id,
                firstName=employee.first_name,
                lastName=employee.last_name,
                username=employee.username,
                type=employee.employee_type,
                phoneNumber=getattr(employee, 'phone_number', None),
                timeIn=tracking.time_in,
                timeOut=tracking.time_out,
                breakIn=tracking.break_in,
                breakOut=tracking.break_out,
                status=EmployeeStatus(tracking.status.value),
                expectedStartTime=employee.expected_start_time
            )
        else:
            return EmployeeModel(
                id=employee.id,
                firstName=employee.first_name,
                lastName=employee.last_name,
                username=employee.username,
                type=employee.employee_type,
                phoneNumber=getattr(employee, 'phone_number', None),
                timeIn=None,
                timeOut=None,
                breakIn=None,
                breakOut=None,
                status=EmployeeStatus.NOT_STARTED,
                expectedStartTime=employee.expected_start_time
            )
    except Exception as e:
        db.rollback()
        raise e

def hash_password(password: str) -> str:
    return pwd_context.hash(password)
