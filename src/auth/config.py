from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
import os


load_dotenv()

config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=os.getenv("sec_key"),
    JWT_TOKEN_LOCATION=["headers"],
)

security = AuthX(config=config)
