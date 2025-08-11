from passlib.context import CryptContext
from pydantic import SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password.get_secret_value())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password.get_secret_value(), hashed_password)