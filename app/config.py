import os


USER_SERVICE_HOST = os.getenv("USER_SERVICE_HOST")
USER_SERVICE_PORT = os.getenv("USER_SERVICE_PORT")
ORDER_SERVICE_HOST = os.getenv("ORDER_SERVICE_HOST")
ORDER_SERVICE_PORT = os.getenv("ORDER_SERVICE_PORT")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"
JWT_EXP_SECONDS = 3600

if USER_SERVICE_HOST is None:
    raise ValueError("USER_SERVICE_HOST environment variable is not set")

if USER_SERVICE_PORT is None:
    raise ValueError("USER_SERVICE_PORT environment variable is not set")

if ORDER_SERVICE_HOST is None:
    raise ValueError("ORDER_SERVICE_HOST environment variable is not set")

if ORDER_SERVICE_PORT is None:
    raise ValueError("ORDER_SERVICE_PORT environment variable is not set")

if JWT_SECRET is None:
    raise ValueError("JWT_SECRET environment variable is not set")
