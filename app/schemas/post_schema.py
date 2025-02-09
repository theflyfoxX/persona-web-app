from pydantic import BaseModel
from datetime import datetime

from uuid import UUID

class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID  


    class Config:
        from_attributes = True
        extra = "allow"

class PostCreateRequest(BaseModel):
    title: str
    content: str
    