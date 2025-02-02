from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class PostResponse(BaseModel):
    id: UUID  # Change from int to UUID
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: UUID  # Ensure user_id remains UUID

    class Config:
        from_attributes = True
        extra = "allow"


class PostCreateRequest(BaseModel):
    title: str
    content: str
    