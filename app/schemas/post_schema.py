from pydantic import BaseModel
from datetime import datetime

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int  


    class Config:
        from_attributes = True
        extra = "allow"

class PostCreateRequest(BaseModel):
    title: str
    content: str
    