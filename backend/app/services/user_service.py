from datetime import date
from typing import List, Optional, Type, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from .. import models, schemas
from ..database import SessionLocal
from .base_service import BaseService

class UserService(BaseService[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def __init__(self):
        super().__init__(model=models.User)
    """
    Service class for handling user-related operations.
    """
    
    def get_user(self, db: Session, user_id: int) -> Optional[models.User]:
        """
        Retrieve a user by ID.
        
        Args:
            db: Database session
            user_id: ID of the user to retrieve
            
        Returns:
            User model if found, None otherwise
        """
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[models.User]:
        """
        Retrieve a user by username.
        
        Args:
            db: Database session
            username: Username to search for
            
        Returns:
            User model if found, None otherwise
        """
        return db.query(models.User).filter(
            func.lower(models.User.username) == func.lower(username)
        ).first()
    
    def get_users(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        department: Optional[str] = None,
        active_only: bool = True
    ) -> List[models.User]:
        """
        Retrieve a list of users with optional filtering.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            department: Filter by department (optional)
            active_only: Only return active users if True
            
        Returns:
            List of User models
        """
        query = db.query(models.User)
        
        if active_only:
            query = query.filter(models.User.is_active == True)
            
        if department:
            query = query.filter(models.User.department == department)
            
        return query.offset(skip).limit(limit).all()
    
    def create_user(self, db: Session, user: schemas.UserCreate) -> models.User:
        """
        Create a new user.
        
        Args:
            db: Database session
            user: User creation data
            
        Returns:
            Created User model
            
        Raises:
            HTTPException: If username already exists
        """
        db_user = self.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="Username already registered"
            )
            
        # In a real app, you would hash the password here
        # hashed_password = get_password_hash(user.password)
        
        db_user = models.User(
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            department=user.department,
            # password=hashed_password,
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(
        self, 
        db: Session, 
        user_id: int, 
        user_update: schemas.UserUpdate
    ) -> Optional[models.User]:
        """
        Update a user's information.
        
        Args:
            db: Database session
            user_id: ID of the user to update
            user_update: Updated user data
            
        Returns:
            Updated User model if found, None otherwise
        """
        db_user = self.get_user(db, user_id=user_id)
        if not db_user:
            return None
            
        update_data = user_update.dict(exclude_unset=True)
        
        # Remove password from update data (handle separately if needed)
        update_data.pop("password", None)
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
            
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def delete_user(self, db: Session, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            db: Database session
            user_id: ID of the user to delete
            
        Returns:
            True if user was deleted, False if not found
        """
        db_user = self.get_user(db, user_id=user_id)
        if not db_user:
            return False
            
        # In a real app, you might want to soft delete instead
        db.delete(db_user)
        db.commit()
        return True
    
    def deactivate_user(self, db: Session, user_id: int) -> Optional[models.User]:
        """
        Deactivate a user account.
        
        Args:
            db: Database session
            user_id: ID of the user to deactivate
            
        Returns:
            Updated User model if found, None otherwise
        """
        db_user = self.get_user(db, user_id=user_id)
        if not db_user:
            return None
            
        db_user.is_active = False
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def activate_user(self, db: Session, user_id: int) -> Optional[models.User]:
        """
        Activate a user account.
        
        Args:
            db: Database session
            user_id: ID of the user to activate
            
        Returns:
            Updated User model if found, None otherwise
        """
        db_user = self.get_user(db, user_id=user_id)
        if not db_user:
            return None
            
        db_user.is_active = True
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user_time_records(
        self,
        db: Session,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.TimeRecord]:
        """
        Get time records for a specific user with optional date filtering.
        
        Args:
            db: Database session
            user_id: ID of the user
            start_date: Optional start date filter
            end_date: Optional end date filter
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of TimeRecord models
        """
        query = db.query(models.TimeRecord).filter(
            models.TimeRecord.user_id == user_id
        )
        
        if start_date:
            query = query.filter(models.TimeRecord.date >= start_date)
            
        if end_date:
            query = query.filter(models.TimeRecord.date <= end_date)
            
        return query.order_by(
            models.TimeRecord.date.desc(),
            models.TimeRecord.time.desc()
        ).offset(skip).limit(limit).all()

# Create a singleton instance to be used across the application
user_service = UserService()
