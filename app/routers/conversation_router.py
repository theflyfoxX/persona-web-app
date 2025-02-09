from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database_postgres import get_db
from app.services.conversation_service import ConversationService
from app.models.conversation_model import ConversationModel
import logging

router = APIRouter()

def get_conversation_service(db: Session = Depends(get_db)):
    return ConversationService(db)

@router.post("/start")
def start_conversation(
    user1_id: str,
    user2_id: str,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    """ Create a new conversation """
    try:
        return conversation_service.start_conversation(user1_id, user2_id)
    except HTTPException as e:
        raise e

