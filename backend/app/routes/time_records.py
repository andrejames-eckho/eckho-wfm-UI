from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import time_record_service

router = APIRouter(prefix="/time-records", tags=["time-records"])

@router.post("/", response_model=schemas.TimeRecord, status_code=status.HTTP_201_CREATED)
def create_time_record(
    time_record: schemas.TimeRecordCreate, 
    db: Session = Depends(get_db)
):
    return time_record_service.create(db, obj_in=time_record)

@router.get("/", response_model=list[schemas.TimeRecord])
def read_time_records(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return time_record_service.get_multi(db, skip=skip, limit=limit)

@router.get("/user/{user_id}", response_model=list[schemas.TimeRecord])
def read_user_time_records(
    user_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    return time_record_service.get_user_time_records(
        db, 
        user_id=user_id, 
        skip=skip, 
        limit=limit
    )

@router.delete("/{time_record_id}", response_model=schemas.TimeRecord)
def delete_time_record(
    time_record_id: int, 
    db: Session = Depends(get_db)
):
    return time_record_service.delete(db, id=time_record_id)
