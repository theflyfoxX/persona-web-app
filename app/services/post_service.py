from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.post_model import PostModel
import logging

logger = logging.getLogger(__name__)

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def get_posts(self, skip: int = 0, limit: int = 10):
      try:
        return self.db.query(PostModel).offset(skip).limit(limit).all()
      except SQLAlchemyError as e:
        logger.error("Error fetching posts: %s", e)
        raise HTTPException(
            status_code=500, detail="An unexpected database error occurred."
        )


    def create_post(self, post_data,user_id: int):
        try:
            new_post = PostModel(title=post_data.title, content=post_data.content,user_id=user_id)
            self.db.add(new_post)
            self.db.commit()
            self.db.refresh(new_post)
            return new_post
        except SQLAlchemyError as e:
            logger.error("Error creating post.")
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred.",
            ) from e
            
    def get_post_by_id(self,post_id):
         try:
             return self.db.query(PostModel).filter(PostModel.id == post_id).first()
         except SQLAlchemyError as e:
             logger.error("Error fetching post.")
             raise HTTPException(
                 status_code=500,
                 detail="An unexpected database error occurred.",
                 message="Post id not Found."
             ) from e
