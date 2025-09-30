# app/services/time_record_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Any, Tuple
from sqlalchemy import func, extract, and_
from sqlalchemy.orm import Session
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
        
    def get_week_start_end(self, target_date: date) -> Tuple[date, date]:
        """Get the start (Monday) and end (Sunday) of the week for the given date"""
        # Monday is 0 and Sunday is 6
        start = target_date - timedelta(days=target_date.weekday())
        end = start + timedelta(days=6)
        return start, end
        
    def get_month_start_end(self, year: int, month: int) -> Tuple[date, date]:
        """Get the start and end dates of the specified month"""
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
            
        start = date(year, month, 1)
        end = date(next_year, next_month, 1) - timedelta(days=1)
        return start, end
        
    def get_weekly_summary(
        self,
        db: Session,
        target_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Get time records for all users for a specific week
        
        Args:
            db: Database session
            target_date: Any date within the target week (defaults to current week)
            
        Returns:
            Dict containing week info and time records grouped by user and date
        """
        if target_date is None:
            target_date = date.today()
            
        week_start, week_end = self.get_week_start_end(target_date)
        
        # Query all time records for the week
        records = db.query(self.model).filter(
            and_(
                self.model.date >= week_start,
                self.model.date <= week_end
            )
        ).order_by(self.model.date, self.model.time).all()
        
        # Group records by user and date
        result = {
            "week_start": week_start.isoformat(),
            "week_end": week_end.isoformat(),
            "records": {}
        }
        
        for record in records:
            user_id = str(record.user_id)
            date_str = record.date.isoformat()
            
            if user_id not in result["records"]:
                result["records"][user_id] = {}
                
            if date_str not in result["records"][user_id]:
                result["records"][user_id][date_str] = []
                
            result["records"][user_id][date_str].append({
                "id": record.id,
                "time": record.time.isoformat(),
                "record_type": record.record_type,
                "created_at": record.created_at.isoformat()
            })
            
        return result
        
    def get_monthly_summary(
        self,
        db: Session,
        year: Optional[int] = None,
        month: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get time records for all users for a specific month
        
        Args:
            db: Database session
            year: Year (defaults to current year)
            month: Month (1-12, defaults to current month)
            
        Returns:
            Dict containing month info and time records grouped by user and date
        """
        today = date.today()
        year = year if year is not None else today.year
        month = month if month is not None else today.month
        
        month_start, month_end = self.get_month_start_end(year, month)
        
        # Query all time records for the month
        records = db.query(self.model).filter(
            and_(
                self.model.date >= month_start,
                self.model.date <= month_end
            )
        ).order_by(self.model.date, self.model.time).all()
        
        # Group records by user and date
        result = {
            "year": year,
            "month": month,
            "month_start": month_start.isoformat(),
            "month_end": month_end.isoformat(),
            "records": {}
        }
        
        for record in records:
            user_id = str(record.user_id)
            date_str = record.date.isoformat()
            
            if user_id not in result["records"]:
                result["records"][user_id] = {}
                
            if date_str not in result["records"][user_id]:
                result["records"][user_id][date_str] = []
                
            result["records"][user_id][date_str].append({
                "id": record.id,
                "time": record.time.isoformat(),
                "record_type": record.record_type,
                "created_at": record.created_at.isoformat()
            })
            
        return result