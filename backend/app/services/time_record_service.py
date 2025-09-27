from datetime import date, time, datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from .base_service import BaseService
from .user_service import UserService

class TimeRecordService(BaseService[models.TimeRecord]):
    def __init__(self):
        super().__init__(models.TimeRecord)
        self.user_service = UserService()

    def create(self, db: Session, *, obj_in: schemas.TimeRecordCreate) -> models.TimeRecord:
        # Verify user exists
        user = self.user_service.get(db, obj_in.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create new time record
        db_time_record = models.TimeRecord(
            user_id=obj_in.user_id,
            date=obj_in.date,
            time=obj_in.time,
            record_type=obj_in.record_type
        )
        
        db.add(db_time_record)
        db.commit()
        db.refresh(db_time_record)
        return db_time_record

    def get_user_time_records(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[models.TimeRecord]:
        # Verify user exists
        if not self.user_service.get(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.date.desc(), self.model.time.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_user_records_for_date(
        self, db: Session, user_id: int, target_date: date
    ) -> List[models.TimeRecord]:
        return (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.date == target_date
            )
            .order_by(self.model.time)
            .all()
        )

    def get_last_record_type(
        self, db: Session, user_id: int, target_date: date
    ) -> Optional[models.RecordType]:
        last_record = (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.date == target_date
            )
            .order_by(self.model.time.desc())
            .first()
        )
        return last_record.record_type if last_record else None
