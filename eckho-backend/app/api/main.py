from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
import json

from app.models.models import (
    LoginRequest, LoginResponse, UserRole, TimeTrackingRequest, TimeTrackingResponse,
    EmployeeListResponse, TimeRecordsResponse, DateRangeRequest,
    StatusUpdateRequest, Employee, TimeRecord, EmployeeUpdateRequest
)
from app.services.auth import (
    create_access_token, verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.services.database import get_db
from app.services.db_service import (
    authenticate_admin_db, authenticate_employee_db, get_all_employees_db,
    get_employee_by_id_db, update_time_tracking_db, get_current_tracking_db,
    get_time_records_db, get_employees_for_date_db, update_employee_status_db,
    get_dashboard_summary_db, update_employee_db
)

app = FastAPI(title="Eckho WFM Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Eckho WFM Backend API", "version": "1.0.0"}

@app.post("/api/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user login"""
    try:
        # Check admin credentials first
        if authenticate_admin_db(db, request.username, request.password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": request.username, "role": UserRole.ADMIN},
                expires_delta=access_token_expires
            )
            return LoginResponse(
                success=True,
                message="Admin login successful",
                user_type=UserRole.ADMIN,
                token=access_token
            )
        
        # Check employee credentials
        employee_id = authenticate_employee_db(db, request.username, request.password)
        if employee_id:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": request.username, "role": UserRole.EMPLOYEE, "employee_id": employee_id},
                expires_delta=access_token_expires
            )
            return LoginResponse(
                success=True,
                message="Employee login successful",
                user_type=UserRole.EMPLOYEE,
                employee_id=employee_id,
                token=access_token
            )
        
        return LoginResponse(
            success=False,
            message="Invalid username or password"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.get("/api/employees", response_model=EmployeeListResponse)
async def get_employees(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all employees (admin only)"""
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        employees = get_all_employees_db(db)
        return EmployeeListResponse(
            employees=employees,
            total=len(employees)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employees: {str(e)}")

@app.get("/api/employees/{employee_id}")
async def get_employee(employee_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get specific employee details"""
    # Admin can view any employee, employees can only view themselves
    if (current_user.get("role") != UserRole.ADMIN and 
        current_user.get("employee_id") != employee_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        employee = get_employee_by_id_db(db, employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employee: {str(e)}")

@app.put("/api/employees/{employee_id}")
async def update_employee(
    employee_id: int, 
    update_data: EmployeeUpdateRequest,
    current_user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """Update employee details (admin only)"""
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        updated_employee = update_employee_db(db, employee_id, update_data)
        if not updated_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"success": True, "message": "Employee updated successfully", "employee": updated_employee}
    except ValueError as e:
        # Handle password verification errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating employee: {str(e)}")

@app.post("/api/time-tracking", response_model=TimeTrackingResponse)
async def time_tracking_action(request: TimeTrackingRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Handle time tracking actions (time in/out, break in/out)"""
    # Employees can only track their own time, admins can track any employee's time
    if (current_user.get("role") != UserRole.ADMIN and 
        current_user.get("employee_id") != request.employeeId):
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        employee = get_employee_by_id_db(db, request.employeeId)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Get current time
        now = datetime.now()
        current_time = now.strftime('%I:%M %p')
        
        # Update time tracking in database
        success, message, tracking_data = update_time_tracking_db(db, request.employeeId, request.action, current_time)
        
        return TimeTrackingResponse(
            success=success,
            message=message,
            data=tracking_data
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Time tracking error: {str(e)}")

@app.get("/api/time-tracking/{employee_id}")
async def get_time_tracking(employee_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current time tracking status for an employee"""
    # Employees can only view their own data, admins can view any employee's data
    if (current_user.get("role") != UserRole.ADMIN and 
        current_user.get("employee_id") != employee_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    employee = get_employee_by_id_db(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    tracking = get_current_tracking_db(db, employee_id)
    return tracking

@app.get("/api/time-records/{employee_id}", response_model=TimeRecordsResponse)
async def get_time_records(
    employee_id: int, 
    months: int = 3,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get historical time records for an employee"""
    # Employees can only view their own records, admins can view any employee's records
    if (current_user.get("role") != UserRole.ADMIN and 
        current_user.get("employee_id") != employee_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    employee = get_employee_by_id_db(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    try:
        records = get_time_records_db(db, employee_id, months)
        return TimeRecordsResponse(
            records=records,
            total=len(records)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching time records: {str(e)}")

@app.post("/api/employees/date-records", response_model=EmployeeListResponse)
async def get_employees_for_date(
    request: DateRangeRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all employees with their time records for a specific date (admin only)"""
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        target_date = datetime.fromisoformat(request.startDate.replace('Z', '+00:00'))
        employees_with_records = get_employees_for_date_db(db, target_date)
        
        return EmployeeListResponse(
            employees=employees_with_records,
            total=len(employees_with_records)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching employee records: {str(e)}")

@app.put("/api/employees/{employee_id}/status")
async def update_employee_status(
    employee_id: int,
    request: StatusUpdateRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update employee status (admin only)"""
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    employee = get_employee_by_id_db(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    try:
        # Update the employee's status in current tracking
        success = update_employee_status_db(db, employee_id, request.status)
        if success:
            return {"success": True, "message": f"Status updated to {request.status}"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update status")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating status: {str(e)}")

@app.get("/api/status-colors")
async def get_status_colors():
    """Get status color mappings"""
    # Status colors mapping
    status_colors = {
        "On Duty": "bg-green-500",
        "On Break": "bg-gray-500",
        "Overtime": "bg-blue-500",
        "Late": "bg-red-500",
        "Undertime": "bg-yellow-500",
        "On Time": "bg-teal-500",
        "No Record": "bg-gray-600",
        "Not Started": "bg-gray-400",
        "Completed": "bg-purple-500"
    }
    return status_colors

@app.get("/api/dashboard/summary")
async def get_dashboard_summary(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get dashboard summary statistics (admin only)"""
    if current_user.get("role") != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        summary = get_dashboard_summary_db(db)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard summary: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
