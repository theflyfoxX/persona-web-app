from fastapi import APIRouter, Depends, HTTPException, logger, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import utils
from app.services.auth_service import authenticate_user
from app.services.user_service import UserService
from app.services.oauth2_service import create_access_token
from app.models.user_model import UserModel
from app.database import get_db
from app.schemas.user_schema import  UserLoginRequest
from app.schemas.token_schema import Token


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login", response_model=Token)
async def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    # Store user ID (not email) in the token
    access_token = create_access_token(data={"sub": str(user.id), "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}
