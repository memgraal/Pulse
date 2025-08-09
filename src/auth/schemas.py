from pydantic import ConfigDict, BaseModel, EmailStr, SecretStr
from datetime import date


class UserLoginCredentials(BaseModel):
    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(extra="forbid")


class UserRegistrationCredentials(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    date_of_registration: date

    model_config = ConfigDict(extra="forbid")

