from flask import Blueprint, jsonify, request
import grpc
from flask import g
from app.auth.jwt import jwt_required
from app.auth.roles import require_roles
from app.grpc_clients.user_client import UserServiceClient


users_bp = Blueprint("users", __name__)
user_client = UserServiceClient()


@users_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required
def get_user(user_id):
    if g.role != "admin" and g.user_id != user_id:
        return {"error": "Forbidden"}, 403
    try:
        user = user_client.get_user(
            user_id = user_id,
            requester_id = g.user_id,
        )
        return jsonify(
            {
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
        )
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return {"error": "User not found"}, 404
        return {"error": "Internal server error"}, 500


@users_bp.route("/users", methods=["POST"])
@jwt_required
@require_roles("admin")
def create_user():
    data = request.json
    try:
        user = user_client.create_user(
            email = data["email"],
            password_hash = data["password_hash"],
            role = data.get("role", "user"),
        )
        return jsonify(
            {
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
        ), 201
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.ALREADY_EXISTS:
            return {"error": "User already exists"}, 409
        return {"error": f"Internal server error"}, 500


@users_bp.route("/users/<int:user_id>/", methods=["POST"])
@jwt_required
@require_roles("admin")
def update_user(user_id):
    data = request.json
    try:
        user = user_client.update_user(
            user_id = user_id,
            role = data.get("role"),
            is_active = data.get("is_active"),
        )
        return jsonify(
            {
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
            }
        )
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return {"error": "User not found"}, 404
        return {"error": f"Internal server error"}, 500
