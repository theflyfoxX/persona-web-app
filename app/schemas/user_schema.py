from pydantic import BaseModel
from datetime import datetime

from uuid import UUID



class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True
    
class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

class UserLoginRequest(BaseModel):
    username: str
    password: str
   


