# auth_service.py
import logging
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.services.oauth2_service import oauth2_scheme, verify_access_token
from app.config.utils import hash_password, verify_password
from app.models.user_model import UserModel
from app.config.database_postgres import get_db

logger = logging.getLogger(__name__)

def authenticate_user(db: Session, username: str, password: str) -> UserModel | None:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    logger.info(f"Token received in get_current_user: {token}")  # ✅ Debugging

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(token, credentials_exception)

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        logger.error(f"User with ID {user_id} not found")
        raise credentials_exception

    return user
