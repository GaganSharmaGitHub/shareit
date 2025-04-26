from pydantic import BaseModel


# Pydantic model for User
class UserModel(BaseModel):
    id: int
    name: str
    email: str
