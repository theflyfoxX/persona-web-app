import datetime
import uuid
from sqlalchemy import String, DateTime, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.config.database_postgres import Base

class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    like_count = Column(Integer, nullable=False, server_default='0')

    def __repr__(self):
        return f'<Post {self.title}>'
