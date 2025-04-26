from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from tinydb import TinyDB, Query
from models.user_model import UserModel

# Initialize TinyDB
db = TinyDB("db.json")
User = Query()

# Initialize APIRouter
router = APIRouter()


# Create a user
@router.post("/users/", response_model=UserModel)
def create_user(user: UserModel):
    if db.search(User.id == user.id):
        raise HTTPException(status_code=400, detail="User already exists")
    db.insert(user.dict())
    return user


# Read a user
@router.get("/users/{user_id}", response_model=UserModel)
def read_user(user_id: int):
    user = db.search(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


# Update a user
@router.put("/users/{user_id}", response_model=UserModel)
def update_user(user_id: int, user: UserModel):
    if not db.search(User.id == user_id):
        raise HTTPException(status_code=404, detail="User not found")
    db.update(user.dict(), User.id == user_id)
    return user


# Delete a user
@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    if not db.search(User.id == user_id):
        raise HTTPException(status_code=404, detail="User not found")
    db.remove(User.id == user_id)
    return {"message": "User deleted successfully"}
