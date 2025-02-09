from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user_model import UserModel
from app.services.auth_service import get_current_user
from app.config.database_postgres import get_db
from app.schemas.post_schema import PostCreateRequest, PostResponse
from app.services.post_service import PostService
import logging

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)

@router.get("/", response_model=List[PostResponse])
async def get_posts(
    post_service: PostService = Depends(get_post_service),
    current_user: dict = Depends(get_current_user)
    ):
    try:
        return post_service.get_posts()
    except HTTPException as e:
        logger.error("Failed to fetch posts: %s", e.detail)
        raise e



@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(
    post_data: PostCreateRequest,
    post_service: PostService = Depends(get_post_service),
    current_user: dict = Depends(get_current_user)  
):
    try:
        user_id = current_user.id  

        return post_service.create_post(post_data, user_id)
    except HTTPException as e:
        logger.error("Failed to create post: %s", e.detail)
        raise e

@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(
    post_id: int, post_service : PostService = Depends(get_post_service),
    current_user: dict = Depends(get_current_user)  
):
    try:
        return post_service.get_post_by_id(post_id)
    except HTTPException as e:
        logger.error("Failed to fetch post: %s", e.detail)
        raise e