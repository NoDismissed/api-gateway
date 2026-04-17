import grpc
from app.config import USER_SERVICE_HOST, USER_SERVICE_PORT
from app.user_pb2_grpc import UserServiceStub
from app.user_pb2 import GetUserRequest, CreateUserRequest, UpdateUserRequest


class UserServiceClient:

    def __init__(self):
        channel = grpc.insecure_channel(
            f"{USER_SERVICE_HOST}:{USER_SERVICE_PORT}"
        )
        self.stub = UserServiceStub(channel)


    def get_user(self, user_id: int, requester_id: int):
        metadata = (
            ("x-user-id", str(requester_id)),
        )
        return self.stub.GetUser(
            GetUserRequest(id = user_id),
            metadata = metadata,
        )


    def create_user(self, email: str, password_hash: str, role: str):
        return self.stub.CreateUser(
            CreateUserRequest(
                email = email,
                password_hash = password_hash,
                role = role,
            )
        )


    def update_user(self, user_id: int, is_active: bool = None, role: str = None):
        return self.stub.UpdateUser(
            UpdateUserRequest(
                id = user_id,
                is_active = is_active,
                role = role,
            )
        )
