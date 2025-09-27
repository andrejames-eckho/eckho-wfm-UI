from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Date, Time  
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class RecordType(str, enum.Enum):
    TIME_IN = "Time In"
    TIME_OUT = "Time Out"
    BREAK_IN = "Break In"
    BREAK_OUT = "Break Out"

class Department(str, enum.Enum):
    FIELD = "Field"
    WAREHOUSE = "Warehouse"
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    department = Column(Enum(Department), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    time_records = relationship("TimeRecord", back_populates="user", cascade="all, delete-orphan")

class TimeRecord(Base):
    __tablename__ = "time_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    record_type = Column(Enum(RecordType), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="time_records")