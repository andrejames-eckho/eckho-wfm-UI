from datetime import date
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    expected_start_time: str | None = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        from_attributes = True


class TimeRecordBase(BaseModel):
    employee_id: int
    date: date
    expected_time_in: str | None = None
    expected_time_out: str | None = None
    time_in: str | None = None
    time_out: str | None = None
    break_in: str | None = None
    break_out: str | None = None
    status: str | None = None


class TimeRecordCreate(TimeRecordBase):
    pass


class TimeRecordRead(TimeRecordBase):
    id: int

    class Config:
        from_attributes = True


