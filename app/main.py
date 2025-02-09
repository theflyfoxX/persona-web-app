from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routers import conversation_router, message_router, user_router, auth_router ,post_router,vote_router
from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
import uuid
from app.config.firebase import bucket 

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
app.include_router(message_router.router, prefix="/messages", tags=["Messages"])
app.include_router(conversation_router.router, prefix="/conversations", tags=["Conversations"])





@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Create a unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"uploads/{uuid.uuid4()}.{file_extension}"

    # Upload file to Firebase Storage
    blob = bucket.blob(unique_filename)
    blob.upload_from_string(await file.read(), content_type=file.content_type)

    # Make file public (optional)
    blob.make_public()

    return {"file_url": blob.public_url}


