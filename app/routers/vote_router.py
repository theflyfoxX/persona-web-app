from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.vote_service import VoteService
from app.schemas.vote_schema import VoteRequest, VoteResponse
from app.services.auth_service import get_current_user
from app.database import get_db
from uuid import UUID
import logging

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()
# In your router file (e.g., app/routers/vote_router.py)

@router.post("/{post_id}/like", response_model=dict)
async def like_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    like_service = VoteService(db)
    return like_service.like_post(current_user.id, post_id)

@router.delete("/{post_id}/unlike", response_model=dict)
async def unlike_post(
    post_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    like_service = VoteService(db)
    return like_service.unlike_post(current_user.id, post_id)

@router.get("/{post_id}/likes", response_model=VoteResponse)
async def get_post_likes(
    post_id: UUID,
    db: Session = Depends(get_db),
):
    like_service = VoteService(db)
    return like_service.get_post_likes(post_id)