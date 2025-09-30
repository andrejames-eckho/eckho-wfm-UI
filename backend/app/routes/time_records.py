from datetime import date, time
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..services.time_record_service import TimeRecordService
from ..services.user_service import UserService

router = APIRouter(prefix="/time-records", tags=["time-records"])
time_record_service = TimeRecordService()
user_service = UserService()

@router.post(
    "/", 
    response_model=schemas.TimeRecord, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a time record",
    description="Create a new time record for a user"
)
async def create_time_record(
    time_record: schemas.TimeRecordCreate, 
    db: Session = Depends(get_db)
) -> schemas.TimeRecord:
    """
    Create a new time record.
    
    - **user_id**: ID of the user (required)
    - **date**: Date of the record (YYYY-MM-DD)
    - **time**: Time of the record (HH:MM:SS)
    - **record_type**: Type of record (TIME_IN, TIME_OUT, BREAK_IN, BREAK_OUT)
    """
    try:
        # Verify user exists
        user = await user_service.get(db, id=time_record.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return await time_record_service.create(db, obj_in=time_record)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating time record: {str(e)}"
        )

@router.get(
    "/", 
    response_model=List[schemas.TimeRecord],
    summary="List time records",
    description="Get a list of time records with optional filtering"
)
async def read_time_records(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    record_type: Optional[models.RecordType] = Query(None, description="Filter by record type"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[schemas.TimeRecord]:
    """
    Retrieve time records with optional filtering.
    """
    try:
        if user_id:
            # Verify user exists
            user = await user_service.get(db, id=user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            return await time_record_service.get_user_time_records(
                db,
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                record_type=record_type,
                skip=skip,
                limit=limit
            )
        
        # Get all time records with filters
        return await time_record_service.get_multi(
            db,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date,
            record_type=record_type
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving time records: {str(e)}"
        )

@router.get(
    "/{time_record_id}",
    response_model=schemas.TimeRecord,
    summary="Get time record by ID",
    description="Get a specific time record by its ID"
)
async def read_time_record(
    time_record_id: int,
    db: Session = Depends(get_db)
) -> schemas.TimeRecord:
    """
    Get a specific time record by ID.
    """
    try:
        record = await time_record_service.get(db, id=time_record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time record not found"
            )
        return record
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving time record: {str(e)}"
        )

@router.get(
    "/user/{user_id}", 
    response_model=List[schemas.TimeRecord],
    summary="Get user's time records",
    description="Get time records for a specific user with optional filtering"
)
async def read_user_time_records(
    user_id: int,
    start_date: Optional[date] = Query(None, description="Filter by start date"),
    end_date: Optional[date] = Query(None, description="Filter by end date"),
    record_type: Optional[models.RecordType] = Query(None, description="Filter by record type"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[schemas.TimeRecord]:
    """
    Get time records for a specific user with optional filtering.
    """
    try:
        # Verify user exists
        user = await user_service.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return await time_record_service.get_user_time_records(
            db=db,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            record_type=record_type,
            skip=skip,
            limit=limit
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user time records: {str(e)}"
        )

@router.get(
    "/user/{user_id}/daily-summary/{target_date}",
    response_model=dict,
    summary="Get daily summary",
    description="Get a summary of a user's time records for a specific date"
)
async def get_daily_summary(
    user_id: int,
    target_date: date,
    db: Session = Depends(get_db)
) -> dict:
    """
    Get a daily summary of time records for a specific user and date.
    """
    try:
        # Verify user exists
        user = await user_service.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
            
        return await time_record_service.get_daily_summary(
            db=db,
            user_id=user_id,
            target_date=target_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving daily summary: {str(e)}"
        )

@router.delete(
    "/{time_record_id}", 
    response_model=schemas.TimeRecord,
    summary="Delete a time record",
    description="Delete a time record by ID"
)
async def delete_time_record(
    time_record_id: int, 
    db: Session = Depends(get_db)
) -> schemas.TimeRecord:
    """
    Delete a time record by ID.
    """
    try:
        # Verify record exists
        record = await time_record_service.get(db, id=time_record_id)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time record not found"
            )
            
        return await time_record_service.delete(db, id=time_record_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting time record: {str(e)}"
        )
