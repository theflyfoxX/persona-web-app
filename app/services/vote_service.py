from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vote_model import VoteModel
from app.models.post_model import PostModel
from sqlalchemy.exc import SQLAlchemyError
import logging
from uuid import UUID

logger = logging.getLogger(__name__)

class VoteService:
    def __init__(self, db: Session):
        self.db = db

    def like_post(self, user_id: UUID, post_id: UUID):
        try:
            # Ensure IDs are treated as UUIDs
            user_id = str(user_id)
            post_id = str(post_id)

            # Check if the post exists
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the user already liked the post
            existing_like = self.db.query(VoteModel).filter_by(user_id=user_id, post_id=post_id).first()
            if existing_like:
                raise HTTPException(status_code=400, detail="You have already liked this post")

            # Add like
            like = VoteModel(user_id=user_id, post_id=post_id)
            self.db.add(like)

            # Update the like count in the posts table (optional)
            if hasattr(post, "like_count"):
                post.like_count += 1

            self.db.commit()
            return {"message": "Post liked successfully"}

        except SQLAlchemyError as e:
            logger.error("Error liking post: %s", e)
            raise HTTPException(
                status_code=500, detail="An unexpected database error occurred."
            )

    def unlike_post(self, user_id: UUID, post_id: UUID):
        try:
            # Ensure IDs are treated as UUIDs
            user_id = str(user_id)
            post_id = str(post_id)

            # Check if the post exists
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Check if the like exists
            like = self.db.query(VoteModel).filter_by(user_id=user_id, post_id=post_id).first()
            if not like:
                raise HTTPException(status_code=404, detail="Like not found")

            # Remove like
            self.db.delete(like)

            # Update the like count in the posts table (optional)
            if hasattr(post, "like_count") and post.like_count > 0:
                post.like_count -= 1

            self.db.commit()
            return {"message": "Post unliked successfully"}

        except SQLAlchemyError as e:
            logger.error("Error unliking post: %s", e)
            raise HTTPException(
                status_code=500, detail="An unexpected database error occurred."
            )

    def get_post_likes(self, post_id: UUID):
        try:
            # Ensure post_id is treated as UUID
            post_id = str(post_id)

            # Check if the post exists
            post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            # Count total likes for a post
            like_count = self.db.query(VoteModel).filter_by(post_id=post_id).count()
            return {"post_id": post_id, "like_count": like_count}

        except SQLAlchemyError as e:
            logger.error("Error fetching likes for post: %s", e)
            raise HTTPException(
                status_code=500, detail="An unexpected database error occurred."
            )
