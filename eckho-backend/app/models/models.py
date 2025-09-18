from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class EmployeeStatus(str, Enum):
    ON_DUTY = "On Duty"
    ON_BREAK = "On Break"
    OVERTIME = "Overtime"
    LATE = "Late"
    UNDERTIME = "Undertime"
    ON_TIME = "On Time"
    NO_RECORD = "No Record"
    NOT_STARTED = "Not Started"
    COMPLETED = "Completed"

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    user_type: Optional[UserRole] = None
    employee_id: Optional[int] = None
    token: Optional[str] = None

class AdminCredentials(BaseModel):
    username: str
    password: str

class EmployeeCredentials(BaseModel):
    id: int
    username: str
    password: str
    employeeId: int

class TimeTrackingData(BaseModel):
    timeIn: Optional[str] = None
    timeOut: Optional[str] = None
    breakIn: Optional[str] = None
    breakOut: Optional[str] = None
    status: EmployeeStatus = EmployeeStatus.NOT_STARTED

class Employee(BaseModel):
    id: int
    firstName: str
    lastName: str
    username: Optional[str] = None
    type: Optional[str] = None
    phoneNumber: Optional[str] = None
    timeIn: Optional[str] = None
    timeOut: Optional[str] = None
    breakIn: Optional[str] = None
    breakOut: Optional[str] = None
    status: EmployeeStatus = EmployeeStatus.NOT_STARTED
    expectedStartTime: Optional[str] = None

class FieldEmployee(Employee):
    expectedStartTime: str

class TimeRecord(BaseModel):
    id: str
    employeeId: int
    date: datetime
    expectedTimeIn: str
    expectedTimeOut: Optional[str] = None
    timeIn: str
    timeOut: str
    breakIn: str
    breakOut: str
    status: EmployeeStatus

class TimeTrackingRequest(BaseModel):
    employeeId: int
    action: str  # "time_in", "time_out", "break_in", "break_out"

class TimeTrackingResponse(BaseModel):
    success: bool
    message: str
    data: Optional[TimeTrackingData] = None

class EmployeeListResponse(BaseModel):
    employees: List[Employee]
    total: int

class TimeRecordsResponse(BaseModel):
    records: List[TimeRecord]
    total: int

class DateRangeRequest(BaseModel):
    startDate: str
    endDate: str
    employeeId: Optional[int] = None

class StatusUpdateRequest(BaseModel):
    employeeId: int
    status: EmployeeStatus

class EmployeeUpdateRequest(BaseModel):
    firstName: str
    lastName: str
    username: str
    type: str
    phoneNumber: Optional[str] = None
    expectedStartTime: Optional[str] = None
    oldPassword: Optional[str] = None
    password: Optional[str] = None

class EmployeeCreateRequest(BaseModel):
    idNumber: str
    firstName: str
    lastName: str
    username: str
    password: str
    department: str
    expectedStartTime: Optional[str] = None
    faceData: Optional[str] = None
    fingerprintData: Optional[str] = None

class EmployeeCreateResponse(BaseModel):
    success: bool
    message: str
    employee: Optional[Employee] = None
