import firebase_admin
from firebase_admin import credentials, storage

# Load Firebase service account key
cred = credentials.Certificate("persona-fastapi-firebase.json")
firebase_admin.initialize_app(cred, {
    "storageBucket": "persona-fastapi.appspot.com"  # Change to your actual storage bucket
})

# Get reference to the storage bucket
bucket = storage.bucket()
