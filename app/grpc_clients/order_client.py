import grpc
from app.config import ORDER_SERVICE_HOST, ORDER_SERVICE_PORT
from app.order_pb2_grpc import OrderServiceStub
from app.order_pb2 import CreateOrderRequest, GetOrderRequest, CancelOrderRequest, ShipOrderRequest


class OrderServiceClient:

    def __init__(self):
        host = ORDER_SERVICE_HOST
        port = ORDER_SERVICE_PORT
        channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = OrderServiceStub(channel)


    def create_order(self, requester_id, role, total_amount):
        return self.stub.CreateOrder(
            CreateOrderRequest(
                requester_id = requester_id,
                requester_role = role,
                total_amount = total_amount,
            )
        )


    def get_order(self, order_id, requester_id, role):
        return self.stub.GetOrder(
            GetOrderRequest(
                order_id = order_id,
                requester_id = requester_id,
                requester_role = role,
            )
        )


    def cancel_order(self, order_id, requester_id, role):
        return self.stub.CancelOrder(
            CancelOrderRequest(
                order_id = order_id,
                requester_id = requester_id,
                requester_role = role,
            )
        )


    def ship_order(self, order_id, requester_id, role):
        return self.stub.ShipOrder(
            ShipOrderRequest(
                order_id = order_id,
                requester_id = requester_id,
                requester_role = role,
            )
        )
