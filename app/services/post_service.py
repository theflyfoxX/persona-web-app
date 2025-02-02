import requests
import json
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
from app.models.post_model import PostModel
import logging

from app.schemas.post_schema import PostResponse

logger = logging.getLogger(__name__)

AZURE_FUNCTION_URL = "http://localhost:7071/api/send-notification"

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def get_posts(self, skip: int = 0, limit: int = 10):
        """Fetch paginated posts from the database."""
        try:
            posts = self.db.query(PostModel).offset(skip).limit(limit).all()
            if not posts:
                raise HTTPException(status_code=404, detail="No posts found.")
            return posts
        except SQLAlchemyError as e:
            logger.error(f"❌ Error fetching posts: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error occurred.")
    
    def create_post(self, post_data, user_id: UUID):
        """Create a new post for a user and trigger an Azure Function."""
        try:
            if not post_data.title or not post_data.content:
                raise HTTPException(status_code=400, detail="Title and content are required.")

            new_post = PostModel(
                title=post_data.title,
                content=post_data.content,
                user_id=user_id
            )

            self.db.add(new_post)
            self.db.commit()
            self.db.refresh(new_post)

            logger.info(f"✅ Post created successfully: {new_post.id}")

            # Call Azure Function for notification and return its response
            azure_response = self.trigger_azure_function(user_id, new_post.id)

            return PostResponse(
            id=new_post.id,
            title=new_post.title,
            content=new_post.content,
            created_at=new_post.created_at,
            updated_at=new_post.updated_at,
            user_id=new_post.user_id
        )

        except IntegrityError as e:
            logger.error(f"⚠️ Integrity error while creating post: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Data integrity error.")

        except SQLAlchemyError as e:
            logger.error(f"❌ Database error while creating post: {str(e)}")
            self.db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred.")

    def get_post_by_id(self, post_id: str):
        """Retrieve a post by its UUID."""
        try:
            # Validate UUID format
            try:
                post_uuid = UUID(post_id)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid UUID format.")

            # Fetch the post
            post = self.db.query(PostModel).filter(PostModel.id == post_uuid).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found.")

            return post

        except SQLAlchemyError as e:
            logger.error(f"❌ Error fetching post by ID ({post_id}): {str(e)}")
            raise HTTPException(status_code=500, detail="Database error occurred.")

    def trigger_azure_function(self, user_id: UUID, post_id: UUID):
        """Send a notification event to Azure Function when a post is created and return its response."""
        payload = {"user_id": str(user_id), "post_id": str(post_id)}

        try:
            response = requests.post(AZURE_FUNCTION_URL, json=payload)
            logger.info(f"🔍 Azure Function Response: {response.status_code} - {response.text}")

            if response.status_code != 200:
                raise HTTPException(
                    status_code=500,
                    detail=f"Azure Function failed: {response.text}"
                )

            # Return the JSON response from Azure Function
            return response.json()

        except Exception as e:
            logger.error(f"⚠️ Error calling Azure Function: {e}")
            raise HTTPException(status_code=500, detail="Failed to call Azure Function.")
