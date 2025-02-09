import uuid
import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from app.config.utils import hash_password
from app.config.validators import validate_email_address, validate_password
from app.models.user_model import UserModel

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db):
        self.db = db

    def get_users(self):
        try:
            users = self.db.query(UserModel).all()
            if not users:
                raise HTTPException(status_code=404, detail="No users found.")
            return users
        except SQLAlchemyError as e:
            logger.error("Error fetching users: %s", str(e))
            raise HTTPException(status_code=500, detail="An unexpected error occurred while retrieving users.")

    def get_user_by_Id(self, user_id: int):
        try:
            user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found.")
            return user
        except SQLAlchemyError as e:
            logger.error("Error fetching user: %s", str(e))
            raise HTTPException(status_code=500, detail="An unexpected error occurred while retrieving the user.")

    def create_user(self, user_data):
        try:
            if not validate_email_address(user_data.email):
                raise HTTPException(status_code=400, detail="Invalid email format.")

            if not validate_password(user_data.password):
                raise HTTPException(
                    status_code=400,
                    detail=("Password must be at least 8 characters long, contain at least "
                            "one uppercase letter, one lowercase letter, one number, "
                            "and one special character.")
                )

            if self.db.query(UserModel).filter(UserModel.username == user_data.username).first():
                raise HTTPException(status_code=400, detail="Username already taken.")

            if self.db.query(UserModel).filter(UserModel.email == user_data.email).first():
                raise HTTPException(status_code=400, detail="Email already registered.")

            hashed_password = hash_password(user_data.password)
            new_user = UserModel(
                id=uuid.uuid4(),
                username=user_data.username,
                email=user_data.email,
                password=hashed_password
            )
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except IntegrityError as e:
            self.db.rollback()
            logger.error("Integrity error occurred: %s", str(e.orig))
            raise HTTPException(status_code=400, detail="Username or email already exists.")
        except ValueError as e:
            logger.error("Validation error: %s", str(e))
            raise HTTPException(status_code=400, detail=str(e))
        except SQLAlchemyError as e:
            logger.error("Database error: %s", str(e))
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")
