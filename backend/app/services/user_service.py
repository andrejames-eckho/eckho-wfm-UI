from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models, schemas
from .base_service import BaseService

class UserService(BaseService[models.User]):
    def __init__(self):
        super().__init__(models.User)

    def get_by_username(self, db: Session, username: str) -> Optional[models.User]:
        return db.query(self.model).filter(self.model.username == username).first()

    def create(self, db: Session, *, obj_in: schemas.UserCreate) -> models.User:
        # Check if username already exists
        if self.get_by_username(db, username=obj_in.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Create new user
        db_user = models.User(
            username=obj_in.username,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            department=obj_in.department
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_with_time_records(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> models.User:
        user = db.query(self.model).filter(self.model.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
