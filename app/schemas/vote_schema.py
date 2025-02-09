
from pydantic import BaseModel
from uuid import UUID


class VoteRequest(BaseModel):
    post_id: UUID
    
    
class VoteResponse(BaseModel):
    post_id: UUID
    like_count: int
    
    