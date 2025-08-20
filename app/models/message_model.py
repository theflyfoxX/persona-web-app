from sqlalchemy import Column, String, UUID, ForeignKey, TIMESTAMP, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database_postgres import Base
from app.models.conversation_model import ConversationModel 
import uuid

class MessageMetadataModel(Base):
    __tablename__ = "message_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"))
    sender_id = Column(UUID(as_uuid=True), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), nullable=False)
    message_id = Column(String, unique=True, nullable=False)  # Matches MongoDB _id
    status = Column(Enum("sent", "delivered", "read", name="message_status"), default="sent")
    created_at = Column(TIMESTAMP, server_default=func.now())

    conversation = relationship("ConversationModel", back_populates="messages")
