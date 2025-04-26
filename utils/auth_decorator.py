from functools import wraps
from fastapi import Request, HTTPException
from tinydb import TinyDB, Query
import base64
from models.user_model import UserModel
from utils.db_utils import DBUtils

# Initialize TinyDB
db = TinyDB("db.json")
User = Query()


def auth_required(func):
    @wraps(func)
    async def wrapper(*args, request: Request, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Basic "):
            raise HTTPException(
                status_code=401, detail="Authorization header missing or invalid"
            )

        # Decode Basic Auth header
        try:
            auth_decoded = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8")
            user_id, password = auth_decoded.split(":", 1)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid Basic Auth format")

        # Log user_id and password for debugging purposes
        print(f"Debug: user_id={user_id}, password={password}")

        # Validate user_id and password before querying the database
        if not user_id or not password:
            raise HTTPException(
                status_code=401, detail="User ID or password is missing"
            )

        # Log filters for debugging purposes
        filters = {"id": user_id, "password": password}
        print(f"Debug: filters={filters}")

        # Use DBUtils to find the user
        users = DBUtils.find(model_class=UserModel, filters=filters)
        if not users or len(users) != 1:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        # Sanitize user object to exclude password
        user: UserModel = users[0]
        user.password = None
        request.state.user = user

        if (
            callable(func)
            and hasattr(func, "__code__")
            and func.__code__.co_flags & 0x80
        ):
            # If the function is asynchronous, await it
            return await func(*args, request=request, **kwargs)
        else:
            # Otherwise, call it normally
            return func(*args, request=request, **kwargs)

    return wrapper
