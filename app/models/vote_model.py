import uuid
from sqlalchemy import DateTime, ForeignKey, Column, func
from sqlalchemy.dialects.postgresql import UUID
from app.config.database_postgres import Base

class VoteModel(Base):
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Vote user_id={self.user_id} post_id={self.post_id}>"
