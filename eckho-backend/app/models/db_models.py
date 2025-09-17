from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from datetime import datetime
import enum

class UserRoleEnum(enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class EmployeeStatusEnum(enum.Enum):
    ON_DUTY = "On Duty"
    ON_BREAK = "On Break"
    OVERTIME = "Overtime"
    LATE = "Late"
    UNDERTIME = "Undertime"
    ON_TIME = "On Time"
    NO_RECORD = "No Record"
    NOT_STARTED = "Not Started"
    COMPLETED = "Completed"

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    expected_start_time = Column(String(10), nullable=True)  # For field employees
    employee_type = Column(String(20), default="warehouse")  # warehouse or field
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    time_records = relationship("TimeRecord", back_populates="employee")
    current_tracking = relationship("CurrentTimeTracking", back_populates="employee", uselist=False)

class TimeRecord(Base):
    __tablename__ = "time_records"
    
    id = Column(String(50), primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    expected_time_in = Column(String(10), nullable=True)
    expected_time_out = Column(String(10), nullable=True)
    time_in = Column(String(10), nullable=True)
    time_out = Column(String(10), nullable=True)
    break_in = Column(String(10), nullable=True)
    break_out = Column(String(10), nullable=True)
    status = Column(Enum(EmployeeStatusEnum), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="time_records")

class CurrentTimeTracking(Base):
    __tablename__ = "current_time_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), unique=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    time_in = Column(String(10), nullable=True)
    time_out = Column(String(10), nullable=True)
    break_in = Column(String(10), nullable=True)
    break_out = Column(String(10), nullable=True)
    status = Column(Enum(EmployeeStatusEnum), default=EmployeeStatusEnum.NOT_STARTED)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    employee = relationship("Employee", back_populates="current_tracking")
