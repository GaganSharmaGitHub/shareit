from functools import wraps
from fastapi import Request, HTTPException
from tinydb import TinyDB, Query
import base64

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

        # Check user in the database
        user = db.search((User.id == user_id) & (User.password == password))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user ID or password")

        # Attach user object to the request
        request.state.user = user[0]
        return await func(*args, request=request, **kwargs)

    return wrapper
