from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.config.database_postgres import get_db
from app.services.message_service import MessageService
from app.schemas.message_schema import MessageCreateRequest, MessageResponse
from typing import List
import logging

# Initialize logger
logger = logging.getLogger(__name__)

router = APIRouter()

def get_message_service(db: Session = Depends(get_db)):
    return MessageService(db)

@router.post("/", response_model=MessageResponse, status_code=201)
async def send_message(
    message_data: MessageCreateRequest,
    message_service: MessageService = Depends(get_message_service),
):
    """ Send a new message """
    try:
        return await message_service.send_message(
            message_data.conversation_id,
            message_data.sender_id,
            message_data.receiver_id,
            message_data.message,
            message_data.media
        )
    except HTTPException as e:
        logger.error("Failed to send message: %s", e.detail)
        raise e

@router.get("/{conversation_id}", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: str, 
    message_service: MessageService = Depends(get_message_service)
):
    """ Get all messages for a conversation """
    try:
        return await message_service.get_messages(conversation_id)
    except HTTPException as e:
        logger.error("Failed to fetch messages: %s", e.detail)
        raise e

@router.put("/mark_as_read/{message_id}")

async def mark_as_read(
    message_id: str, 
    message_service: MessageService = Depends(get_message_service)
):
    """ Mark a message as read """
    try:
        return await message_service.mark_as_read(message_id)
    except HTTPException as e:
        logger.error("Failed to mark message as read: %s", e.detail)
        raise e
