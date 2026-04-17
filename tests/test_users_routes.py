import grpc
from unittest.mock import patch
from app.grpc_clients.user_client import UserServiceClient


def test_get_user_success(client, make_token):
    token = make_token(user_id = 1, role = "user")
    fake_user = type(
        "User",
        (),
        {
            "email": "test@example.com",
            "role": "user",
            "is_active": True,
        },
    )()
    with patch.object(
        UserServiceClient,
        "get_user",
        return_value = fake_user,
    ):
        response = client.get(
            "/users/1",
            headers = {"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert response.json == {
        "email": "test@example.com",
        "role": "user",
        "is_active": True,
    }


def test_get_user_not_found(client, make_token):
    token = make_token(user_id = 999, role = "user")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.NOT_FOUND
    with patch.object(
        UserServiceClient,
        "get_user",
        side_effect = error,
    ):
        response = client.get(
            "/users/999",
            headers = {"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}


def test_create_user_success(client, make_token):
    token = make_token(user_id = 1, role = "admin")
    fake_user = type(
        "User",
        (),
        {
            "email": "new@example.com",
            "role": "user",
            "is_active": True,
        },
    )()
    with patch.object(
        UserServiceClient,
        "create_user",
        return_value = fake_user,
    ):
        response = client.post(
            "/users",
            headers = {"Authorization": f"Bearer {token}"},
            json = {
                "email": "new@example.com",
                "password_hash": "hash",
                "role": "user",
            },
        )
    assert response.status_code == 201
    assert response.json == {
        "email": "new@example.com",
        "role": "user",
        "is_active": True,
    }


def test_create_user_conflict(client, make_token):
    token = make_token(user_id = 1, role = "admin")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.ALREADY_EXISTS
    with patch.object(
        UserServiceClient,
        "create_user",
        side_effect = error,
    ):
        response = client.post(
            "/users",
            headers = {"Authorization": f"Bearer {token}"},
            json = {
                "email": "dup@example.com",
                "password_hash": "hash",
            },
        )
    assert response.status_code == 409
    assert response.json == {"error": "User already exists"}


def test_update_user_success(client, make_token):
    token = make_token(user_id = 1, role = "admin")
    fake_user = type(
        "User",
        (),
        {
            "email": "updated@test.com",
            "role": "admin",
            "is_active": False,
        },
    )()
    with patch.object(
        UserServiceClient,
        "update_user",
        return_value = fake_user,
    ) as mock_update:
        response = client.post(
            "/users/2/",
            headers = {"Authorization": f"Bearer {token}"},
            json = {
                "role": "admin",
                "is_active": False,
            },
        )
    assert response.status_code == 200
    assert response.json == {
        "email": "updated@test.com",
        "role": "admin",
        "is_active": False,
    }
    mock_update.assert_called_once_with(
        user_id = 2,
        role = "admin",
        is_active = False,
    )
