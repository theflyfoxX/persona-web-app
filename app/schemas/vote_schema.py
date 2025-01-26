
from pydantic import BaseModel


class VoteRequest(BaseModel):
    post_id: int
    
    
class VoteResponse(BaseModel):
    post_id: int
    like_count: int
    
    