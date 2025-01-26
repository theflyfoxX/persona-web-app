
import datetime
from sqlalchemy import Integer, String, DateTime, Column
from app.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return f'<User {self.username}>'