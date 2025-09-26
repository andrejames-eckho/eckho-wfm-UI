from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        department=user.department
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_time_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TimeRecord).offset(skip).limit(limit).all()

def create_time_record(db: Session, time_record: schemas.TimeRecordCreate):
    db_time_record = models.TimeRecord(
        user_id=time_record.user_id,
        date=time_record.date,
        time=time_record.time,
        record_type=time_record.record_type
    )
    db.add(db_time_record)
    db.commit()
    db.refresh(db_time_record)
    return db_time_record

def get_user_time_records(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.TimeRecord).filter(
        models.TimeRecord.user_id == user_id
    ).order_by(models.TimeRecord.date.desc()).offset(skip).limit(limit).all()
