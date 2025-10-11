from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post(
    "/", 
    response_model=schemas.User, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information"
)
async def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
) -> schemas.User:
    """
    Create a new user.
    
    - **username**: Must be unique
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **department**: User's department
    - **is_active**: Whether the user is active (default: True)
    """
    try:
        return await user_service.create(db, obj_in=user)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.get(
    "/", 
    response_model=List[schemas.User],
    summary="List users",
    description="Get a list of users with optional filtering and pagination"
)
async def read_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    department: Optional[str] = Query(None, description="Filter by department"),
    active_only: bool = Query(True, description="Only return active users"),
    db: Session = Depends(get_db)
) -> List[schemas.User]:
    """
    Retrieve users with optional filtering and pagination.
    """
    try:
        if department:
            return await user_service.get_users_by_department(
                db, 
                department=department,
                skip=skip,
                limit=limit,
                active_only=active_only
            )
        return user_service.get_multi(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )

@router.get(
    "/{user_id}", 
    response_model=schemas.UserWithTimeRecords,
    summary="Get user by ID",
    description="Get a specific user by their ID with their time records"
)
async def read_user(
    user_id: int, 
    start_date: Optional[date] = Query(
        None, 
        description="Optional start date to filter time records"
    ),
    end_date: Optional[date] = Query(
        None, 
        description="Optional end date to filter time records"
    ),
    db: Session = Depends(get_db)
) -> schemas.UserWithTimeRecords:
    """
    Get a specific user by ID with optional time record filtering by date range.
    """
    try:
        return await user_service.get_with_time_records(
            db, 
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving user: {str(e)}"
        )

@router.put(
    "/{user_id}", 
    response_model=schemas.User,
    summary="Update a user",
    description="Update an existing user's information"
)
async def update_user(
    user_id: int, 
    user_update: schemas.UserUpdate, 
    db: Session = Depends(get_db)
) -> schemas.User:
    """
    Update a user's information.
    """
    try:
        db_user = await user_service.get(db, id=user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return await user_service.update(db, db_obj=db_user, obj_in=user_update)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating user: {str(e)}"
        )

@router.delete(
    "/{user_id}", 
    response_model=schemas.User,
    summary="Delete a user",
    description="Delete a user by ID"
)
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db)
) -> schemas.User:
    """
    Delete a user by ID.
    """
    try:
        user = await user_service.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return await user_service.delete(db, id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting user: {str(e)}"
        )

@router.post(
    "/{user_id}/deactivate",
    response_model=schemas.User,
    summary="Deactivate a user",
    description="Deactivate a user account by ID"
)
async def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> schemas.User:
    """
    Deactivate a user account.
    """
    try:
        return await user_service.deactivate_user(db, user_id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deactivating user: {str(e)}"
        )

@router.post(
    "/{user_id}/activate",
    response_model=schemas.User,
    summary="Activate a user",
    description="Activate a user account by ID"
)
async def activate_user(
    user_id: int,
    db: Session = Depends(get_db)
) -> schemas.User:
    """
    Activate a user account.
    """
    try:
        return await user_service.activate_user(db, user_id=user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error activating user: {str(e)}"
        )

@router.get(
    "/{user_id}/time-records",
    response_model=List[schemas.TimeRecord],
    summary="Get user's time records",
    description="Get time records for a specific user with optional date filtering"
)
async def get_user_time_records(
    user_id: int,
    start_date: Optional[date] = Query(
        None, 
        description="Optional start date to filter records"
    ),
    end_date: Optional[date] = Query(
        None, 
        description="Optional end date to filter records"
    ),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
) -> List[schemas.TimeRecord]:
    """
    Get time records for a specific user with optional date filtering.
    """
    try:
        return user_service.get_user_time_records(
            db,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            skip=skip,
            limit=limit
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving time records: {str(e)}"
        )
