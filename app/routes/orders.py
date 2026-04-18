from flask import Blueprint, request, g
import grpc
from app.auth.jwt import jwt_required
from app.grpc_clients.order_client import OrderServiceClient


orders_bp = Blueprint("orders", __name__)
order_client = OrderServiceClient()


@orders_bp.route("/orders", methods=["POST"])
@jwt_required
def create_order():
    data = request.get_json()
    total_amount = data["total_amount"]
    resp = order_client.create_order(
        requester_id = g.user_id,
        role = g.role,
        total_amount = total_amount,
    )
    return {
        "id": resp.order.id,
        "status": resp.order.status,
        "total_amount": resp.order.total_amount,
    }, 201


@orders_bp.route("/orders/<int:order_id>", methods=["GET"])
@jwt_required
def get_order(order_id):
    try:
        resp = order_client.get_order(
            order_id = order_id,
            requester_id = g.user_id,
            role = g.role,
        )
        return {
            "id": resp.order.id,
            "user_id": resp.order.user_id,
            "status": resp.order.status,
            "total_amount": resp.order.total_amount,
        }
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            return {"error": "Order not found"}, 404
        return {"error": "Internal error"}, 500


@orders_bp.route("/orders/<int:order_id>/cancel", methods=["POST"])
@jwt_required
def cancel_order(order_id):
    try:
        resp = order_client.cancel_order(
            order_id = order_id,
            requester_id = g.user_id,
            role = g.role,
        )
        return {
            "id": resp.order.id,
            "status": resp.order.status,
        }
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            return {"error": "Forbidden"}, 403
        if e.code() == grpc.StatusCode.FAILED_PRECONDITION:
            return {"error": "Invalid order state"}, 409
        return {"error": "Internal error"}, 500


@orders_bp.route("/orders/<int:order_id>/ship", methods=["POST"])
@jwt_required
def ship_order(order_id):
    if g.role != "admin":
        return {"error": "Forbidden"}, 403
    resp = order_client.ship_order(
        order_id = order_id,
        requester_id = g.user_id,
        role = g.role,
    )
    return {
        "id": resp.order.id,
        "status": resp.order.status,
    }
