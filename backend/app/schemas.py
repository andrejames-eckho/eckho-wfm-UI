from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from .models import RecordType, Department

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    department: Department

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class TimeRecordBase(BaseModel):
    user_id: int
    date: datetime
    time: datetime
    record_type: RecordType

class TimeRecordCreate(TimeRecordBase):
    pass

class TimeRecord(TimeRecordBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserWithTimeRecords(User):
    time_records: List[TimeRecord] = []