# auth_service.py
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.services.oauth2_service import oauth2_scheme, verify_access_token
from app.utils import hash_password, verify_password
from app.models.user_model import UserModel
from app.database import get_db


def authenticate_user(db: Session, username: str, password: str) -> UserModel | None:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_access_token(token, credentials_exception)
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise credentials_exception
    return user
