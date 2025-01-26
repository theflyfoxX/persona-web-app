from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.vote_model import VoteModel
from app.models.post_model import PostModel


class VoteService:
    def __init__(self, db: Session):
        self.db = db

    def like_post(self, user_id: int, post_id: int):
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

    def unlike_post(self, user_id: int, post_id: int):
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
        if hasattr(post, "like_count"):
            post.like_count -= 1

        self.db.commit()
        return {"message": "Post unliked successfully"}

    def get_post_likes(self, post_id: int):
        # Check if the post exists
        post = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        # Count total likes for a post
        like_count = self.db.query(VoteModel).filter_by(post_id=post_id).count()
        return {"post_id": post_id, "like_count": like_count}
