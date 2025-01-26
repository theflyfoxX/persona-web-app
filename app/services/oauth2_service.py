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
    to_encode.update({"exp": expire, "sub": str(data["user_id"])}) 
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.info("Access token created successfully.")
    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id_str: str = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        
        user_id = int(user_id_str)  # Convert user_id to integer
        logger.info(f"Token verified, user_id: {user_id}")
        return user_id
    except JWTError as e:
        logger.error(f"JWT error: {e}")
        raise credentials_exception
    except ValueError:
        logger.error("Invalid user ID in token (not an integer).")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise credentials_exception

