from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserWithTimeRecords)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Time Record endpoints
@app.post("/time-records/", response_model=schemas.TimeRecord)
def create_time_record(
    time_record: schemas.TimeRecordCreate, db: Session = Depends(get_db)
):
    return crud.create_time_record(db=db, time_record=time_record)

@app.get("/time-records/", response_model=list[schemas.TimeRecord])
def read_time_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    time_records = crud.get_time_records(db, skip=skip, limit=limit)
    return time_records

@app.get("/users/{user_id}/time-records/", response_model=list[schemas.TimeRecord])
def read_user_time_records(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    time_records = crud.get_user_time_records(db, user_id=user_id, skip=skip, limit=limit)
    return time_records