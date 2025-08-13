from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
import os


load_dotenv()

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_COOKIE_NAME="access_token",
    JWT_SECRET_KEY=os.getenv("sec_key"),
    JWT_TOKEN_LOCATION=["headers", "cookies"],
)

security = AuthX(config=config)
