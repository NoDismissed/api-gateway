import grpc
from unittest.mock import patch
from app import order_pb2


def test_create_order_success(client, make_token):
    token = make_token(user_id = 1, role = "user")
    mock_response = order_pb2.CreateOrderResponse(
        order = order_pb2.Order(
            id = 1,
            user_id = 1,
            status = order_pb2.CREATED,
            total_amount = 100.0,
        )
    )
    with patch(
        "app.routes.orders.order_client.create_order",
        return_value = mock_response,
    ):
        res = client.post(
            "/orders",
            json = {"total_amount": 100.0},
            headers = {"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 201
    data = res.get_json()
    assert data["id"] == 1
    assert data["status"] == order_pb2.CREATED


def test_create_order_without_token_returns_401(client):
    res = client.post(
        "/orders",
        json = {"total_amount": 50.0},
    )
    assert res.status_code == 401


def test_get_order_not_found(client, make_token):
    token = make_token(user_id = 1, role = "user")
    rpc_error = grpc.RpcError()
    rpc_error.code = lambda: grpc.StatusCode.NOT_FOUND
    with patch(
        "app.routes.orders.order_client.get_order",
        side_effect = rpc_error,
    ):
        res = client.get(
            "/orders/999",
            headers = {"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 404
    assert res.get_json()["error"] == "Order not found"


def test_cancel_order_invalid_state(client, make_token):
    token = make_token(user_id = 1, role = "user")
    rpc_error = grpc.RpcError()
    rpc_error.code = lambda: grpc.StatusCode.FAILED_PRECONDITION
    with patch(
        "app.routes.orders.order_client.cancel_order",
        side_effect = rpc_error,
    ):
        res = client.post(
            "/orders/1/cancel",
            headers = {"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 409
    assert "Invalid order state" in res.get_json()["error"]


def test_ship_order_non_admin_forbidden(client, make_token):
    token = make_token(user_id = 2, role = "user")
    res = client.post(
        "/orders/1/ship",
        headers = {"Authorization": f"Bearer {token}"},
    )
    assert res.status_code == 403


def test_ship_order_admin_success(client, make_token):
    token = make_token(user_id = 99, role = "admin")
    mock_response = order_pb2.ShipOrderResponse(
        order = order_pb2.Order(
            id = 1,
            user_id = 1,
            status = order_pb2.SHIPPED,
            total_amount = 100.0,
        )
    )
    with patch(
        "app.routes.orders.order_client.ship_order",
        return_value = mock_response,
    ):
        res = client.post(
            "/orders/1/ship",
            headers = {"Authorization": f"Bearer {token}"},
        )
    assert res.status_code == 200
    assert res.get_json()["status"] == order_pb2.SHIPPED
