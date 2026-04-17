import grpc
from app.config import USER_SERVICE_HOST, USER_SERVICE_PORT
from app.auth_pb2_grpc import AuthServiceStub
from app.auth_pb2 import AuthenticateRequest


class AuthServiceClient:

    def __init__(self):
        channel = grpc.insecure_channel(
            f"{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"
        )
        self.stub = AuthServiceStub(channel)


    def authenticate(self, email: str, password: str):
        return self.stub.Authenticate(
            AuthenticateRequest(
                email = email,
                password = password,
            )
        )
