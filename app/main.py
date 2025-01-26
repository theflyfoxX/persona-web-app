from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import user_router, auth_router ,post_router,vote_router


app = FastAPI()

origins = [
    "http://localhost:9000",  

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(vote_router.router, prefix="/likes", tags=["Likes"])






