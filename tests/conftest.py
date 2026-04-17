import pytest
from app.app import create_app
from app.config import JWT_ALGORITHM, JWT_EXP_SECONDS, JWT_SECRET
import datetime
import jwt


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_token():
    def _make_token(user_id = 1, role = "user"):
        payload = {
            "sub": str(user_id),
            "role": role,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds = JWT_EXP_SECONDS),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm = JWT_ALGORITHM)
    return _make_token
