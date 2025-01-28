from sqlalchemy import DateTime, ForeignKey, Integer, Column, func
from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class VoteModel(Base):
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

 