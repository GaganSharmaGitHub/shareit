from uuid import uuid4
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile, File
from pydantic import BaseModel
from tinydb import TinyDB, Query
from models.user_model import UserModel, FileModel
from functools import wraps
from utils.auth_decorator import auth_required
from utils.db_utils import DBUtils
from datetime import datetime
import os

# Initialize APIRouter
router = APIRouter()

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Create a user
@router.post("/users/", response_model=UserModel)
def create_user(user: UserModel):
    existing_users = DBUtils.find(model_class=UserModel, filters={"id": user.id})
    if existing_users:
        raise HTTPException(status_code=400, detail="User already exists")
    DBUtils.create(user)
    return user


# Read a user
@router.get("/users/{user_id}", response_model=UserModel)
@auth_required
def read_user(user_id: int):
    users = DBUtils.find(model_class=UserModel, filters={"id": user_id})
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[0]


# Update a user
@router.put("/users/{user_id}", response_model=UserModel)
@auth_required
def update_user(user_id: int, user: UserModel):
    existing_users = DBUtils.find(model_class=UserModel, filters={"id": user_id})
    if not existing_users:
        raise HTTPException(status_code=404, detail="User not found")
    DBUtils.update(
        model_class=UserModel, filters={"id": user_id}, data=user.model_dump()
    )
    return user


# Delete a user
@router.delete("/users/{user_id}")
@auth_required
def delete_user(user_id: int):
    existing_users = DBUtils.find(model_class=UserModel, filters={"id": user_id})
    if not existing_users:
        raise HTTPException(status_code=404, detail="User not found")
    DBUtils.delete(model_class=UserModel, filters={"id": user_id})
    return {"message": "User deleted successfully"}


# List all users
@router.get("/users", response_model=list[dict])
def list_users():
    users = DBUtils.find(model_class=UserModel, filters={})
    return [{"id": user.id, "name": user.name} for user in users]


# Get current user
@router.get("/me")
@auth_required
async def get_current_user(request: Request):
    return request.state.user
