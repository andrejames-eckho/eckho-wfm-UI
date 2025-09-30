from pydantic import BaseModel, Field
from datetime import datetime, date, time
from typing import List, Optional
from .models import RecordType, Department

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    department: Department

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department: Optional[Department] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TimeRecordBase(BaseModel):
    user_id: int
    date: date
    time: time
    record_type: RecordType

class TimeRecordCreate(TimeRecordBase):
    pass

class TimeRecordUpdate(BaseModel):
    user_id: Optional[int] = None
    date: Optional[date] = None
    time: Optional[time] = None
    record_type: Optional[RecordType] = None

class TimeRecord(TimeRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserWithTimeRecords(User):
    time_records: List[TimeRecord] = []