from functools import wraps
from flask import g


def require_roles(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if g.role not in allowed_roles:
                return {"error": "Forbidden"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
