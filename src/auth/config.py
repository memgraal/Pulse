from authx import AuthX, AuthXConfig
from dotenv import load_dotenv
import os


load_dotenv()

config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv("sec_key")

authx = AuthX(config)

