from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services import user_service, time_record_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create(db, obj_in=user)

@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_multi(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas.UserWithTimeRecords)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_with_time_records(db, user_id=user_id)
    return user

@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete(db, id=user_id)
