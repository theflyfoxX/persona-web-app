import logging
import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException
from app.models.post_model import PostModel

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
            logger.error(f"Database error while fetching posts: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

    def create_post(self, post_data, user_id: int):
        try:
            if not post_data.title or not post_data.content:
                raise HTTPException(status_code=400, detail="Title and content are required.")

            new_post = PostModel(
                id=uuid.uuid4(),
                title=post_data.title,
                content=post_data.content,
                user_id=user_id
            )
            self.db.add(new_post)
            self.db.commit()
            self.db.refresh(new_post)
            return new_post
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"Integrity error while creating post: {str(e.orig)}")
            raise HTTPException(status_code=400, detail="Post creation conflict. Please check input data.")
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating post: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

    def get_post_by_id(self, post_id: int):
        try:
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")
            return post
        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching post by ID: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

    def delete_post(self, post_id: int, user_id: int):
        try:
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")
            if post.user_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to delete this post.")

            self.db.delete(post)
            self.db.commit()
            return {"message": "Post deleted successfully"}
        except SQLAlchemyError as e:
            logger.error(f"Database error while deleting post: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

    def update_post(self, post_id: int, post_data, user_id: int):
        try:
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")
            if post.user_id != user_id:
                raise HTTPException(status_code=403, detail="You are not authorized to update this post.")

            if post_data.title:
                post.title = post_data.title
            if post_data.content:
                post.content = post_data.content

            self.db.commit()
            self.db.refresh(post)
            return post
        except SQLAlchemyError as e:
            logger.error(f"Database error while updating post: {str(e)}")
            raise HTTPException(status_code=500, detail="An unexpected database error occurred.")
