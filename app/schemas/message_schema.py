from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreateRequest(BaseModel):
    conversation_id: str
    sender_id: str
    receiver_id: str
    message: str
    media: Optional[str] = None

class MessageResponse(BaseModel):
    id: str  # MongoDB _id
    conversation_id: str
    sender_id: str
    receiver_id: str
    message: str
    media: Optional[str] = None
    created_at: datetime
    read: bool
