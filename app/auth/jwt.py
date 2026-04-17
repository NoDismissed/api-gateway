import jwt
from functools import wraps
from flask import request, g
from app.config import JWT_SECRET, JWT_ALGORITHM


def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return {"error": "Missing token"}, 401
        token = auth.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])
            g.user_id = int(payload["sub"])
            g.role = payload["role"]
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401
        return fn(*args, **kwargs)
    return wrapper
