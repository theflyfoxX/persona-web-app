from pytest import Session
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.utils import hash_password
from app.validators import validate_email_address, validate_password
from app.models.user_model import UserModel
import logging
from sqlalchemy.exc import SQLAlchemyError
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_users(self):
        try:
            return self.db.query(UserModel).all()
            return users
        except SQLAlchemyError as e:
            logger.error(f"Database error occurred while fetching users: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=400,
                detail="Failed to fetch users due to a database error."
            ) from e
        except Exception as e:
          logger.error(f"Unexpected error occurred while fetching users: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while fetching users."
        )
        
    def get_user_by_Id(self, user_id: UUID):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found."
                )
            return user
        except SQLAlchemyError as e:
            logger.error(f"Database error fetching user with ID {user_id}: {str(e)}")
            raise HTTPException(status_code=400, detail="Database query failed.")
        except Exception as e:
            logger.error(f"Unexpected error fetching user with ID {user_id}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred.",
            ) from e
    
    def create_user(self, user_data):
        try:
            if not validate_email_address(user_data.email):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid email format."
                )
    
            # Validate password
            if not validate_password(user_data.password):
                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Password must be at least 8 characters long, contain at least "
                        "one uppercase letter, one lowercase letter, one number, "
                        "and one special character."
                    )
                )
            
            # Check if username already exists
            if self.db.query(UserModel).filter(UserModel.username == user_data.username).first():
                raise HTTPException(
                    status_code=400,
                    detail="Username already taken."
                )
            
            # Check if email already exists
            if self.db.query(UserModel).filter(UserModel.email == user_data.email).first():
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered."
                )
            hashed_password = hash_password(user_data.password)
            # Create and add new user
            new_user = UserModel(username=user_data.username, email=user_data.email, password=hashed_password)
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            self.db.rollback()  # Rollback to maintain DB integrity
            logger.error("Integrity error occurred: %s", str(e.orig))
            raise HTTPException(
                status_code=400,
                detail="Username or email already exists."
            ) from e
        except SQLAlchemyError as e:
            logger.error("Error creating user.")
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred.",
            ) from e
