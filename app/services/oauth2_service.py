from datetime import datetime, timedelta
import logging
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from app.configuration import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

logger = logging.getLogger(__name__)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))

    # Store user_id as a string (to support UUIDs)
    user_id = str(data["user_id"])  

    to_encode.update({"exp": expire, "user_id": user_id})  # Store as string

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.info(f"Access token created successfully for user_id: {user_id}")
    return encoded_jwt
def verify_access_token(token: str, credentials_exception: HTTPException) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("user_id")

        if not user_id:
            logger.error("Token missing user_id field.")
            raise credentials_exception

        logger.info(f"Token verified, user_id: {user_id}")
        return user_id  # Keep it as a string (UUID-safe)

    except jwt.JWTError as e:
        logger.error(f"JWT error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise credentials_exception
