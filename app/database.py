import os
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import logging
from dotenv import load_dotenv  
from app.configuration import settings

load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

# Connection string
# DATABASE_URL =  os.environ.get("postgresql://postgres:root@localhost:5432/postgres")
logger.info(f"Database URL: {DATABASE_URL}")
# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Check database connection
def check_db_connection():
    try:
        with engine.connect() as connection:
            logger.info("Database connection successful.")
    except OperationalError as e:
        logger.error("Database connection failed: %s", e)
        raise RuntimeError("Database connection failed.") from e

# Dependency for database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    except OperationalError as e:
        logger.error("OperationalError: %s", e)
        raise HTTPException(
            status_code=500,
            detail="Database connection failed. Please try again later.",
        ) from e
    except SQLAlchemyError as e:
        logger.error("SQLAlchemyError: %s", e)
        raise HTTPException(
            status_code=500,
            detail="An unexpected database error occurred.",
        ) from e
    finally:
        db.close()

# Run the connection check on module load
try:
    check_db_connection()
except RuntimeError:
    logger.critical("Failed to connect to the database during initialization.")
    raise
