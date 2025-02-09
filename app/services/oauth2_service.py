from datetime import datetime, timedelta
import logging
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from app.config.settings import settings
from datetime import datetime, timedelta
from uuid import UUID  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Setup logger
logger = logging.getLogger(__name__)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()

    # Convert UUIDs to strings if present
    if "user_id" in to_encode and isinstance(to_encode["user_id"], UUID):
        to_encode["user_id"] = str(to_encode["user_id"])

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        logger.info("Access token created successfully.")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Could not create token")

def verify_access_token(token: str, credentials_exception: HTTPException) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("user_id")  # Extract user_id as string
        
        if not user_id:
            raise credentials_exception

        logger.info(f"Token verified successfully for user_id: {user_id}")
        return user_id
    
    except JWTError as e:
        logger.error(f"JWT error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected token verification error: {e}")
        raise credentials_exception
