from pydantic import BaseModel
from datetime import datetime



class UserResponse(BaseModel):
    id: int
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
    email: str
    password: str
    class Config:
        from_attributes = True


