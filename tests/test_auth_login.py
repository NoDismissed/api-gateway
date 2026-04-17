from unittest.mock import patch
from app.grpc_clients.auth_client import AuthServiceClient
from app.grpc_clients.user_client import UserServiceClient


def test_login_success(client):
    fake_user = type(
        "AuthResponse",
        (),
        {
            "id": 1,
            "role": "user"
        },
    )()
    with patch.object(
        AuthServiceClient,
        "authenticate",
        return_value = fake_user,
    ):
        resp = client.post(
            "/auth/login",
            json = {
                "email": "gateway@test.com",
                "password": "hash",
            },
        )
    assert resp.status_code == 200
    assert "access_token" in resp.json


def test_user_cannot_create_user(client, make_token):
    token = make_token(user_id = 1, role = "user")
    response = client.post(
        "/users",
        headers = {"Authorization": f"Bearer {token}"},
        json = {
            "email": "x@test.com",
            "password_hash": "x",
            "role": "user",
        },
    )
    assert response.status_code == 403


def test_admin_can_create_user(client, make_token):
    token = make_token(user_id = 1, role = "admin")
    fake_user = type(
        "User",
        (),
        {
            "email": "x@test.com",
            "role": "user",
            "is_active": True
        },
    )()
    with patch.object(
        UserServiceClient,
        "create_user",
        return_value = fake_user
    ):
        response = client.post(
            "/users",
            headers = {"Authorization": f"Bearer {token}"},
            json = {
                "email": "x@test.com",
                "password_hash": "x",
                "role": "user",
            },
        )
    assert response.status_code == 201


def test_user_cannot_get_other_user(client, make_token):
    token = make_token(user_id = 1, role = "user")
    response = client.get(
        "/users/2",
        headers = {"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
