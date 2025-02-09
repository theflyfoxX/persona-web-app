from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from app.config.database_mongo import messages_collection
from app.config.database_postgres import get_db
from app.models.conversation_model import ConversationModel
from app.models.message_model import MessageMetadataModel
import logging

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self, db: Session):
        self.db = db

    def start_conversation(self, user1_id: str, user2_id: str):
        """ Create a new conversation if it doesn't exist """
        try:
            # Check if conversation already exists
            existing_conversation = (
                self.db.query(ConversationModel)
                .filter(
                    ((ConversationModel.user1_id == user1_id) & (ConversationModel.user2_id == user2_id)) |
                    ((ConversationModel.user1_id == user2_id) & (ConversationModel.user2_id == user1_id))
                )
                .first()
            )

            if existing_conversation:
                return existing_conversation  # Return existing conversation

            # Create a new conversation
            new_conversation = ConversationModel(user1_id=user1_id, user2_id=user2_id)
            self.db.add(new_conversation)
            self.db.commit()
            self.db.refresh(new_conversation)

            return new_conversation

        except SQLAlchemyError as e:
            logger.error("Database error while creating conversation: %s", e)
            raise HTTPException(status_code=500, detail="Database error")
