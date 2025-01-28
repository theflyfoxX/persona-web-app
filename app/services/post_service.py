from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models.post_model import PostModel
import logging

logger = logging.getLogger(__name__)

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def get_posts(self, skip: int = 0, limit: int = 10):
        try:
            posts = self.db.query(PostModel).offset(skip).limit(limit).all()
            if not posts:
                raise HTTPException(status_code=404, detail="No posts found.")
            return posts
        except SQLAlchemyError as e:
            logger.error("Error fetching posts: %s", e)
            raise HTTPException(
                status_code=500, detail="An unexpected database error occurred."
            )

    def create_post(self, post_data, user_id: UUID):
        try:
            if not post_data.title or not post_data.content:
                raise HTTPException(
                    status_code=400, detail="Title and content are required."
                )

            new_post = PostModel(title=post_data.title, content=post_data.content, user_id=user_id)
            self.db.add(new_post)
            self.db.commit()
            self.db.refresh(new_post)
            return new_post
        except IntegrityError as e:
            logger.error("Integrity error creating post: %s", e)
            raise HTTPException(
                status_code=400, detail="Data integrity error. Please check your input."
            )
        except SQLAlchemyError as e:
            logger.error("Error creating post: %s", e)
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred.",
            )

    def get_post_by_id(self, post_id: str):
        try:
            # Validate UUID
            try:
                post_id = UUID(post_id)  # Ensure the ID is a valid UUID
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid UUID format.")

            # Fetch the post
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")
            return post

        except SQLAlchemyError as e:
            logger.error("Error fetching post by ID: %s", e)
            raise HTTPException(
                status_code=500,
                detail="An unexpected database error occurred.",
            )
