from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/time-records", tags=["time-records"])

@router.post("/", response_model=schemas.TimeRecord)
def create_time_record(
    time_record: schemas.TimeRecordCreate, db: Session = Depends(get_db)
):
    return crud.create_time_record(db=db, time_record=time_record)

@router.get("/", response_model=list[schemas.TimeRecord])
def read_time_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    time_records = crud.get_time_records(db, skip=skip, limit=limit)
    return time_records

@router.get("/user/{user_id}", response_model=list[schemas.TimeRecord])
def read_user_time_records(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    time_records = crud.get_user_time_records(db, user_id=user_id, skip=skip, limit=limit)
    return time_records
