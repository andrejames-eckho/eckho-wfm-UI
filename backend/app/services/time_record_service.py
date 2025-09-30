# app/services/time_record_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, date, time
from .. import models, schemas
from .base_service import BaseService

class TimeRecordService(BaseService[models.TimeRecord, schemas.TimeRecordCreate, schemas.TimeRecordUpdate]):
    def __init__(self):
        super().__init__(models.TimeRecord)

    def get_user_time_records(
        self,
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        record_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.TimeRecord]:
        query = db.query(self.model).filter(self.model.user_id == user_id)
        
        if start_date:
            query = query.filter(self.model.date >= start_date)
        if end_date:
            query = query.filter(self.model.date <= end_date)
        if record_type:
            query = query.filter(self.model.record_type == record_type)
            
        return query.order_by(self.model.date.desc(), self.model.time.desc()).offset(skip).limit(limit).all()

    def initialize_user_tracking(self, db: Session, user_id: int) -> None:
        """Initialize time tracking for a new user"""
        # Create current tracking record
        current_tracking = models.CurrentTimeTracking(
            user_id=user_id,
            status='NOT_STARTED'
        )
        db.add(current_tracking)
        db.commit()
        
        # Create today's time record if it doesn't exist
        today = date.today()
        existing_record = db.query(models.TimeRecord).filter(
            models.TimeRecord.user_id == user_id,
            models.TimeRecord.date == today
        ).first()
        
        if not existing_record:
            time_record = models.TimeRecord(
                user_id=user_id,
                date=today,
                time=time(0, 0),
                record_type='TIME_IN'
            )
            db.add(time_record)
            db.commit()

    def get_daily_summary(
        self,
        db: Session,
        user_id: int,
        target_date: date
    ) -> Dict[str, Any]:
        """Get daily summary of time records for a user"""
        records = self.get_user_time_records(
            db=db,
            user_id=user_id,
            start_date=target_date,
            end_date=target_date
        )
        
        return {
            "date": target_date.isoformat(),
            "total_records": len(records),
            "records": [{
                "id": r.id,
                "time": r.time.isoformat(),
                "record_type": r.record_type,
                "created_at": r.created_at.isoformat()
            } for r in records]
        }