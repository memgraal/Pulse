from fastapi import APIRouter
from .schemas import UserLoginCredentials, UserRegistrationCredentials


router = APIRouter(
    prefix="/auth",
    tags=['Athentication'],
)


@router.post("/login")
def loggining(user: UserLoginCredentials) -> dict:
    ...    


@router.post("/register")
def register(user: UserRegistrationCredentials) -> dict:
    ...