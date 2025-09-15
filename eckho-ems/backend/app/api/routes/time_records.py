from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.employee import TimeRecord, Employee
from app.schemas.employee import TimeRecordCreate, TimeRecordRead


router = APIRouter(prefix="/time-records", tags=["time-records"])


@router.get("/", response_model=list[TimeRecordRead])
def list_time_records(
    employee_id: int | None = None,
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(TimeRecord)
    if employee_id is not None:
        query = query.filter(TimeRecord.employee_id == employee_id)
    if start_date is not None:
        query = query.filter(TimeRecord.date >= start_date)
    if end_date is not None:
        query = query.filter(TimeRecord.date <= end_date)
    return query.order_by(TimeRecord.date.desc()).all()


@router.post("/", response_model=TimeRecordRead, status_code=201)
def create_time_record(payload: TimeRecordCreate, db: Session = Depends(get_db)):
    if not db.query(Employee).get(payload.employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    record = TimeRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


