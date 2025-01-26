
import datetime
from sqlalchemy import Integer, String, DateTime, Column
from app.database import Base

class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    user_id = Column(Integer, nullable=False)
    like_count = Column(Integer, nullable=False, server_default='0')

    def __repr__(self):
        return f'<Post {self.title}>'
    
    