from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from app.config.database_mongo import messages_collection
from app.config.database_postgres import get_db
from app.models.conversation_model import ConversationModel
from app.models.message_model import MessageMetadataModel
from app.schemas.message_schema import MessageResponse  # Import Response Schema

import logging

logger = logging.getLogger(__name__)

class MessageService:
    def __init__(self, db: Session):
        self.db = db

    async def send_message(self, conversation_id: str, sender_id: str, receiver_id: str, message: str, media: str = None):
      try:
        print(f" Sending Message: {sender_id} → {receiver_id} in Conversation {conversation_id}")

        #  Check if conversation exists
        conversation = self.db.query(ConversationModel).filter_by(id=conversation_id).first()
        if not conversation:
            print(f" Conversation Not Found: {conversation_id}")
            raise HTTPException(status_code=404, detail="Conversation not found. Please create a conversation first.")

        #  Save message in MongoDB
        new_message = {
            "conversation_id": conversation_id,
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "message": message,
            "media": media,
            "created_at": datetime.utcnow(),
            "read": False
        }
        result = await messages_collection.insert_one(new_message)
        message_id = str(result.inserted_id)

        print(f" Message Stored in MongoDB: {message_id}")

        # 3 Save metadata in PostgreSQL
        new_metadata = MessageMetadataModel(
            conversation_id=conversation_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message_id=message_id,
            status="sent",
        )
        self.db.add(new_metadata)
        self.db.commit()
        self.db.refresh(new_metadata)

        print(f" Metadata Saved in PostgreSQL")

        #  Return response matching `MessageResponse`
        return MessageResponse(
            id=message_id,
            conversation_id=conversation_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            message=message,
            media=media,
            created_at=new_message["created_at"],
            read=False
        )

      except Exception as e:
        print(f" Failed to Send Message: {e}")
        raise HTTPException(status_code=500, detail="Failed to send message")

    async def get_messages(self, conversation_id: str):
        """ Retrieve messages from MongoDB for a given conversation """

        try:
            messages_cursor = messages_collection.find({"conversation_id": conversation_id}).sort("created_at", 1)
            messages_list = await messages_cursor.to_list(length=100)  # Convert cursor to list

            if not messages_list:
                return []

            # Format messages to match `MessageResponse` schema
            formatted_messages = [
                MessageResponse(
                    id=str(msg["_id"]),
                    conversation_id=msg["conversation_id"],
                    sender_id=msg["sender_id"],
                    receiver_id=msg["receiver_id"],
                    message=msg["message"],
                    media=msg.get("media", None),
                    created_at=msg["created_at"],
                    read=msg.get("read", False)
                )
                for msg in messages_list
            ]

            return formatted_messages

        except Exception as e:
            logger.error("Error retrieving messages: %s", e)
            raise HTTPException(status_code=500, detail="Failed to retrieve messages")
