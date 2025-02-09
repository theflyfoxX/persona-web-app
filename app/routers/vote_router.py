from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.vote_service import VoteService
from app.schemas.vote_schema import  VoteRequest, VoteResponse
from app.services.auth_service import get_current_user
from app.config.database_postgres import get_db
import logging

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=dict)
async def like_post(
    like_request: VoteRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    like_service = VoteService(db)
    return like_service.like_post(current_user.id, like_request.post_id)

# Unlike a post
@router.delete("/unlike", response_model=dict)
async def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    like_service = VoteService(db)
    return like_service.unlike_post(current_user.id, post_id)


# Get likes for a post
@router.get("/{post_id}", response_model=VoteResponse)
async def get_post_likes(
    post_id: int,
    db: Session = Depends(get_db),
):
    like_service = VoteService(db)
    return like_service.get_post_likes(post_id)

