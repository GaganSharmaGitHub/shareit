from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from tinydb import TinyDB, Query
from models.user_model import UserModel
from functools import wraps
from utils.auth_decorator import auth_required

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
    db.insert(user.model_dump())
    return user


# Read a user
@router.get("/users/{user_id}", response_model=UserModel)
@auth_required
def read_user(user_id: int):
    user = db.search(User.id == user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user[0]


# Update a user
@router.put("/users/{user_id}", response_model=UserModel)
@auth_required
def update_user(user_id: int, user: UserModel):
    if not db.search(User.id == user_id):
        raise HTTPException(status_code=404, detail="User not found")
    db.update(user.model_dump(), User.id == user_id)
    return user


# Delete a user
@router.delete("/users/{user_id}")
@auth_required
def delete_user(user_id: int):
    if not db.search(User.id == user_id):
        raise HTTPException(status_code=404, detail="User not found")
    db.remove(User.id == user_id)
    return {"message": "User deleted successfully"}


# List all users
@router.get("/users", response_model=list[dict])
def list_users():
    users = db.all()
    return [{"id": user["id"], "name": user["name"]} for user in users]
