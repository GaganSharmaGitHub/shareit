from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime


# Pydantic model for User
class UserModel(BaseModel):
    id: str = str(uuid4())  # Auto-generate unique user ID
    name: str
    password: str  # New field added for user password


class FileModel(BaseModel):
    id: str  # Unique identifier for the file
    file_path: str  # Path to the file in the uploads folder
    uploaded_at: str  # Timestamp of when the file was uploaded
    user_id: str  # ID of the user who uploaded the file
