from sqlalchemy import Column, UUID, TIMESTAMP, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database_postgres import Base
import uuid

class ConversationModel(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user1_id = Column(UUID(as_uuid=True), nullable=False)
    user2_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Unique constraint to ensure a user pair has only one conversation
    __table_args__ = (UniqueConstraint("user1_id", "user2_id", name="unique_conversation"),)

    messages = relationship("MessageMetadataModel", back_populates="conversation")
