# app/services/time_record_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta
from typing import Dict, List, Optional, Any, Tuple, Literal
from sqlalchemy import func, extract, and_
from sqlalchemy.orm import Session
from enum import Enum
from .. import models, schemas
from .base_service import BaseService

class AttendanceStatus(str, Enum):
    ON_TIME = "ON_TIME"
    LATE = "LATE"
    EARLY = "EARLY"
    OVERTIME = "OVERTIME"
    UNDERTIME = "UNDERTIME"
    ABSENT = "ABSENT"

class TimeRecordService(BaseService[models.TimeRecord, schemas.TimeRecordCreate, schemas.TimeRecordUpdate]):
    def __init__(self):
        super().__init__(models.TimeRecord)
        
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        **filters
    ) -> List[models.TimeRecord]:
        """
        Get multiple time records with support for date range filtering.
        """
        from datetime import datetime
        
        print(f"[DEBUG] get_multi called with filters: {filters}")
        query = db.query(self.model)
        
        # Handle date range filtering
        start_date = filters.pop('start_date', None)
        end_date = filters.pop('end_date', None)
        
        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            print(f"[DEBUG] Filtering by start_date: {start_date} (type: {type(start_date)})")
            query = query.filter(self.model.date >= start_date)
            
        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            print(f"[DEBUG] Filtering by end_date: {end_date} (type: {type(end_date)})")
            query = query.filter(self.model.date <= end_date)
            
        # Handle other filters
        for field, value in filters.items():
            if hasattr(self.model, field):
                print(f"[DEBUG] Filtering by {field} = {value}")
                query = query.filter(getattr(self.model, field) == value)
        
        # Order by date and time
        query = query.order_by(self.model.date.desc(), self.model.time.desc())
        
        # Print the generated SQL for debugging
        from sqlalchemy import text
        compiled_query = query.statement.compile(compile_kwargs={"literal_binds": True})
        print(f"[DEBUG] Generated SQL: {str(compiled_query)}")
        
        # Execute the query and print the results
        result = query.offset(skip).limit(limit).all()
        print(f"[DEBUG] Found {len(result)} records")
        
        # Print the first few records for debugging
        for i, record in enumerate(result[:5]):
            print(f"[DEBUG] Record {i+1}: id={record.id}, user_id={record.user_id}, date={record.date}, type={record.record_type}, time={record.time}")
            
        return result
        
    async def create_time_record(
        self,
        db: Session,
        user_id: int,
        record_type: models.RecordType,
        record_time: Optional[time] = None,
        record_date: Optional[date] = None,
        commit: bool = True
    ) -> models.TimeRecord:
        """
        Create a new time record with proper validation and business logic.
        
        Args:
            db: Database session
            user_id: ID of the user
            record_type: Type of record (TIME_IN, TIME_OUT, BREAK_IN, BREAK_OUT)
            record_time: Time of the record (defaults to current time if not provided)
            record_date: Date of the record (defaults to current date if not provided)
            commit: Whether to commit the transaction (useful for batch operations)
            
        Returns:
            The created TimeRecord object
            
        Raises:
            HTTPException: If validation fails or there's an error creating the record
        """
        try:
            # Set default values if not provided
            if record_date is None:
                record_date = date.today()
            if record_time is None:
                record_time = datetime.now().time()
                
            # Validate record type
            if not isinstance(record_type, models.RecordType):
                try:
                    record_type = models.RecordType(record_type)
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid record type: {record_type}"
                    )
            
            # Check for duplicate records
            existing_record = await self.get_existing_record(
                db=db,
                user_id=user_id,
                record_date=record_date,
                record_type=record_type
            )
            
            if existing_record:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{record_type.value} record already exists for this user and date"
                )
            
            # Create the time record
            time_record = models.TimeRecord(
                user_id=user_id,
                date=record_date,
                time=record_time,
                record_type=record_type
            )
            
            db.add(time_record)
            
            if commit:
                db.commit()
                db.refresh(time_record)
            
            return time_record
            
        except HTTPException:
            raise
        except Exception as e:
            if not commit:  # Rollback if we're in a transaction
                db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating time record: {str(e)}"
            )
            
    async def get_existing_record(
        self,
        db: Session,
        user_id: int,
        record_date: date,
        record_type: models.RecordType
    ) -> Optional[models.TimeRecord]:
        """
        Check if a time record already exists for the given user, date, and type.
        
        Args:
            db: Database session
            user_id: ID of the user
            record_date: Date of the record
            record_type: Type of record to check for
            
        Returns:
            The existing TimeRecord if found, None otherwise
        """
        return db.query(models.TimeRecord).filter(
            models.TimeRecord.user_id == user_id,
            models.TimeRecord.date == record_date,
            models.TimeRecord.record_type == record_type
        ).first()

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
        
    def _calculate_attendance_status(
        self,
        time_records: List[Dict[str, Any]],
        expected_time_in: Optional[time] = None,
        expected_time_out: Optional[time] = None
    ) -> Dict[str, Any]:
        """
        Calculate attendance status based on time records and expected times
        
        Args:
            time_records: List of time records for a specific date
            expected_time_in: Expected time in (e.g., time(9, 0) for 9:00 AM)
            expected_time_out: Expected time out (e.g., time(17, 0) for 5:00 PM)
            
        Returns:
            Dict containing attendance status and relevant time information
        """
        if not time_records:
            return {
                "status": AttendanceStatus.ABSENT,
                "message": "No time records found",
                "time_in": None,
                "time_out": None,
                "expected_time_in": expected_time_in.isoformat() if expected_time_in else None,
                "expected_time_out": expected_time_out.isoformat() if expected_time_out else None
            }
        
        # Extract time_in and time_out from records
        time_in = None
        time_out = None
        
        for record in time_records:
            if record["record_type"] == "Time In" and not time_in:
                time_in = datetime.strptime(record["time"], "%H:%M:%S").time()
            elif record["record_type"] == "Time Out" and not time_out:
                time_out = datetime.strptime(record["time"], "%H:%M:%S").time()
        
        # If no time in, consider absent
        if not time_in:
            return {
                "status": AttendanceStatus.ABSENT,
                "message": "No time in record",
                "time_in": None,
                "time_out": time_out.isoformat() if time_out else None,
                "expected_time_in": expected_time_in.isoformat() if expected_time_in else None,
                "expected_time_out": expected_time_out.isoformat() if expected_time_out else None
            }
        
        # If no expected time in, just return the basic info
        if not expected_time_in:
            return {
                "status": AttendanceStatus.ON_TIME,
                "message": "No expected time set",
                "time_in": time_in.isoformat(),
                "time_out": time_out.isoformat() if time_out else None,
                "expected_time_in": None,
                "expected_time_out": expected_time_out.isoformat() if expected_time_out else None
            }
        
        # Calculate time differences in minutes
        time_in_dt = datetime.combine(date.today(), time_in)
        expected_time_in_dt = datetime.combine(date.today(), expected_time_in)
        minutes_late = (time_in_dt - expected_time_in_dt).total_seconds() / 60
        
        # Determine status based on time differences
        status = AttendanceStatus.ON_TIME
        message = "On time"
        
        if minutes_late > 15:  # More than 15 minutes late
            status = AttendanceStatus.LATE
            message = f"{int(minutes_late)} minutes late"
        elif minutes_late < -15:  # More than 15 minutes early
            status = AttendanceStatus.EARLY
            message = f"{int(abs(minutes_late))} minutes early"
        
        # Check for overtime/undertime if time_out and expected_time_out are provided
        if time_out and expected_time_out:
            time_out_dt = datetime.combine(date.today(), time_out)
            expected_time_out_dt = datetime.combine(date.today(), expected_time_out)
            minutes_overtime = (time_out_dt - expected_time_out_dt).total_seconds() / 60
            
            if minutes_overtime > 15:  # More than 15 minutes overtime
                status = AttendanceStatus.OVERTIME
                message = f"{int(minutes_overtime)} minutes overtime"
            elif minutes_overtime < -15:  # More than 15 minutes undertime
                status = AttendanceStatus.UNDERTIME
                message = f"{int(abs(minutes_overtime))} minutes undertime"
        
        return {
            "status": status,
            "message": message,
            "time_in": time_in.isoformat(),
            "time_out": time_out.isoformat() if time_out else None,
            "expected_time_in": expected_time_in.isoformat(),
            "expected_time_out": expected_time_out.isoformat() if expected_time_out else None
        }

    def get_attendance_summary(
        self,
        db: Session,
        user_id: int,
        start_date: date,
        end_date: date,
        expected_work_hours: Dict[date, Dict[str, Optional[time]]] = None
    ) -> Dict[date, Dict[str, Any]]:
        """
        Get attendance summary for a user within a date range
        
        Args:
            db: Database session
            user_id: User ID to get attendance for
            start_date: Start date of the range (inclusive)
            end_date: End date of the range (inclusive)
            expected_work_hours: Optional dict mapping dates to expected work hours
                              Format: {date: {"time_in": time, "time_out": time}}
                              
        Returns:
            Dict mapping dates to attendance information
        """
        # Get all time records for the date range
        records = self.get_user_time_records(
            db=db,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        # Group records by date
        records_by_date = {}
        for record in records:
            date_str = record.date.isoformat()
            if date_str not in records_by_date:
                records_by_date[date_str] = []
            records_by_date[date_str].append({
                "id": record.id,
                "time": record.time.isoformat(),
                "record_type": record.record_type.value,
                "created_at": record.created_at.isoformat()
            })
        
        # Generate attendance for each day in the range
        attendance = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.isoformat()
            day_records = records_by_date.get(date_str, [])
            
            # Get expected work hours for this date if provided
            expected_in = None
            expected_out = None
            if expected_work_hours and current_date in expected_work_hours:
                expected_in = expected_work_hours[current_date].get("time_in")
                expected_out = expected_work_hours[current_date].get("time_out")
            
            # Calculate attendance status
            attendance[current_date] = self._calculate_attendance_status(
                time_records=day_records,
                expected_time_in=expected_in,
                expected_time_out=expected_out
            )
            
            current_date += timedelta(days=1)
        
        return attendance

    def get_monthly_summary(
        self,
        db: Session,
        year: Optional[int] = None,
        month: Optional[int] = None,
        include_attendance: bool = False,
        expected_work_hours: Dict[date, Dict[str, Optional[time]]] = None
    ) -> Dict[str, Any]:
        """
        Get time records for all users for a specific month
        
        Args:
            db: Database session
            year: Year (defaults to current year)
            month: Month (1-12, defaults to current month)
            include_attendance: Whether to include attendance status
            expected_work_hours: Optional dict mapping dates to expected work hours
                              Format: {date: {"time_in": time, "time_out": time}}
                              
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
                "record_type": record.record_type.value,
                "created_at": record.created_at.isoformat()
            })
        
        # Add attendance status if requested
        if include_attendance:
            for user_id, user_records in result["records"].items():
                # Get expected work hours for this user if provided
                user_expected_hours = None
                if expected_work_hours:
                    user_expected_hours = {
                        date.fromisoformat(d): v 
                        for d, v in expected_work_hours.items()
                        if str(v.get("user_id")) == user_id
                    }
                
                # Get attendance for this user
                attendance = self.get_attendance_summary(
                    db=db,
                    user_id=int(user_id),
                    start_date=month_start,
                    end_date=month_end,
                    expected_work_hours=user_expected_hours
                )
                
                # Add attendance status to each day's records
                for date_str in user_records:
                    if date.fromisoformat(date_str) in attendance:
                        user_records[date_str].append({
                            "attendance": attendance[date.fromisoformat(date_str)]
                        })
        
        return result