import jwt
import datetime
import grpc
from flask import Blueprint, request, jsonify
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_SECONDS
from app.grpc_clients.auth_client import AuthServiceClient


auth_bp = Blueprint("auth", __name__)
auth_client = AuthServiceClient()


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return {"error": "Invalid payload"}, 400
    try:
        user = auth_client.authenticate(
            email = data["email"],
            password = data["password"],
        )
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            return {"error": "Invalid credentials"}, 401
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            return {"error": "User inactive"}, 403
    except Exception:
        return {"error": "Auth service unavailable"}, 503
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds = JWT_EXP_SECONDS),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return jsonify({"access_token": token})
