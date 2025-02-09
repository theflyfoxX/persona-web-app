from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.config.database_postgres import get_db
from app.schemas.user_schema import UserResponse,UserCreateRequest
from app.services.user_service import UserService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

@router.get("/", response_model=List[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.get_users()
    except HTTPException as e:
        logger.error("Failed to fetch users: %s", e.detail)
        raise e
    
@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreateRequest, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.create_user(user_data)
    except HTTPException as e:
        logger.error("Failed to create user: %s", e.detail)
        raise e
    
@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, user_service : UserService = Depends(get_user_service)):
    try:
        return user_service.get_user_by_Id(user_id)
    except HTTPException as e:
        logger.error("Failed to fetch user: %s", e.detail)
        raise e
    
