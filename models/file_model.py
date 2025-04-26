from pydantic import BaseModel
from datetime import datetime


class FileModel(BaseModel):
    id: str  # Unique identifier for the file
    file_path: str  # Path to the file in the uploads folder
    uploaded_at: datetime  # Timestamp of when the file was uploaded
    user_id: str  # ID of the user who uploaded the file
    file_name: str  # Name of the file
