from pydantic import ConfigDict, BaseModel, EmailStr, SecretStr
from datetime import date


class UserLoginCredentialsSchema(BaseModel):
    email: EmailStr
    password: SecretStr

    model_config = ConfigDict(extra="forbid")


class UserRegistrationCredentialsSchema(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    password: SecretStr
    date_of_registration: date

    model_config = ConfigDict(extra="forbid")
