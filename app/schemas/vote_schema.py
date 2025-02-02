
from uuid import UUID
from pydantic import BaseModel


class VoteRequest(BaseModel):
    post_id: UUID
    
    
class VoteResponse(BaseModel):
    post_id: UUID
    like_count: int
    
    