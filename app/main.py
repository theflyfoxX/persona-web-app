from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
import httpx
from app.routers import user_router, auth_router ,post_router,vote_router

from app.services.oauth2_service import oauth2_scheme, verify_access_token

app = FastAPI()

AZURE_FUNCTION_URL = "http://localhost:7071/api/myHttpFunction"  # Change this when deployed

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

# AZURE_FUNCTION_URL = "http://localhost:7071/api/myHttpFunction"

# @app.get("/call-azure-function")
# async def call_azure(name: str, token: str = Depends(oauth2_scheme)):
#     """Call Azure Function with JWT Authentication"""
#     headers = {"Authorization": f"Bearer {token}"}

#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"{AZURE_FUNCTION_URL}?name={name}", headers=headers)
    
#     # Print raw response for debugging
#     print("Azure Function Response:", response.status_code, response.text)

#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail="Error calling Azure Function")

#     return response.json()


app.include_router(post_router.router, prefix="/posts", tags=["Posts"])
app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(auth_router.router, prefix="/auth", tags=["Authentication"])
app.include_router(vote_router.router, prefix="/likes", tags=["Likes"])






