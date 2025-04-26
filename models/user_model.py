from pydantic import BaseModel
from uuid import uuid4


# Pydantic model for User
class UserModel(BaseModel):
    id: str = str(uuid4())  # Auto-generate unique user ID
    name: str
    password: str  # New field added for user password
